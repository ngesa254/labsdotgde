/* The archived renderer creates '/' exit links. Keep exits inside this site. */
(() => {
  const update = () => {
    for (const link of document.querySelectorAll('google-codelab #arrow-back, google-codelab #done')) {
      link.setAttribute('href', '../../index.html');
    }
  };
  new MutationObserver(update).observe(document.body, { childList: true, subtree: true });
  customElements.whenDefined('google-codelab').then(() => requestAnimationFrame(update));
  update();
})();
