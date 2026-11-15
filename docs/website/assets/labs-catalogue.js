const search = document.querySelector('#lab-search');
const topic = document.querySelector('#lab-topic');
const cards = [...document.querySelectorAll('.lab-card')];
const panels = [...document.querySelectorAll('[data-guide-panel]')];
const count = document.querySelector('#lab-count');
const empty = document.querySelector('#lab-empty');
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const refreshControls = [];

for (const panel of panels) {
  const viewport = panel.querySelector('.guide-viewport');
  const controls = panel.querySelector('.guide-controls');
  const previous = controls.querySelector('[data-direction="-1"]');
  const next = controls.querySelector('[data-direction="1"]');
  controls.hidden = false;
  function refresh() {
    previous.disabled = viewport.scrollLeft <= 2;
    next.disabled = viewport.scrollLeft + viewport.clientWidth >= viewport.scrollWidth - 2;
  }
  for (const button of [previous, next]) {
    button.addEventListener('click', () => {
      const first = panel.querySelector('.lab-card:not([hidden])');
      const distance = first ? first.getBoundingClientRect().width + 18 : viewport.clientWidth;
      viewport.scrollBy({ left: Number(button.dataset.direction) * distance, behavior: reducedMotion.matches ? 'auto' : 'smooth' });
    });
  }
  viewport.addEventListener('scroll', refresh, { passive: true });
  new ResizeObserver(refresh).observe(viewport);
  refreshControls.push(refresh);
}

function filterLabs() {
  const words = search.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
  let visible = 0;
  for (const card of cards) {
    const matches = words.every(word => card.textContent.toLowerCase().includes(word)) &&
      (!topic.value || card.dataset.tags.split('|').includes(topic.value));
    card.hidden = !matches;
    if (matches) visible++;
  }
  for (const panel of panels) {
    const matches = [...panel.querySelectorAll('.lab-card')].filter(card => !card.hidden).length;
    panel.hidden = matches === 0;
    panel.querySelector('.guide-count').textContent = `${matches} ${matches === 1 ? 'guide' : 'guides'}`;
    panel.querySelector('.guide-viewport').scrollLeft = 0;
  }
  count.textContent = `${visible} ${visible === 1 ? 'guide' : 'guides'}`;
  empty.hidden = visible !== 0;
  requestAnimationFrame(() => refreshControls.forEach(refresh => refresh()));
}
search.addEventListener('input', filterLabs);
topic.addEventListener('change', filterLabs);
document.querySelector('.catalogue-filters').addEventListener('submit', event => event.preventDefault());
document.querySelector('#clear-filters').addEventListener('click', () => {
  search.value = ''; topic.value = ''; filterLabs(); search.focus();
});
filterLabs();
