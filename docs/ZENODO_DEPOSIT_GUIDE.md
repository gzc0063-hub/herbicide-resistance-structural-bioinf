# Zenodo Deposit Guide

## What this is and why it matters

A GitHub repository alone is not considered a permanent, citable data source by most
journals — a repo can be renamed, made private, or deleted, and its URL carries no
guarantee of long-term stability. **Zenodo** is a free, CERN-operated research-data
archive that solves this: it connects directly to GitHub, and every time you cut a
**GitHub Release**, Zenodo automatically archives a permanent snapshot of the repository
at that exact commit and mints a **DOI** for it — a citable, versioned, non-removable
record. This is what Pest Management Science's data-availability requirement is actually
asking for: not just "the code is on GitHub," but "here is a permanent DOI for the exact
version of the data/code behind this paper."

Each new release gets its own DOI, and Zenodo also provides a "concept DOI" that always
resolves to the latest version, so the manuscript can cite a single stable identifier even
if the repo is updated after publication.

## What has already been prepared (no account needed for this part)

- `CITATION.cff` — machine-readable citation metadata (author, affiliation, license,
  keywords, abstract). Zenodo reads this automatically when a release is archived.
- `.zenodo.json` — a second, Zenodo-specific metadata file with the same information in
  Zenodo's own schema, for more explicit control over how the deposit's title, creators,
  and license are prefilled (belt-and-suspenders alongside `CITATION.cff`).
- Both files currently omit an ORCID iD for the author — see the `# TODO` comment in
  `CITATION.cff`. Add it whenever you're ready; it is not required for the deposit to work.

## What only you can do (requires your own accounts/login)

1. **Create a Zenodo account** at https://zenodo.org, and log in with **"Log in with
   GitHub"** so the two accounts are linked.
2. Go to https://zenodo.org/account/settings/github/ and find this repository
   (`gzc0063-hub/herbicide-resistance-structural-bioinf`) in the list. Toggle it **on**.
   This does nothing to the repo itself — it just tells Zenodo to watch for new releases.
3. **Cut a GitHub Release** (not just a git tag) once the manuscript is in the state you
   want archived for submission:
   - On GitHub: Releases -> "Draft a new release" -> pick a tag (e.g. `v1.0.0`) -> publish.
   - Or via the `gh` CLI, which is already available in this environment if you'd like me
     to run it when you're ready: `gh release create v1.0.0 --title "v1.0.0" --notes "..."`.
4. Within a few minutes, Zenodo will show the archived deposit with its own DOI at
   https://zenodo.org/account/settings/github/repository/gzc0063-hub/herbicide-resistance-structural-bioinf.
5. Copy that DOI into:
   - `docs/MANUSCRIPT_DRAFT.md`'s Data and Code Availability section (replace the
     "will be created at submission time" sentence with the real DOI).
   - `CITATION.cff`'s `identifiers` field (optional but good practice).

## When to do this

Not yet — the manuscript is still being actively edited in this session (citations,
figures). Cutting the release now would archive a state that's about to change again.
Do this once the manuscript is genuinely submission-ready, so the archived snapshot
matches what a reviewer would actually see referenced by the DOI.
