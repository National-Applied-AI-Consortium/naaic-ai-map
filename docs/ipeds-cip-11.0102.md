# IPEDS completions for CIP 11.0102

What the IPEDS row in the growth table counts, whether it is right, and how old the code is. Checked against NCES on
Nov 4, 2026. To rebuild the figures, run `python3 scripts/refresh_ipeds_cip.py`.

## Plain answer for the reviewer

The numbers were right. All six published figures match the NCES completions files exactly, so none changed.

They looked high because the row is not about community colleges. It counts every college and university that reports
to IPEDS, at every award level. In 2023-24, 1,122 of the 1,616 completions were master's degrees, and Carnegie Mellon alone
reported 227. Community colleges reported 63, about 4%.

The code is not new either. NCES added it in the 2000 edition of the CIP, so the rise since 2019-20 does not come from a new
code or a changed definition.

## What the row counts

- **Institutions:** all that report to IPEDS: public and private, two-year and four-year.
- **Award levels:** all, from certificates to doctorates.
- **Majors:** first majors only (`MAJORNUM` 1). Second majors are left out and are listed in their own column.
- **Unit:** awards conferred (`CTOTALT`), so a person with two awards counts twice.
- **Year:** July 1 to June 30. The value sits under the year the award year ends.
- **File:** the revised copy inside each NCES zip when there is one. C2024_A has none. Its awards were collected in the
  2024-25 collection year, which NCES still lists as [provisional](https://nces.ed.gov/ipeds/use-the-data/download-access-database).
  C2025_A is not published yet.

| Award year | Release | Published | Rebuilt | Master's | Institutions reporting | With completers | Community colleges |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2018-19 | final (revised) | 325 | 325 | 260 | 22 | 15 | 0 |
| 2019-20 | final (revised) | 389 | 389 | 296 | 33 | 23 | 2 |
| 2020-21 | final (revised) | 517 | 517 | 397 | 56 | 35 | 3 |
| 2021-22 | final (revised) | 712 | 712 | 485 | 74 | 55 | 5 |
| 2022-23 | final (revised) | 1,264 | 1,264 | 935 | 92 | 68 | 23 |
| 2023-24 | provisional | 1,616 | 1,616 | 1,122 | 125 | 86 | 63 |

The other columns in the by-year CSV also rebuild exactly. Institution counts include colleges that
filed a row with zero completers.

## Community college figures

These are in the data files and not on the site, so the team can choose which to show.

| File | What it has |
| --- | --- |
| `data/ipeds_cip110102_by_year.csv` | Yearly totals, with community college columns next to the published figure. |
| `data/ipeds_cip110102_by_award_level.csv` | Each year by award level, for all institutions and for community colleges. |
| `data/ipeds_cip110102_community_colleges.csv` | Each community college, year and award level, including zero rows. |

A community college here is public, and either two-year in IPEDS (`ICLEVEL` 2) or in a Carnegie 2021 class listed in
`CC_CARNEGIE` in `scripts/refresh_ipeds.py`. The [HD2024 directory](https://nces.ed.gov/ipeds/datacenter/data/HD2024.zip)
classifies every year, so a college stays in one group.

The two-year count alone is too narrow. IPEDS lists Houston Community College and Miami Dade College as four-year because
they also grant bachelor's degrees. By `ICLEVEL` alone, 2023-24 would show 33 completions instead of 63.

Treat the community college figure as a floor for AI teaching. In 2023-24, 15 community colleges filed under this code and
7 had completers. Only 10 of the 94 colleges on the map filed under it. New programs may have no completers yet, and a
college may report its AI program under another code. Other codes were not checked.

## History of the code

| Edition | What happened to 11.0102 | NCES source |
| --- | --- | --- |
| CIP 1990 | Not in the list. | [CIP 1990, series 11](https://nces.ed.gov/pubs2002/cip2000/ciplist90.asp?CIP2=11) |
| CIP 2000 | **Established** and marked new, as "Artificial Intelligence and Robotics". | [CIP 2000, series 11](https://nces.ed.gov/pubs2002/cip2000/ciplist.asp?CIP2=11), [full edition (PDF)](https://nces.ed.gov/pubs2002/2002165.pdf) |
| CIP 2010 | Retitled "Artificial Intelligence". Robot design left the definition, "motor control and motions by computer-driven machinery" became computer modeling of motor control and motion, and robotics got its own new code, 14.4201. NCES marks this "no substantive changes", with a text change. | [Crosswalk 2000 to 2010](https://nces.ed.gov/ipeds/cipcode/Files/Crosswalk2000to2010.csv), [CIP 2010 list](https://nces.ed.gov/ipeds/cipcode/Files/CIPCode2010.csv) |
| CIP 2020 | No substantive change and no text change. This is the current edition. | [Crosswalk 2010 to 2020](https://nces.ed.gov/ipeds/cipcode/Files/Crosswalk2010to2020.csv), [CIP 2020 entry](https://nces.ed.gov/ipeds/cipcode/cipdetail.aspx?y=56&cip=11.0102) |

The code first appears in IPEDS completions in the 2002-03 file,
[C2003_A](https://nces.ed.gov/ipeds/datacenter/data/C2003_A.zip), with rows from Carnegie Mellon only. The 2001-02 file,
[C2002_A](https://nces.ed.gov/ipeds/datacenter/data/C2002_A.zip), has none.

Every year in the growth table falls after the 2010 change, so the definition is the same across the row.
