# Locally served codelab runtime

These assets remove external runtime/font requests from the generated guided labs. The source codelabs remain claat Markdown and export through claat; this directory supplies the original frontend components locally.

`manifest.json` records upstream download URLs, SHA-256 hashes and retrieval date. `scripts/build.py` verifies every listed asset. `scripts/vendor_runtime.py` bootstraps reviewed upstream downloads and reuses existing completed files; it does not run during ordinary exports. Refresh sources/checksums deliberately rather than fetching a floating runtime at every build.

The codelab elements, custom-element helpers and styles are from the official claat CDN. Syntax highlighting is Google's code-prettify source because the CDN request was rejected by the proxy. Font files come from the official Google Fonts and Material Design Icons repositories; local `fonts.css` and `icons.css` declare the same font family names.

Upstream license notices are preserved here:

- `LICENSE-codelab-components.txt`: Apache License 2.0 for codelab components.
- `LICENSE-MaterialIcons.txt`: Apache License 2.0 for Material Icons.
- `LICENSE-Roboto.txt`, `LICENSE-RobotoMono.txt`, `LICENSE-SourceCodePro.txt`: the respective SIL Open Font License notices.
- `prettify.js` retains its copyright and Apache-2.0 license header.

Ship the complete directory, including notices, with the static site. External documentation links and cloud exercises still require internet access. Reading and guided navigation are tested through a local HTTP server with external network requests blocked.
