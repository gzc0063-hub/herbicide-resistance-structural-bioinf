# Working conventions for this repo

## Paywalled or bot-blocked papers

When full-text verification requires a paper that's paywalled or blocks automated
access (Wiley, and others like it, have blocked fetch attempts here before): **stop
after one attempt - don't burn tokens on repeated workarounds** (alternate URLs,
scraping, proxies, etc.).

Instead, ask the user for the paper by full citation (authors, year, title, journal,
DOI). They can search for it, download the PDF through their own institutional
access, and upload it directly to the session. This is faster and cheaper than
automated retries against sources known to block that kind of access, and it's the
same path already used successfully for Dayan et al. 2010, Hao et al. 2009, and
Giacomini et al. 2017 (see `docs/references/`).
