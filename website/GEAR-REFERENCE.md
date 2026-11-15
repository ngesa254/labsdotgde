# Labs catalogue: GEAR reference

Reference inspected on November 15, 2026:
https://developers.google.com/program/gear/

The local saved GEAR HTML supplied by the user includes the full Step-by-step
guides CSS and eight codelab target URLs. The live official page was also read;
the titles and subjects agree with that saved section.

The catalogue adapts the rounded panel, square grid, ticker strip, scrollable
cards, and circular link buttons. It uses locally authored CSS and existing local
fonts; it does not import Google's page scripts, tracking, logos or account UI.

The three LabsDotGDE entries remain local workshops. The eight entries marked
Google GEAR are external resources, each linking to the corresponding official
g.dev URL provided by Google's page. Their short summaries are newly written.
These additions do not create local copies of those codelabs or imply Google
endorsement, completed exercises, membership benefits or awarded credits.

The web reader could not resolve the g.dev redirects during inspection. The
URLs are taken from the supplied official page, rather than guessed targets.

Edit `labs.json` to maintain entries; `source: google-gear` places an entry in the
external panel. Run `python3 website/scripts/stage-github-pages.py` from the
repository root to rebuild and stage all Pages copies.
