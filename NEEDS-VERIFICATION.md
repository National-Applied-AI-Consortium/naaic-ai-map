# Programs that need verification

Since build 58c81b71 (Nov 2, 2026; first published in 62353ad9), the public map leaves out any AI program whose
**launch year** has not been confirmed from a public source. These programs are real and each has a source page for
the program itself. What is missing is solid evidence of the year the program started: the year shown rested only on
news coverage, an approval date (board, state or curriculum), the first catalog year it appears in, or a first-term
mention.

In total, 26 program rows were hidden: 17 at the 14 colleges that left the map, 8 at 7 colleges that stay on the map,
and 1 at a university (Texas Tech) that was never a map dot. None of these rows are in `data/naaic-map.json` or
`site/index.html`. They are listed here so they can be checked and added back.

"Year shown" is the launch year the map used before the rows were hidden.

## Colleges taken off the map (14)

These colleges had no other confirmed AI program, so they left the map (110 colleges became 96).

| # | College | Program | Year shown | Why it needs confirmation | Program source |
|---|---|---|---|---|---|
| 1 | Northwest Vista College, San Antonio, TX | Data Science and Artificial Intelligence A.A.S. | 2026 | Only the first catalog year it appears in | https://mynvccatalog.alamo.edu/preview_program.php?catoid=295&poid=56781 |
| | | Artificial Intelligence Specialist Occupational Skills Award | 2026 | Only the first catalog year it appears in | https://mynvccatalog.alamo.edu/preview_program.php?catoid=295&poid=56772 |
| 2 | Estrella Mountain Community College, Avondale, AZ | Artificial Intelligence and Machine Learning (CCL 5897N) | 2020 | News coverage only | https://www.estrellamountain.edu/degrees-certificates/science-technology-engineering-and-mathematics/artificial-intelligence-and-machine-learning-5897n-ccl |
| 3 | Wayne Community College, Goldsboro, NC | Artificial Intelligence Engineer (AAS) | 2021 | Only the state approval year | https://www.waynecc.edu/programs/ai/ |
| 4 | Ocean County College, Toms River, NJ | Artificial Intelligence Certificate | 2021 | Only the board approval year | https://www.ocean.edu/area-of-study/artificial-intelligence-al |
| 5 | Rose State College, Midwest City, OK | Associate of Science in Artificial Intelligence/Machine Learning | 2024 | Only the state approval year | https://rose.edu/program/artificial-intelligence-machine-learning-technologies/ |
| 6 | Bristol Community College, Fall River, MA | Associate of Applied Science in Artificial Intelligence | 2025 | News coverage only | https://bristolcc.edu/AI |
| | | Artificial Intelligence Practitioner Certificate | 2025 | News coverage only | https://catalog.bristolcc.edu/applied-artificial-intelligence/artificial-intelligence-practitioner-certificate |
| 7 | Community College of Baltimore County, Baltimore, MD | Artificial Intelligence, Associate of Science | 2025 | News coverage only | https://www.ccbcmd.edu/Programs-and-Courses-Finder/Program/artificial-intelligence.html |
| 8 | Isothermal Community College, Spindale, NC | Applied Science degree in Artificial Intelligence | 2026 | News coverage only | https://www.naaic.ai/post/from-mentorship-to-momentum-a-look-at-naaics-2025-2026-institutional-mentorship-program |
| 9 | Seminole State College of Florida, Sanford, FL | Artificial Intelligence Awareness (ARTINT-CC) | 2025 | Only a first-term mention | https://www.seminolestate.edu/catalog/programs/artint-cc |
| 10 | Edmonds College, Lynnwood, WA | Robotics and Artificial Intelligence (AETRABAS) | 2024 | News coverage only | https://catalog.edmonds.edu/preview_program.php?catoid=68&poid=18091&print |
| 11 | Mississippi Gulf Coast Community College, Perkinston, MS | Artificial Intelligence and Data Technology | 2025 | Only a first-term mention | https://catalog.mgccc.edu/preview_program.php?catoid=32&poid=6174&returnto=3166 |
| 12 | UCNJ Union College of Union County, New Jersey, Cranford, NJ | Artificial Intelligence | 2025 | Only the board approval year | http://onlinecatalog.ucc.edu/preview_program.php?catoid=13&poid=1810 |
| 13 | College of Western Idaho, Nampa, ID | Artificial Intelligence and Cloud Computing (AICC.AAS) | 2024 | Only the curriculum approval year | https://catalog.cwi.edu/programs-study/artificial-intelligence/aicc-aas/ |
| 14 | Delaware County Community College, Media, PA | AI Foundations (AIF) | 2025 | Only a first-term mention | https://www.dccc.edu/ai-programs |
| | | AI Specialist (AIS) | 2025 | Only a first-term mention | https://www.dccc.edu/ai-programs |

## Colleges still on the map with some programs hidden (7)

These colleges stay on the map because they have at least one other confirmed AI program. Only the rows below are hidden.

| # | College | Hidden program | Year shown | Why it needs confirmation | Program source |
|---|---|---|---|---|---|
| 1 | Lone Star College System, The Woodlands, TX | Artificial Intelligence & Machine Learning | 2024 | News coverage only | https://www.lonestar.edu/programs-of-study/ai-machine-learning.htm |
| 2 | City Colleges of Chicago-Wilbur Wright College, Chicago, IL | Artificial Intelligence and Machine Learning Development, Advanced Certificate | 2026 | Only the board approval year | https://catalog.ccc.edu/academic-program-requirements/artificial-intelligence-machine-learning-development-advanced-certificate/ |
| 3 | Florida State College at Jacksonville, Jacksonville, FL | Artificial Intelligence (AI) Practitioner (T.C.) | 2026 | Only the board approval year | https://www.fscj.edu/program?pCode=6118 |
| 4 | Bellevue College, Bellevue, WA | Software Development, BAS, Artificial Intelligence Concentration | 2022 | News coverage only | https://www.bellevuecollege.edu/academics/undergraduate-programs/software-development-artificial-intelligence-concentration-bas |
| 5 | Daytona State College, Daytona Beach, FL | Artificial Intelligence and Data Analytics | 2026 | Only the board approval year | https://www.daytonastate.edu/academic-departments/college-of-business-engineering-and-technology/school-of-computer-science/ai-data-analytics-atc.html |
| | | Artificial Intelligence Awareness | 2026 | Only the board approval year | https://www.daytonastate.edu/academic-departments/college-of-business-engineering-and-technology/school-of-computer-science/ai-awareness-as-certificate.html |
| 6 | Pensacola State College, Pensacola, FL | Artificial Intelligence Practitioner | 2026 | Only the board approval year | https://catalog.pensacolastate.edu/preview_program.php?catoid=2&poid=933&returnto=55 |
| 7 | College of DuPage, Glen Ellyn, IL | Machine Learning (CIS.CER.MLRN) | 2025 | News coverage only | https://catalog.cod.edu/programs-study/computer-information-science/machine-learning-certificate |

## Also hidden, but never a map dot

- **Texas Tech University**, Lubbock, TX: Online Bachelor of Science in Human-Centered Artificial Intelligence (year
  shown 2025, launch news only). https://www.depts.ttu.edu/online/programs/bachelors/human-centered-ai/
  It is a university, so it was never one of the 110 college dots. Its row only counted toward the growth table.

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

1. Open the program source above and confirm the program is still offered (or announced) under that name.
2. Find a public source that gives the **first year the program was offered**: the earliest college catalog that
   lists it (checked against the catalog year before it, so it is the first listing and not only the newest catalog
   online), a class schedule or college page naming the first term students enrolled, or an official college
   announcement that it started enrolling. An approval date, a news story or a single current catalog is not enough.
3. Record that source and the year in the program's growth row (`growth_progs` in `data/naaic-map.json`, with
   `conf: "high"`, `fy`, `fy_src` and `as_of`), and add the program to the college's `programs` list. For a college
   that left the map, set its `kind` back to `prog`.
4. Run `python3 scripts/site_data.py growth` (updates the yearly counts in the growth table), then
   `python3 scripts/site_data.py embed` and `python3 scripts/site_data.py check`, and look at the map locally.
5. Remove the row from this file.
