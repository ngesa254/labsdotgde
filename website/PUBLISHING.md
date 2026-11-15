# GitHub Pages publication

Website URL: https://ngesa254.github.io/labsdotgde/website/

Editable website files are in `website/dist/`. Publish them by running from the
repository root:

```sh
python3 website/scripts/stage-github-pages.py
```

This copies only `website/dist/` into `docs/website/`. It verifies identical
file checksums and leaves the existing Barista `docs/index.html` and DECODE
`docs/codelabs/` intact. Commit the source and staged output together.

GitHub Pages is configured to publish `/docs` from `release/devfest_2026`.
Push the reviewed commit to `main` and the publishing branch, then wait for the
Pages deployment. If that configuration changes, use the branch selected in
repository Settings → Pages.

Only static files are deployed. Repository visibility remains public; committed
website source can be viewed on GitHub. A custom domain is not configured.

After updating canonical lab docs, run `python3 scripts/sync-labs.py` from
`website/`, review those copies, then stage GitHub Pages again.
