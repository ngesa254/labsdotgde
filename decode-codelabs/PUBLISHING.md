# Future publication plan — documentation only

Proposed future URL: **https://ngesa254.github.io/labsdotgde/codelabs/**. This task has not made that URL live and has not changed Pages, workflows or `docs/`.

## Build output to publish

Run `python3 scripts/build.py` from `decode-codelabs/`, then `.venv/bin/python scripts/validate.py`. Preview the output under a prefix and repeat browser checks. The complete static output is the **contents of `decode-codelabs/site/`**:

```text
index.html
workshop.css
codelab-overrides.css
codelab-navigation.js
codelabs/decode-mpesa-mcp/...
codelabs/decode-adk-payment-agent/...
assets/ngesa.jpeg
assets/fonts/...
downloads/lab1.zip
downloads/lab2.zip
vendor/claat/...
```

Publish that whole tree together. The doubled segment in the resulting lab URL (`/labsdotgde/codelabs/codelabs/decode-mpesa-mcp/`) reflects the landing root plus the generated codelab directory; it is intentional and keeps local relative paths consistent. Flattening it would require a reviewed link/build change.

## Later repository changes, requiring a separate authorized task

First inspect the actual existing Pages source/settings and deployment workflow. If Pages is served from `docs/`, copy/upload the built site contents into a **new `docs/codelabs/` directory**. Preserve `docs/index.html`, the Barista landing page, its assets and all unrelated pages. Do not replace the existing Pages root with this workshop. If Pages uses an Actions artifact instead, add this subtree to the existing artifact assembly without changing the current landing root.

A later maintainer may add a clearly labeled link from the existing site to `codelabs/`, and may add a build/copy job using the pinned toolchain. Those repository-level edits, workflow permissions, branch/Pages settings and publishing actions are outside this task. No proposed command here is authorization to perform them.

Keep the entire relative structure. This edition avoids root-relative content asset paths and corrects the renderer's generated exit controls to a relative landing-page path. Do not rewrite assets to `/...`, since the project is mounted under `/labsdotgde/`.

## Rebuild and release checks

Edit only `labs/*/codelab.md`, editable sample files, diagram definitions and landing assets. Rebuild; replace only the future workshop subtree with the new complete output after review. Generated hashed image names may change; deploy the complete output to avoid stale references. Do not edit exported lesson HTML manually.

Before future publication, resolve the material gates in SOURCE_AUDIT.md/VALIDATION.md: authorized Cloud Run/model checks, Linux/container verification, SDK teardown diagnostics, provider verification for optional Daraja work, human technical/curriculum review and any required licensing review. Keep Draft status until the maintainer deliberately changes it based on review, not merely because export passed.

Include the entire `vendor/claat/` directory and its upstream license notices. The guided runtime now loads locally pinned scripts/styles/fonts; reading/navigation passes with external requests blocked. Cloud exercises, dependency installs and reference links still need network access. No custom tracking account is configured. Verify all URLs, downloads and Back/Next/Done controls at the final project prefix before announcing publication.

## GitHub Pages compatibility

Yes: the landing page, both guided labs, Back/Next/sidebar navigation, diagrams, trainer photo, local fonts/scripts and sample-code downloads are static HTML/CSS/JavaScript/assets. They can run on GitHub Pages as they do through the local HTTP preview, provided the complete `site/` tree and relative paths are preserved. [GitHub describes Pages as static hosting](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages).

GitHub Pages does not run the Python MCP server, ADK service or cloud/payment exercises. Those continue to run in the participant's environment/Cloud Run, exactly as with the local workshop website. No production backend is embedded in the landing page. Pages publication has not been performed.
