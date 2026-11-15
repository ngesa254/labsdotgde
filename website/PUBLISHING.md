# GitLab Pages publication

The repository-level `.gitlab-ci.yml` publishes `website/dist/` on the GitLab
project's default branch. The homepage is prebuilt, so this job needs no npm
installation. It includes the local DECODE codelabs and Barista guide.

1. Select the intended GitLab project and confirm its repository visibility.
2. Add that project's actual clone URL as a separate `gitlab` remote; preserve
   the existing GitHub `origin` remote.
3. Push the committed branch to the project's default branch. Do not force push
   an existing project or replace unrelated history.
4. Check **Build → Pipelines** and wait for the Pages job and deployment.
5. Open **Deploy → Pages** and use the exact URL GitLab reports. Unique-domain
   settings and access controls can affect the URL and who can open it.

This configuration uses current `pages.publish` syntax (GitLab 17.9+). A Pages
runner must be available. Older self-managed installations need configuration
adapted to their version. The pipeline publishes only the static distribution;
it does not deploy repository documents, development scripts, or `.git`.

The existing GitHub Pages configuration and `docs/` content are unchanged.
The `labsdotgde.afrika` name does not register or configure that domain.

After changing canonical lab documents, run `python3 scripts/sync-labs.py` from
`website/`, review the generated copies, and commit them before publishing.

Reference: https://docs.gitlab.com/user/project/pages/
