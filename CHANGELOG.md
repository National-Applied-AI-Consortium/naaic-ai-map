# Changelog

Public builds of the map at https://naaic-ai-map.vercel.app/, newest first. Each build is named by the first
8 characters of its content hash. The hash is the SHA-256 of the sorted list of file hashes, run inside the
build folder:

```sh
cd site && find . -type f -print0 | LC_ALL=C sort -z | xargs -0 sha256sum | sha256sum
```

The `site/` folder in this repo is build f48edf6b, which is the live build.

## Unreleased (in the repo, not yet live)

- Map: Atlantic Cape Community College came off because nothing shows its AI & Machine Learning option has started.
  It stays in the Grants tab. The map now shows **93 colleges and 144 programs** (was 94 and 145), and the growth
  table's 2026 count is 64 (was 65). See NEEDS-VERIFICATION.md.
- Map page: "Updated" moves to Nov 9, 2026.
- Data check: `site_data.py check` now stops on a program whose status isn't "offered", so an announced or
  upcoming program can't reach the map. Nothing in `site/` changes.

## Nov 5, 2026

### f48edf6b: credential filter, 3 colleges off the map, confirmed programs (current)
- Map page: a credential filter shows colleges with a certificate, associate degree or bachelor's degree, including when it
  isn't their highest credential. It works with the state view and year slider, using each matching program's own start year.
  The map, college list and counts follow it, and a college's details mark which programs match. All dots take the selected
  credential's color while it is on. The growth table doesn't change.
- News: the EDC "AI Across Careers" item no longer names Bridgerland Technical College, which is kept off the map.
  Its headline now reads "EDC and community colleges launch NSF-funded AI Across Careers" and it lists Green River,
  Bunker Hill, Nashville State and Harford.
- Map: County College of Morris, Casper College and El Camino came off because their programs have not launched. The map
  now shows **94 colleges and 145 programs** (was 97 and 148). See NEEDS-VERIFICATION.md.
- De Anza's Applied AI degree and certificate now show as offered, based on its program page and Fall 2026 class listing.
- Blinn's two AI degrees now show as offered. Its Fall 2026 schedule lists ITAI 1370, a first-semester course in both degree plans.
- Map page: an "As featured in" section is ready for the first feature. It stays hidden until `featured` in the data has
  an entry, so nothing changes on the page yet. `site_data.py check` stops on an incomplete entry or a logo that isn't embedded.
- Growth table: the IPEDS row now says what it counts: first majors at all colleges and universities, at every award
  level, mostly master's degrees. All six figures were rebuilt from the NCES files and match, so none changed; their "as of"
  date moves to Nov 4, 2026. Community college figures are in `data/` and not on the site. See `docs/ipeds-cip-11.0102.md`.
- The note under the growth table now shows 82 programs with no sourced launch year. It showed 89, which didn't match the
  data, and `site_data.py` now calculates and checks it.

## Nov 3, 2026

### e49c218b: new grants, news and one new college
- County College of Morris (NJ) is added to the map with its Certificate in AI & Data Science (status: announced, no
  launch year yet). The map now shows **97 colleges and 148 programs** (was 96 and 147).
- Two new grants: Johnston Community College ($150,000 from the Gates Foundation, Oct 2026) and Fullerton College
  ($3,000,000 Title III Strengthening Institutions Program, no award date given). Both are in the Grants tab and the RSS feed.
- Bunker Hill, Nashville State, Green River and Harford community colleges are listed as partner colleges in EDC's
  "AI Across Careers" NSF project. They appear as partners, not as map dots, unless they also have an AI program.
- News page: 4 new October items (NAAIC turns two, Fullerton, County College of Morris, Johnston). 24 items in total.
- Month-only grant dates now show as "Oct 2026" instead of "Invalid Date".
- College type labels: less-than-2-year technical colleges and bachelor's-granting community colleges get their own
  labels. No existing label changed.

### 3e8ecec0: hover box and college details popup
- Hovering a single dot on a computer shows a small dark box with the college name and its highest credential.
  Clicking the dot opens its details.
- College details now open in one dark popup everywhere (map dots, lists, the full list below the map, Grants cards
  and partner links), with sections for Programs, Grants and Partners and a link to the college on College Navigator.
  A back arrow returns to the list you came from.
- On phones, the details dock at the bottom of the screen and the map scrolls so the dot stays visible.
- Long college names in lists wrap onto two lines instead of being cut off.

## Nov 2, 2026

### a2c82bd5: popup list and simpler dots
- "Location: IPEDS" now opens the college's page on College Navigator instead of downloading the IPEDS data file.
- Every dot is a solid fill in its credential color. The teal "new this year" ring, the hollow dots and their two
  legend rows are gone.
- The counter reads "96 colleges on the map" for 2026. Earlier years read "N colleges with a sourced AI program by YEAR".
- Tapping or hovering where several dots overlap opens a compact dark "N colleges here" list.
- Visible keyboard focus ring fixed.

### 62353ad9: smaller dots, spread apart (first public build with the 58c81b71 fixes)
- Dots are about 60% of their old size, and dots that overlap in a metro area are pushed apart until they just touch.
  Only the display moves; the stored locations do not change. The tap target grew to 44 px.
- The link under the legend fits on one line: "Full list of colleges and programs".
- Clearer legend labels.
- Also carries every change from 58c81b71 below, which was never published on its own.

### 58c81b71: quick fixes, programs needing confirmation taken off (built from f302afca)
- **Programs whose launch year still needs confirmation are hidden.** 26 program rows that rested only on news
  coverage, an approval date or a first-term mention were taken off the map, the college list and the growth table.
  14 colleges left the map (110 to 96 colleges, 172 to 147 programs). See NEEDS-VERIFICATION.md.
- Dot color shows the highest AI credential a college offers: certificate, associate degree or bachelor's degree.
- The legend and the About page explain the dotted partnership lines.
- The numbered "group of nearby colleges" bubbles are gone; every college is its own dot.
- The growth table has one "United States" row.
- A link under the legend jumps to the full list of colleges and programs.
- New About section, "How this map is updated": updates are not automatic, every addition is checked against its
  public source, and a person approves each version before it is published.

## Oct 31, 2026

### f302afca: accessibility and news batch
- Stronger color contrast for the focus ring, state labels, partnership lines and the "new" ring (all checked against
  WCAG ratios in light and dark mode).
- News page: teal accent instead of gold, keyboard-reachable source links, and its Grants and About links open
  those tabs on the map page.
- Larger tap areas on grant card links. Unused correction-form styles removed.
- The page heading is "AI in Community Colleges" on both pages.
- NAAIC mentorship lines read "NAAIC 2025-26 Institutional Mentorship cohort. NAAIC has mentored 16 colleges to date."
- NAAIC's reach figures updated from NAAIC's "NAAIC Turns 2" post. 20 news items.
- Replaced an earlier candidate of the same batch (5177cff6) that was never published.

## Oct 30, 2026

### 3d6fe451: menu order
- The top menu on both pages reads News, Map, Grants, About. Nothing else changed.

### a219cf1c: news page grows to 21 items
- 19 news items added, grouped by month, with filter chips for Programs, Grants, Partnerships, Policy and Events.
- The National AI Conference 2027 card is dated Oct 27, 2026.
- Houston City College's bachelor's degree start-year link was replaced (the old page no longer exists).
- News summaries are no longer cut to two lines, so nothing is clipped on narrow phones.

## Oct 29, 2026

### d1642c23: News page launched
- New page at /news/ with NAAIC news items (2 at launch: the National AI Conference 2027 at Houston City College and
  Community College Daily's story on NAAIC's free AI faculty training). A News tab links to it from the map.
- Added robots.txt and sitemap.xml.

## Oct 26, 2026

### 92aab814: October 26 data batch
- 6 colleges added: Rockland Community College (NY), Santa Fe College (FL), Moorpark College (CA) and Norco College
  (CA) for new grants; Casper College (WY) for its AI Certificate launching fall 2027; Henry Ford College (MI) as a
  partner of Grand Valley State University.
- 4 new grants, with the federal funder named the same way on every Title III grant.

## Oct 25, 2026

### 307722ac: two-way light and dark switch
- The theme button switches between light and dark with a single icon. With nothing chosen, the page follows the
  device setting.

### c8b473ac: dark mode and the October 19 data
- Dark mode that follows the device setting, plus a theme button in the header.
- "Tap a state to zoom" on phones; "Click a state to zoom" on computers.
- Data added on Oct 19 (first published here): 6 new programs, including Eastern West Virginia Community and Technical
  College's AI Certificate in Applied Science and its grant. 171 programs and 45 grants.
- St. Petersburg College's grant names its funder (Title III Strengthening Institutions Program).
- Internal notes that were hidden in the page source were removed, along with the inactive "Suggest a correction"
  buttons and placeholder About text. The RSS feed links point to the live address.
- Includes the unpublished Oct 19 to Oct 25 builds 1bfb47ad, 3b1a2046 and a2f1cf6b.

## Oct 8 to Oct 12, 2026

### First public versions
- The map went live at naaic-ai-map.vercel.app with AI programs, grants since Jan 1, 2024, and documented
  partnerships at community colleges, each linked to a public source. The Oct 12 version ("Updated Oct 12, 2026")
  listed 165 programs and 44 grants, with 108 colleges on the map. No build hashes were recorded for these versions.
