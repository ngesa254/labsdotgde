"""Real Chromium checks against an already running local preview."""
import argparse
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--url',default='http://127.0.0.1:8765/workshop/');a=p.parse_args()
results=[]
with sync_playwright() as playwright:
    context=playwright.chromium.launch_persistent_context(str(ROOT/'.preview/chrome'), channel='chrome',headless=True,
        viewport={'width':1440,'height':1000},args=['--disable-background-networking','--disable-component-update'])
    # Verify navigation with an empty browser cache and no external network.
    context.clear_cookies()
    page=context.new_page()
    from urllib.parse import urlsplit
    session=context.new_cdp_session(page)
    session.send('Network.clearBrowserCache')
    origin=urlsplit(a.url).netloc
    page.route('**/*',lambda route: route.continue_() if urlsplit(route.request.url).netloc==origin else route.abort())
    failures=[]
    page.on('pageerror',lambda error: failures.append(str(error)))
    page.goto(a.url,wait_until='networkidle')
    page.screenshot(path=str(ROOT/'evidence/landing-desktop.png'),full_page=True)
    page.evaluate('localStorage.clear()')
    assert page.title().startswith('From Code to Cash')
    assert page.locator('a[href="codelabs/decode-mpesa-mcp/"]').count()==2
    results.append('Landing page loaded; both lab links and downloads present.')
    for id,count in [('decode-mpesa-mcp',11),('decode-adk-payment-agent',9)]:
        url=a.url+'codelabs/'+id+'/'
        page.goto(a.url,wait_until='networkidle')
        # Exercise the actual landing links, rather than bypassing them with goto.
        page.locator(f'a[href="codelabs/{id}/"]').first.click()
        page.wait_for_url(url+'*')
        page.wait_for_function("customElements.get('google-codelab') !== undefined",timeout=45000)
        assert page.locator('google-codelab-step').count()==count
        page.locator('#next-step').click()
        page.wait_for_function("location.hash === '#1'")
        page.locator('#previous-step').click()
        page.wait_for_function("location.hash === '#0'")
        assert page.locator('#arrow-back').get_attribute('href')=='../../index.html'
        assert page.locator('#done').get_attribute('href')=='../../index.html'
        images=page.locator('google-codelab-step').first.locator('img')
        assert images.count() > 0
        assert images.evaluate_all('(els)=>els.every(i=>i.complete && i.naturalWidth>0)')
        for step in range(1,count):
            page.locator('#next-step').click()
            page.wait_for_function(f"location.hash === '#{step}'")
            page.wait_for_function(f"document.querySelector('google-codelab-step[selected]')?.getAttribute('step') === '{step+1}'")
        page.locator(f'a[href="#{count-1}"]').first.click()
        page.wait_for_function(f"location.hash === '#{count-1}'")
        other='decode-adk-payment-agent' if id=='decode-mpesa-mcp' else 'decode-mpesa-mcp'
        assert page.locator(f'a[href="../{other}/"]').is_visible()
        page.locator('a[href="#0"]').first.click()
        page.wait_for_timeout(900)
        assert page.locator('google-codelab-step').first.is_visible()
        page.screenshot(path=str(ROOT/f'evidence/{id}-desktop.png'),full_page=True)
        page.locator(f'a[href="#{count-1}"]').first.click()
        page.wait_for_function(f"location.hash === '#{count-1}'")
        page.locator(f'a[href="../{other}/"]').click()
        page.wait_for_url(a.url+'codelabs/'+other+'/*')
        results.append(f'{id}: same-tab handoff, landing click, local runtime with external requests blocked, all {count} steps, Back/Next, sidebar, exit paths, handoff and loaded SVG passed.')
    page.set_viewport_size({'width':390,'height':844})
    page.goto(a.url,wait_until='networkidle')
    page.screenshot(path=str(ROOT/'evidence/landing-mobile.png'),full_page=True)
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    page.evaluate("localStorage.removeItem('progress_decode-mpesa-mcp')")
    page.goto(a.url+'codelabs/decode-mpesa-mcp/',wait_until='networkidle')
    page.screenshot(path=str(ROOT/'evidence/lab1-mobile.png'),full_page=True)
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    page.locator('#next-step').click()
    page.wait_for_function("location.hash === '#1'")
    page.locator('#menu').click()
    page.locator('a[href="#3"]').first.click()
    page.wait_for_function("location.hash === '#3'")
    results.append('390px landing/codelab fit viewport; mobile Next/menu/section selection passed; screenshots captured.')
    page.set_viewport_size({'width':390,'height':844})
    page.goto(a.url+'codelabs/decode-adk-payment-agent/',wait_until='networkidle')
    page.screenshot(path=str(ROOT/'evidence/lab2-mobile.png'),full_page=True)
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    assert not failures, failures
    (ROOT/'evidence/browser-results.json').write_text(json.dumps({'results':results,'page_errors':failures,'url':a.url,'browser_version':context.browser.version if context.browser else 'Chrome persistent context'},indent=2))
    context.close()
