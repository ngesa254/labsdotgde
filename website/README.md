# labsdotgde.afrika

**[Open the website](https://ngesa254.github.io/labsdotgde/)**

A self-contained local home for Ngesa Marvin's labs, technical talks, and developer
advocacy across Afrika. The original blueprint design, motion, city-linked
headlines, and terminal interaction remain; content is now organised around
learning, teaching and shipping.

## Run

```sh
cd "/Users/ngesamarvine/Documents/Terminal F/labsdotgde/website"
npm start
```

Or run `python3 serve.py`. Open http://127.0.0.1:8768.
No install or build is required. Only `dist/` is served. Hidden files, directory
listing and traversal outside that folder are blocked. Set `LABS_SITE_PORT` for
another port.

## Page structure

1. Hero — rotating headlines, matching city coordinates, Browse labs, Book a call,
   Request a Lab, and the intro: “Practical workshops, Hands-on labs, and shared
   know-how for engineers across Afrika.”
2. Shosholoza — a blueprint illustration and three practical
   principles, adapted from the supplied profnandaa visual reference.
3. Start. Build. Grow. — three working local lab links.
4. Thuma Mina. From Cape To Cairo — separate six-city route:
   Nairobi → Dala → Accra → Cape Town → Kigali → Addis.
5. Request a Lab — terminal or plain form, collecting topic, audience and outcome.
6. Footer — socials, the original requested phrase, and a drawing title block:
   Project **labsdotgde**, Drawn by **Ngesa Marvin**, Revision
   **techxafrika v0.11 · 2026**, Sheet **A-006 · 6 of 6**.

The site is an independent personal/community lab resource. Links to Google
programs are learning resources; the website does not claim to be a Google-run
program or promise acceptance, funding, cloud credits or other program benefits.

## Where visitors find the labs

“Browse labs” in the header and “Explore the labs” in the hero lead to `#labs`.
Three catalogue cards open local, published resources from this repository:

| Catalogue card | Local page | Canonical source |
| --- | --- | --- |
| Merchant MCP tools | `dist/codelabs/codelabs/decode-mpesa-mcp/` | `../docs/codelabs/codelabs/decode-mpesa-mcp/` |
| ADK payment agent | `dist/codelabs/codelabs/decode-adk-payment-agent/` | `../docs/codelabs/codelabs/decode-adk-payment-agent/` |
| AI Barista guide | `dist/barista/index.html` | `../developers-day-nairobi-2026/01-ai-barista-cloud-run/BARISTA_CLOUD_RUN_ARCHITECTURE.html` |

`dist/codelabs/` is a copy of the existing published `../docs/codelabs/`, including
its locally vendored fonts, scripts, illustrations, sample archives and licenses.
The Barista copy preserves the original Mermaid architecture and sequence diagrams, including the interactive renderer. Mermaid loads from jsDelivr and requires an internet connection. Refresh copied content when canonical resources change. Cloud exercises and
outbound documentation links may require internet; the Barista diagrams require jsDelivr access, while the DECODE guides serve their runtime assets locally.

## Booking and lab requests

No calendar link was supplied. As approved, “Book a call” opens a contact panel
with Ngesa's LinkedIn profile to agree a time by message. It does not claim a
calendar slot has been booked. Edit `BookCallLink` in `labs-experience.js` when a
real calendar URL is available.

Lab requests download JSON and save browser-local history. They are not sent
automatically. The success view offers another download, a LinkedIn contact link
and a return to the catalogue. The two descriptive fields are exported as
`lab_topic` and `audience_and_outcome`, with request type
`labsdotgde.afrika/lab-request`.

Drafts use `labsdotgde.local.original-draft.v1`; history uses
`labsdotgde.local.requests.v1`. Clear site browser storage to remove them. The
internal DOM identifiers retain `invite` for compatibility with the restored
terminal, but visitor-facing copy says Request a Lab.

## Editing

- `dist/assets/labs-experience.js`: purpose section, catalogue, booking panel,
  project title block.
- `dist/assets/start-build-grow.svg`: standalone, locally editable blueprint art.
- `dist/assets/africa-route.js`: route title and six stops.
- `dist/locations.js`: headline-to-city mapping and coordinates.
- `dist/assets/index-CBLKzAzN.js`: recovered production runtime, with homepage
  adaptations. Third-party runtime license comments are retained.
- `dist/assets/InviteSection-BBDi5jPd.js`: original terminal/form runtime adapted
  for lab requests.
- `dist/styles.css`: original design and additional responsive layouts.
- `dist/app.js`: local draft/history and sharing-note helpers.
- `dist/offline.html`: how to save and share a lab request.

The original authoring JSX/TypeScript and source maps were not supplied. The
website uses recovered production bundles plus the readable modules above.

## Headline locations

| Headline | City |
| --- | --- |
| hapa kazi tu | Nairobi |
| as'hamb', there's a seat | Cape Town |
| all hands on deck | Addis Ababa |
| tukutane production | Nairobi |
| tupo site, kata simu | Nairobi |
| akwaaba, builders | Accra |
| chale, ship am | Accra |
| tugende, ship it | Kigali |

The hero, footer, blueprint scene, crosshair and terminal location use the same
active city. No device location access or remote lookup is used. City centres
are rounded to minutes. Reduced-motion mode keeps the first phrase with Nairobi.
Cape Town and Addis are editorial assignments for the two general phrases.

Coordinates: [Nairobi](https://www.geonames.org/184745/nairobi.html),
[Accra](https://www.geonames.org/2306104/accra.html),
[Kigali](https://www.geonames.org/202061/kigali.html),
[Cape Town](https://www.geonames.org/3369157/cape-town.html),
[Addis Ababa](https://ungegn.un.org/dashboard/cities/details?id=94).

## Privacy and hosting

The website is committed at the user’s request. `website/dist/` is staged to
`docs/` (and `docs/website/` for existing links) for GitHub Pages. The existing Barista and DECODE URLs are preserved.
Publication requires a successful Pages deployment; a custom domain is not configured.
See [PUBLISHING.md](PUBLISHING.md) and [SOURCE-PRIVACY.md](SOURCE-PRIVACY.md).
The homepage loads local assets only and blocks remote connections with CSP.
Social links and program-resource links navigate externally only when clicked.

To refresh the local guide copies after editing canonical published docs, run
`python3 scripts/sync-labs.py` from the website directory. This also refreshes
the Barista guide while preserving its original Mermaid diagrams.
