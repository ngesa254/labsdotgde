import { j as jsx } from './index-CBLKzAzN.js';

function h(tag, props, ...children) {
  return children.length ? jsx.jsxs(tag, { ...props, children }) : jsx.jsx(tag, props || {});
}

export function BookCallLink({ className = '' }) {
  return h('a', {
    href: '#book-call', className: `book-call-link ${className}`.trim(),
    onClick: event => {
      event.preventDefault();
      document.getElementById('book-call-dialog')?.showModal();
    },
  }, 'Book a call ↗');
}

export function CallDialog() {
  return h('dialog', {
    id: 'book-call-dialog', className: 'call-dialog', 'aria-labelledby': 'call-dialog-title',
    onClick: event => { if (event.target === event.currentTarget) event.currentTarget.close(); },
  },
  h('div', { className: 'call-dialog__body' },
    h('button', { type: 'button', className: 'call-dialog__close', 'aria-label': 'Close booking panel', onClick: () => document.getElementById('book-call-dialog').close() }, '×'),
    h('p', { className: 'section-eyebrow mono' }, 'LET’S CONNECT'),
    h('h2', { id: 'call-dialog-title', className: 'section-title' }, 'Find a time. Talk it through.'),
    h('p', {}, 'Planning a lab, a technical talk, or a session for your community? Message Ngesa with your topic and a few times that work for you.'),
    h('a', { className: 'btn btn-primary', href: 'https://www.linkedin.com/in/engngesamarvin/', target: '_blank', rel: 'noopener noreferrer' }, 'Message Ngesa on LinkedIn ↗'),
    h('p', { className: 'call-dialog__note mono' }, 'We’ll arrange a time by message. No appointment is booked on this page.'),
  ));
}

export function PracticeSection() {
  return h('section', { id: 'what-we-are', className: 'sheet sheet--cyanotype-deep practice-sheet', 'aria-labelledby': 'practice-title' },
    h('div', { className: 'sheet__inner' },
      h('div', { className: 'practice-layout' },
        h('div', { className: 'practice-copy' },
          h('p', { className: 'section-eyebrow mono' }, 'THE LABSDOTGDE WAY'),
          h('h2', { id: 'practice-title', className: 'practice-title' }, h('a', { href: 'https://en.wikipedia.org/wiki/Shosholoza', target: '_blank', rel: 'noopener noreferrer' }, 'Shosholoza')),
          h('p', { className: 'practice-lede' }, 'A lab is where an idea becomes something you can run. We write the code, explain the why, and make room to experiment.'),
          h('ol', { className: 'practice-principles' },
            h('li', {}, h('span', { className: 'mono' }, '① code'), h('p', {}, 'Build useful systems with AI, MCP, and cloud tools. Start small. Make it work. Ship it.')),
            h('li', {}, h('span', { className: 'mono' }, '② teach'), h('p', {}, 'Turn what you learn into a talk, a guided lab, or a better explanation for the next developer.')),
            h('li', {}, h('span', { className: 'mono' }, '③ play'), h('p', {}, 'Try the odd idea. Test the assumption. Leave with a working example and a new question.')),
          ),
          h('a', { className: 'practice-link', href: './labs/' }, 'Find your next lab →'),
        ),
        h('figure', { className: 'practice-drawing' },
          h('img', { src: './assets/start-build-grow.svg', width: 540, height: 440, loading: 'lazy', alt: 'The labsdotgde blueprint: code with git push --ship-it, teach community labs, and play with ideas.' }),
          h('figcaption', { className: 'mono' }, 'fig. 01 — anatomy of labsdotgde'),
        ),
      ),
    ),
    h('div', { className: 'title-block' }, 'SHEET 02 OF 06'),
  );
}

export function ProjectTitleBlock() {
  const cells = [['Project', 'labsdotgde'], ['Drawn by', 'Ngesa Marvin'], ['Revision', 'techxafrika v0.11 · 2026'], ['Sheet', 'A-006 · 6 of 6']];
  return h('dl', { className: 'project-titleblock', 'aria-label': 'Project drawing details' }, ...cells.map(([label, value]) =>
    h('div', { key: label }, h('dt', { className: 'mono' }, label), h('dd', {}, value)),
  ));
}
