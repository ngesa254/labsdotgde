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
          h('h2', { id: 'practice-title', className: 'practice-title' }, h('a', { href: 'https://en.wikipedia.org/wiki/Shosholoza', target: '_blank', rel: 'noopener noreferrer' }, 'Shosholoza'), h('br', {}), h('span', {}, 'Ship it.')),
          h('p', { className: 'practice-lede' }, 'A lab is where an idea becomes something you can run. We write the code, explain the why, and make room to experiment.'),
          h('ol', { className: 'practice-principles' },
            h('li', {}, h('span', { className: 'mono' }, '① code'), h('p', {}, 'Build useful systems with AI, MCP, and cloud tools. Start small. Make it work. Ship it.')),
            h('li', {}, h('span', { className: 'mono' }, '② teach'), h('p', {}, 'Turn what you learn into a talk, a guided lab, or a better explanation for the next developer.')),
            h('li', {}, h('span', { className: 'mono' }, '③ play'), h('p', {}, 'Try the odd idea. Test the assumption. Leave with a working example and a new question.')),
          ),
          h('a', { className: 'practice-link', href: '#labs' }, 'Find your next lab →'),
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

const labs = [
  { number: '01', title: 'Give your agent useful tools.', text: 'Build a merchant MCP service with FastMCP. Validate baskets, prepare payment payloads, and learn the Cloud Run identity boundary.', tags: ['MCP', 'FastMCP', 'Cloud Run'], href: './codelabs/codelabs/decode-mpesa-mcp/', label: 'Open the MCP lab →' },
  { number: '02', title: 'Connect reasoning to tools.', text: 'Connect a Google ADK agent to your MCP service. Inspect tool calls, test the boundaries, and work through verified results.', tags: ['Google ADK', 'Vertex AI', 'MCP'], href: './codelabs/codelabs/decode-adk-payment-agent/', label: 'Open the agent lab →' },
  { number: '03', title: 'Meet your AI barista.', text: 'Explore an ADK and Streamlit barista on Cloud Run, from the architecture to deployment, with an optional Firestore search extension.', tags: ['Gemini', 'Cloud Run', 'Google ADK'], href: './decode/index.html', label: 'Open the barista guide →' },
];

export function LabsSection() {
  return h('section', { id: 'labs', className: 'sheet sheet--paper labs-sheet', 'aria-labelledby': 'labs-title' },
    h('div', { className: 'sheet__inner' },
      h('div', { className: 'labs-heading' },
        h('div', {}, h('p', { className: 'section-eyebrow mono' }, 'PICK A STARTING POINT'), h('h2', { id: 'labs-title', className: 'section-title' }, 'Start. Build. Grow.')),
        h('p', {}, 'The labs are right here. Open a guide, follow the steps, and get your hands on the code.'),
      ),
      h('div', { className: 'lab-grid' }, ...labs.map(lab => h('article', { className: 'lab-card', key: lab.number },
        h('span', { className: 'lab-card__number mono' }, lab.number),
        h('h3', {}, lab.title), h('p', {}, lab.text),
        h('ul', { className: 'lab-tags', 'aria-label': 'Technologies' }, ...lab.tags.map(tag => h('li', { key: tag }, tag))),
        h('a', { href: lab.href }, lab.label),
      ))),
      h('div', { className: 'labs-bottom' },
        h('a', { href: './codelabs/index.html' }, 'Browse the DECODE workshop →'),
        h('a', { href: 'https://github.com/ngesa254/labsdotgde', target: '_blank', rel: 'noopener noreferrer' }, 'Explore the full lab repository ↗'),
      ),
    ),
    h('div', { className: 'title-block' }, 'SHEET 03 OF 06'),
  );
}

export function ProjectTitleBlock() {
  const cells = [['Project', 'labsdotgde'], ['Drawn by', 'Ngesa Marvin'], ['Revision', 'techxafrika v0.11 · 2026'], ['Sheet', 'A-006 · 6 of 6']];
  return h('dl', { className: 'project-titleblock', 'aria-label': 'Project drawing details' }, ...cells.map(([label, value]) =>
    h('div', { key: label }, h('dt', { className: 'mono' }, label), h('dd', {}, value)),
  ));
}
