import { j as jsx } from './index-CBLKzAzN.js';

const stops = [
  { city: 'Nairobi', x: 80, y: 200 },
  { city: 'Dala', x: 250, y: 90 },
  { city: 'Accra', x: 430, y: 200 },
  { city: 'Cape Town', x: 610, y: 90 },
  { city: 'Kigali', x: 780, y: 200 },
  { city: 'Addis', x: 930, y: 100 },
];

function RouteDrawing() {
  return jsx.jsxs('div', {
    className: 'africa-route',
    children: [
      jsx.jsx('h2', {
        id: 'africa-route-title',
        className: 'africa-route__title',
        children: 'Thuma Mina. From Cape To Cairo',
      }),
      jsx.jsxs('figure', {
        className: 'africa-route__figure',
        'aria-labelledby': 'africa-route-title',
        children: [
          jsx.jsxs('svg', {
            viewBox: '0 0 1000 300',
            className: 'africa-route__map',
            'aria-hidden': true,
            focusable: false,
            children: [
              jsx.jsx('path', {
                className: 'africa-route__path',
                d: 'M80 200 C150 200 170 90 250 90 S360 200 430 200 S540 90 610 90 S710 200 780 200 S870 100 930 100',
                fill: 'none',
              }),
              ...stops.map((stop, index) => jsx.jsxs('g', {
                className: `africa-route__stop${index === stops.length - 1 ? ' africa-route__stop--last' : ''}`,
                children: [
                  jsx.jsx('circle', { cx: stop.x, cy: stop.y, r: index === stops.length - 1 ? 22 : 14 }),
                  jsx.jsx('text', {
                    className: 'africa-route__city',
                    x: stop.x,
                    y: stop.y + (stop.y < 150 ? -50 : 43),
                    textAnchor: 'middle',
                    children: stop.city,
                  }),
                  jsx.jsx('text', {
                    className: 'africa-route__number',
                    x: stop.x,
                    y: stop.y + (stop.y < 150 ? -28 : 63),
                    textAnchor: 'middle',
                    children: `0${index + 1}`,
                  }),
                ],
              }, stop.city)),
            ],
          }),
          jsx.jsx('ol', {
            className: 'africa-route__stops',
            'aria-label': 'Cities along the route',
            children: stops.map((stop, index) => jsx.jsxs('li', {
              children: [
                jsx.jsx('span', { className: 'africa-route__mobile-number mono', 'aria-hidden': true, children: `0${index + 1}` }),
                jsx.jsx('span', { children: stop.city }),
              ],
            }, stop.city)),
          }),
        ],
      }),
    ],
  });
}

export function AfricaRoute() {
  return jsx.jsxs('section', {
    id: 'africa-route', className: 'sheet sheet--paper route-sheet',
    'aria-labelledby': 'africa-route-title',
    children: [
      jsx.jsx('div', { className: 'sheet__inner', children: jsx.jsx(RouteDrawing, {}) }),
      jsx.jsx('div', { className: 'title-block', children: 'SHEET 04 OF 06' }),
    ],
  });
}
