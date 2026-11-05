# AI in Community Colleges: NAAIC AI programs map

An interactive map of AI programs, AI-related grants and documented partnerships at U.S. community colleges,
made for the National Applied AI Consortium (NAAIC). Houston City College built it.

The site has three public parts:

- **Map** (`site/index.html`): one dot per community college with a sourced AI program. Dot color shows the highest
  AI credential the college offers (certificate, associate degree or bachelor's degree). A credential filter shows the
  colleges with any program of that type, whatever their highest credential, and gives all their dots that type's color.
  Dotted lines show documented partnerships.
  A Grants tab, a growth table and a full list of colleges and programs sit below the map.
- **News** (`site/news/index.html`): dated news items about AI programs, grants and events at community colleges.
- **Grants feed** (`site/feed.xml`): an RSS feed of the AI-related grants, newest first.

Every program, grant, partnership and news item links to a public source and carries an "as of" date.
Programs whose launch year still needs confirmation are left out of the published data. They are listed in
`NEEDS-VERIFICATION.md`. `CHANGELOG.md` has the history of public builds.

## What is in this repo

| Path | What it is |
| --- | --- |
| `site/` | The complete published site, exactly as it is live today. Plain static files, no build step needed to serve it. |
| `data/naaic-map.json` | A readable copy of the map data. The same data is embedded in `site/index.html`. |
| `data/ipeds_cip110102_by_year.csv` | Public IPEDS completions for CIP 11.0102 (Artificial Intelligence) by award year, with community college columns and a `source_url` and `as_of` on every row. |
| `data/ipeds_cip110102_by_award_level.csv`, `data/ipeds_cip110102_community_colleges.csv` | The same completions by award level, and college by college for community colleges. |
| `docs/ipeds-cip-11.0102.md` | What the IPEDS row counts, whether it matches NCES, and the history of the code. |
| `scripts/site_data.py` | Moves the data between `data/naaic-map.json` and `site/index.html`, and checks both. |
| `scripts/test_site_data.py` | Tests for the "As featured in" rules in the data check. Run `python3 scripts/test_site_data.py`. |
| `scripts/test_credential_filter.mjs` | Tests for the map's credential filter. Run `node scripts/test_credential_filter.mjs`. |
| `scripts/project_xy.py`, `scripts/geo.mjs` | Look up a college in IPEDS and work out its dot position on the map. |
| `scripts/refresh_ipeds.py` | Downloads the IPEDS college directory file. |
| `scripts/refresh_ipeds_cip.py` | Rebuilds the three `ipeds_cip110102` files from the NCES completions files. |
| `scripts/test_refresh_ipeds_cip.py` | Tests for the IPEDS counting rules. Run `python3 scripts/test_refresh_ipeds_cip.py`. |
| `scripts/refresh_grants_nsf.py`, `scripts/common.py` | Pulls AI-related NSF awards to community colleges as candidates for review. |
| `scripts/check_links.py` | Checks that every source link in the data still answers. |
| `CHANGELOG.md` | Dated history of the map's public builds. |
| `NEEDS-VERIFICATION.md` | Programs left off the map until their launch year is confirmed, and how to check them. |
| `package.json`, `package-lock.json` | The three npm packages used to draw and project the base map. |
| `.github/workflows/ci.yml` | The checks that run on every pull request. |
| `LICENSE`, `THIRD-PARTY-NOTICES.md` | The MIT license for this repo, and the terms of the third-party material in it. |

The pages are self-contained: fonts, styles, scripts, the base map and the data are all inside the HTML files.
They make no third-party requests and use no cookies, tracking or logins. A strict Content-Security-Policy is set
in the page.

## Run it locally

You only need Python 3.

```sh
python3 -m http.server 8000 --directory site
```

Then open http://localhost:8000/ for the map and http://localhost:8000/news/ for the news page.

## Run the checks

These are the checks CI runs. They need Python 3 and Node, and no packages.

```sh
python3 scripts/site_data.py check
python3 -m unittest discover -s scripts
node scripts/test_credential_filter.mjs
```

CI also scans the repo's history for secrets with [gitleaks](https://github.com/gitleaks/gitleaks).

## Data sources

- **IPEDS** (National Center for Education Statistics): college names, cities, states, types and locations
  (HD2024 directory file), plus program completions used in the growth table. Public domain.
- **College catalogs and program pages**: each AI program is listed only when a public catalog or official college
  page confirms it. The link is stored with the program.
- **Grant announcements**: official college pages, press releases, U.S. Department of Education and Department of
  Labor announcements, and the NSF Award Search API.
- **NAAIC's website** (naaic.ai): consortium membership, mentorship and partnership information.
- **Base map**: us-atlas v3 (ISC license), derived from U.S. Census Bureau cartographic boundary files (public domain).

## How the data is shaped

`data/naaic-map.json` has these main parts:

- `updated`: the date shown as the data date.
- `inst`: one entry per institution, keyed by IPEDS UNITID (`id`). `kind` decides where it appears:
  - `prog`: has at least one sourced AI program and gets a dot on the map.
  - `grant`: has a grant but no sourced program yet. It shows in the Grants tab, not as a dot.
  - `ep`: appears only as the other end of a partnership.
  
  Each entry has `programs`, `grants` (grant ids), `partners`, and `xy` (its position on the map).
- `grants`: the grants, with recipient, amount, funder, award date, purpose, `source_url` and `as_of`.
- `lines`: partnerships between two institutions (`a`, `b`), each with sourced `items`.
- `featured`: the "As featured in" tiles, each with `outlet`, `excerpt` (a headline or short excerpt from the article),
  `logo`, `source_url` (the article), `date` (when it ran) and `as_of`. The section stays hidden while this list is empty.
- `growth`, `growth_progs`, `ipeds`, `hcc`: the numbers behind the growth table and its sources.
- `states`: state outlines' bounding boxes for zooming.

## How to refresh

Updates are made by hand in reviewed batches. Nothing updates on its own.

1. **Gather candidates.**
   ```sh
   python3 scripts/refresh_ipeds.py          # IPEDS directory file into data/raw/
   python3 scripts/refresh_grants_nsf.py     # NSF award candidates into data/candidates/
   ```
   Add anything else you find (college announcements, catalog pages, NAAIC posts) to your own list of candidates.
2. **Check each candidate against its public source.** Only add an item when the source page says what the item
   says. Every item needs a `source_url` and an `as_of` date.
3. **Edit `data/naaic-map.json`.** For a college that is not in `inst` yet, get its IPEDS details and dot position:
   ```sh
   npm ci                                    # once, installs the base map packages
   python3 scripts/project_xy.py <UNITID> [<UNITID> ...]
   ```
   Use the printed `xy`, `city`, `state` and `geo_source` in the new entry. IPEDS can lag behind a college's
   current name (for example, IPEDS still lists Houston City College under its former name), so check the name.
   To add an "As featured in" tile, add an entry to `featured`. The page's security policy blocks outside images, so
   the logo goes inside the data as a `data:image/` address. Keep the file small, because every visitor downloads it:
   ```sh
   echo "data:image/png;base64,$(base64 -w0 logo.png)"
   ```
   Tiles show the newest first, and `date` can be `YYYY-MM-DD` or `YYYY-MM`. Logos sit on a white plate in both themes, so use a
   version that reads on white.
4. **Put the data back into the page and check it.**
   ```sh
   python3 scripts/site_data.py growth       # only if you changed growth_progs
   python3 scripts/refresh_ipeds_cip.py      # only to recheck NCES: rewrites data/ipeds_cip110102_*.csv
   python3 scripts/site_data.py ipeds        # after refresh_ipeds_cip.py, then embed: new downloads change "as of"
   python3 scripts/site_data.py embed
   python3 scripts/site_data.py check
   ```
   `check` stops on a missing source link or date, a dot with no program, a partnership line to an unknown
   college, a non-confirmed growth row, growth table counts that don't match the rows, a featured entry that is incomplete
   or has a logo that isn't embedded, or IPEDS rows that don't match the by-year CSV.
5. **Update the parts that are written by hand.**
   - The "Updated" date in the page header of `site/index.html` and `site/news/index.html`.
   - New grants in `site/feed.xml` (one `<item>` each, newest first) and its `lastBuildDate`.
   - New news items, and the item counts on the filter chips, in `site/news/index.html`.
6. **Check the links and look at the result.**
   ```sh
   python3 scripts/check_links.py
   python3 -m http.server 8000 --directory site
   ```
   Some college sites block scripted requests, so open any link that fails in a browser before removing it.

## How changes go live

1. A change goes on a branch and opens a pull request. CI runs on it.
2. A maintainer reviews the pull request and merges it once CI passes. Merging doesn't change the live map.
3. A maintainer publishes separately: lock a copy of `site/`, record its hash in `CHANGELOG.md` and a rollback point, compare
   screenshots, then upload it to the host.
4. To undo a publish, go back to the rollback point. To undo a change in the repo, revert its commit.

Publish only from a named commit on `main`, and confirm the `site/` hash matches that commit before uploading. Changes made
outside this repo reach the live map only through a pull request here.

Planning and team discussion happen in a private tracker. Automated tools open pull requests and never merge or publish.

## Hosting

Any static host works: upload the contents of `site/` as the web root. The canonical address in
`site/index.html`, `site/feed.xml`, `site/robots.txt` and `site/sitemap.xml` is currently
https://naaic-ai-map.vercel.app/. Change those if the site moves to a new address.

## License

MIT, see `LICENSE`. Third-party material keeps its own terms, listed in `THIRD-PARTY-NOTICES.md`.
