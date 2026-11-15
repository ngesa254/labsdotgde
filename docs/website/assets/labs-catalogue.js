const search = document.querySelector('#lab-search');
const topic = document.querySelector('#lab-topic');
const cards = [...document.querySelectorAll('.lab-card')];
const count = document.querySelector('#lab-count');
const empty = document.querySelector('#lab-empty');
function filterLabs() {
  const words = search.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
  let visible = 0;
  for (const card of cards) {
    const matches = words.every(word => card.textContent.toLowerCase().includes(word)) &&
      (!topic.value || card.dataset.tags.split('|').includes(topic.value));
    card.hidden = !matches;
    if (matches) visible++;
  }
  count.textContent = `${visible} ${visible === 1 ? 'lab' : 'labs'}`;
  empty.hidden = visible !== 0;
}
search.addEventListener('input', filterLabs);
topic.addEventListener('change', filterLabs);
document.querySelector('#clear-filters').addEventListener('click', () => {
  search.value = ''; topic.value = ''; filterLabs(); search.focus();
});
filterLabs();
