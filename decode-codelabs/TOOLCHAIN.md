# Toolchain and renderer behavior

## Tested claat artifact

- Release download: `https://github.com/googlecodelabs/tools/releases/download/v2.2.6/claat-darwin-amd64`.
- SHA-256: `3ba3eebec664076123626c2c77674f7779d5fc5647c53d180399183a3ba31695`.
- Actual `claat version`: `2.2.5-2023-06-15T18:32:06Z-872cbcf`.
- File type: Mach-O 64-bit x86_64. Host: Darwin arm64; the binary executed successfully using existing host compatibility support. No compatibility software or global tool was installed.
- The release label and embedded version differ. Both are recorded; the checksum pins what was actually tested. GitHub release metadata was retrieved successfully; a later tag-ref lookup hit API HTTP 403, so no extra tag/commit identity is inferred.
- `.tools/claat` is ignored. `scripts/install_claat.py` downloads that exact asset and verifies its checksum; `scripts/build.py` rejects an unexpected binary checksum, including through `CLAAT` override.
- No Go is installed/needed for this binary path. Python scripts replace Node watchers. Docker is not an authoring requirement.

For another OS, select an official compatible release binary and verify its provenance/checksum, or build claat from a deliberately pinned source commit with an approved Go toolchain. That is a toolchain migration: update the installer/build pin, record the artifact identity and rerun the complete export/browser checks. The included installer deliberately fails on non-macOS rather than claiming that the macOS asset is portable. A clean Apple Silicon host may need organization-approved compatibility support before this x86 asset runs.

## Build behavior established by export

The [official repository](https://github.com/googlecodelabs/tools) is archived as of 16 December 2025. Its legacy renderer has maintenance implications; this workshop does not imply active upstream support.

The authoritative `labs/*/codelab.md` files keep metadata before the title and blank lines between fields. The tested binary stops metadata at the first blank paragraph, despite current guide prose describing separated fields. Direct export initially failed with “missing at least id: map[author:Ngesa Marvin]”. `scripts/build.py` therefore generates a temporary compact metadata header in ignored `.cache/export/`; it preserves all participant body content and copies local images there. Edit only the authoritative sources.

`Positive` followed by `: text` exported as plain text in the tested binary. The verified `> aside positive` / `> aside negative` forms now export as styled `<aside class="special">` / `<aside class="warning">` elements.

The `author` field is retained in source but not emitted visibly or in the built metadata JSON by this artifact. Each overview includes visible **Author: Ngesa Marvin** and the supplied biography; validation checks the generated attribution. `status: Draft` becomes `status: ["draft"]`; a successful export does not change publication status. Durations are parsed into 97 and 79 minutes, and all 20 steps are checked in order.

claat copies SVG images into hashed `img/` filenames. Build also copies `assets/` so full-size links work. `scripts/diagrams.py` is the editable diagram source; no Mermaid support is assumed. Sample archives are rebuilt from the editable samples. Build output metadata timestamps can change between builds; deterministic archive entries use a fixed date. This is reproducible source-to-output generation, not a claim of bit-identical HTML/JSON across toolchain changes.

## Runtime frontend and navigation

The following upstream resources originally loaded externally; they are now served from `site/vendor/claat/`:

- `https://storage.googleapis.com/claat-public/codelab-elements.css`
- `https://storage.googleapis.com/claat-public/native-shim.js`
- `https://storage.googleapis.com/claat-public/custom-elements.min.js`
- `https://storage.googleapis.com/claat-public/prettify.js`
- `https://storage.googleapis.com/claat-public/codelab-elements.js`
- Google Fonts styles (`fonts.googleapis.com`) and font downloads (`fonts.gstatic.com`) for Roboto, monospace fonts and Material Icons.

A fresh-browser Start Lab click reproduced a failure to initialize navigation while external runtime assets stalled. Both generated labs now reference local scripts/styles/font files, so external CSS and scripts cannot block initialization. `manifest.json` pins each asset by SHA-256, and build verifies those hashes. The codelab theme and typeface families are preserved; the landing page alone uses the DECODE palette.

The runtime components come from the official claat CDN. The CDN's prettify/font downloads were rejected by the proxy, so syntax highlighting comes from Google's upstream `google/code-prettify` source, and font files from Google's `google/fonts` and `google/material-design-icons` repositories. Local `@font-face` declarations replace the Google Fonts request. The corresponding Apache-2.0 and SIL OFL license notices are included alongside the assets. `scripts/vendor_runtime.py` bootstraps those files and reuses completed downloads; normal builds make no runtime-asset network requests. Review upstream versions and refresh checksums deliberately when maintaining the vendored files.

Browser checks block external requests and exercise the actual landing links, every step in both labs, Back/Next, the mobile menu and same-tab handoff. This establishes locally served reading/navigation behavior; cloud exercises, package installation and external references still require network access.

Build passes `-ga=` explicitly because the tool's default global Analytics account is `UA-49880327-14`. It removes the generated analytics component and unused `support.google.com/inapp/api.js`; generated files contain no personal or global tracking ID. The remaining codelab element has an empty `codelab-gaid`. This is inspection of the authored analytics configuration, not a general guarantee about browser extensions or unrelated traffic. No CDN request is required by the exported lesson runtime.

The runtime renderer creates exit/Done links pointing to `/`. Its `index` query handling did not preserve arbitrary subdirectory paths. `site/codelab-navigation.js` observes renderer-created controls and sets those two exits to `../../index.html`. It does not replace the renderer's step navigation. Browser checks verify Back/Next, sidebar, handoff, images and corrected exits under `/workshop/`. Local CSS allows code/table scrolling and responsive images.

## Dependency environments

Samples target CPython 3.11. Authoring validation used **3.11.15**, while Dockerfiles use the versioned `python:3.11.14-slim` base. Neither base-image digests nor Python package artifact hashes are pinned. Linux/container runtime verification is distinct from installed macOS imports and dependency resolution.

Each sample has direct pins (`requirements.txt`) and its installed dependency closure (`requirements.lock`). `scripts/lock_dependencies.py` regenerates these closures only after a deliberate reviewed dependency change; it is not run during ordinary site builds. `requirements-dev.lock` captures the full authoring/test environment including Playwright 1.56.0. No browser is downloaded: browser tests use existing Google Chrome through a profile under `.preview/`.

Important retained source pins: FastMCP 2.12.4, HTTPX 0.28.1 and Google ADK 1.14.0. Explicit additional compatibility pins include MCP 1.14.1, Pydantic 2.11.9, Google Gen AI 1.36.0 and Google Auth 2.40.3. Dotenv changes from source 1.0.1 to 1.1.1 are documented in the audit. Direct package/import compatibility and no-network behavior are tested; current hosted model compatibility requires a later authorized run.
