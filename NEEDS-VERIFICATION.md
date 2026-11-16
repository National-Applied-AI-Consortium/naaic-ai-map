# Programs that need verification

From build 58c81b71 (Nov 2, 2026) the public map left out any AI program whose **launch year** had not been
confirmed from a public source. That hid 26 program rows. Since Nov 16, 2026, a program with an unknown launch year
is back on the map once its official program page shows the college offers it. It shows no launch year and is
counted in the note under the growth table.

A check of each program page on Nov 13, 2026 confirmed 19 of the 26 rows, and they are back on the map. The 7 rows
below are still off. None of them are in `data/naaic-map.json` or `site/index.html`.

## Still off the map (7 rows)

| # | College | Program | Why it is still off | Program source |
|---|---|---|---|---|
| 1 | Northwest Vista College, San Antonio, TX | Data Science and Artificial Intelligence A.A.S. | Not confirmed in the Nov 13 check. The college's AI Specialist award is back on the map. | https://mynvccatalog.alamo.edu/preview_program.php?catoid=295&poid=56781 |
| 2 | Ocean County College, Toms River, NJ | Artificial Intelligence Certificate | The Nov 13 check found that the Computer Science AS page no longer lists an AI option. | https://www.ocean.edu/area-of-study/artificial-intelligence-al |
| 3 | Mississippi Gulf Coast Community College, Perkinston, MS | Artificial Intelligence and Data Technology | The Nov 13 check found only the college's noncredit AI courses. | https://catalog.mgccc.edu/preview_program.php?catoid=32&poid=6174&returnto=3166 |
| 4 | UCNJ Union College of Union County, New Jersey, Cranford, NJ | Artificial Intelligence | Not in the Nov 13 check. | http://onlinecatalog.ucc.edu/preview_program.php?catoid=13&poid=1810 |
| 5 | Daytona State College, Daytona Beach, FL | Artificial Intelligence and Data Analytics (ATC) | Not in the Nov 13 check. The college's AS is on the map. | https://www.daytonastate.edu/academic-departments/college-of-business-engineering-and-technology/school-of-computer-science/ai-data-analytics-atc.html |
| | | Artificial Intelligence Awareness | Not in the Nov 13 check. | https://www.daytonastate.edu/academic-departments/college-of-business-engineering-and-technology/school-of-computer-science/ai-awareness-as-certificate.html |
| 6 | Texas Tech University, Lubbock, TX | Online Bachelor of Science in Human-Centered Artificial Intelligence | A university, so never a map dot. Its row only counted toward the growth table. | https://www.depts.ttu.edu/online/programs/bachelors/human-centered-ai/ |

## Left off the map by decision (not a data problem)

- **Bridgerland Technical College**, Logan, UT, is a less-than-2-year technical college. It is kept off the map by
  decision, not because its evidence is weak. It is still named in one public news item: the EDC "AI Across
  Careers" item on the News page (`site/news/index.html`) lists it among the five partner colleges, because EDC's
  own announcement names it. That mention is accurate to the source and was left in.

## Taken off because the program has not launched (3)

Checked Nov 4, 2026 (`naaic-ai-map-planning#1`). These programs were on the map as announced, approved or upcoming.

| College | Program | Status on the map | What the source says | Source |
|---|---|---|---|---|
| County College of Morris, Randolph, NJ | Certificate in AI & Data Science (registered apprenticeship) | Announced | Applications closed Nov 2, 2026. GovTech reports a January 2027 start. | https://www.ccm.edu/news/applications-are-open-for-ccms-ai-data-science-apprenticeship/ and https://www.govtech.com/education/higher-ed/new-jersey-community-colleges-offer-hands-on-data-science-ai-training |
| Casper College, Casper, WY | Artificial Intelligence Certificate | Launching fall 2027 | Starts in the fall 2027 semester. | https://caspercollege.edu/news/2026/10/artificial-intelligence-certificate/ |
| El Camino Community College District, Torrance, CA | AI Practitioner Certificate of Achievement | Approved | A NAAIC post says it was developed and approved, with no start term. No college source found yet. | https://www.naaic.ai/post/from-mentorship-to-momentum-a-look-at-naaics-2025-2026-institutional-mentorship-program |

County College of Morris stays in the Grants tab. El Camino stays as the other end of a partnership line.

## Announced, never on the map (1)

Checked Nov 5, 2026. This program stays off the map until a catalog entry or approved program shows its award type and units.

| College | Program | What the source says | Source |
|---|---|---|---|
| Moorpark College, Moorpark, CA | Applied Artificial Intelligence certificate | A $3,000,000 grant "will fund" the certificate. No start term, units or award type. Not in the 2026-27 catalog's program list. | https://www.moorparkcollege.edu/news/3-million-federal-grant-brings-applied-ai-training-moorpark-college-students |

Moorpark College stays in the Grants tab.

## How to verify a row and add it back

1. Open the program source above and confirm the college offers the program now, under that name. An approval, an
   announcement or a news story is not enough.
2. Add the program to the college's `programs` list in `data/naaic-map.json`, with `status: "offered"`, the program
   page as `source_url`, and `as_of`. For a college that left the map, set its `kind` back to `prog`.
3. If a public source gives the **first year the program was offered** (the earliest catalog that lists it, a class
   schedule or college page naming the first term, or an official announcement that it started enrolling), also add
   a growth row (`growth_progs`, with `conf: "high"`, `fy`, `fy_src` and `as_of`). Without one, the program shows no
   launch year.
4. Run `python3 scripts/site_data.py growth` (updates the growth table counts and its note), then
   `python3 scripts/site_data.py embed` and `python3 scripts/site_data.py check`, and look at the map locally.
5. Remove the row from this file.
