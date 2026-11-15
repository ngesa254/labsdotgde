# A public website with private project source

Visitors must receive HTML, CSS, JavaScript, fonts and illustrations for their
browser to display this website. Those delivered files can always be inspected,
saved, or copied. Minification and obfuscation cannot make browser code secret.
Disabling right-click or developer-tools keyboard shortcuts does not protect it.

You can keep the authoring repository, Git history, deployment configuration,
server-side code, API credentials, private data, and unpublished files private.

## Suggested layout for this project

1. The user has requested committing this website. It is no longer excluded
   from repository staging. If pushed to a public repository, its committed
   files and history will be public.
2. If private authoring source is required, use a private destination repository.
   Publishing only `dist/` limits the deployed artifact, not repository visibility.
3. Configure your hosting service to publish only `website/dist/` (or `dist/`
   if the private repository contains just this project). Do not deploy the
   surrounding labs repository, `.git`, local documentation or environment files.
4. Keep original source maps out of public deployment. This copy includes none.
   Its production JavaScript is already minified, but is still browser-readable.
5. If you later add real invitation delivery, database writes or secret MCP/API
   credentials, implement those on an authenticated/validated server endpoint.
   Never put secrets in `dist/` or assume a browser request can hide them.
6. Connect the `labsdotgde.afrika` domain to the public site when you own and
   configure that domain. The website name here does not register a domain.

No repository visibility, remote hosting, DNS or domain settings were changed
by the local implementation. The local server serves only `dist/` and blocks
directory listing, hidden files, and paths outside that directory.

## References

- MDN, how browsers receive website code:
  https://developer.mozilla.org/en-US/docs/Learn_web_development/Getting_started/Web_standards/How_the_web_works
- GitHub Pages and repository/plan requirements:
  https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages

GitHub Pages supports private repositories on eligible paid plans. Source
repository privacy and published-site access are separate concerns. Making an
existing repository private can affect its current publishing setup; choose
hosting for the new site before changing the workshop repository's visibility.
