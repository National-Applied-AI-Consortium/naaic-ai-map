# NAAIC AI programs map

Public map answering "Who is teaching AI today?" at U.S. community colleges. Reliability outranks coverage: leave a program off until its evidence holds.

## What may be published

Some existing rows still break these rules; the cleanup is tracked in the issue tracker.

- The map lists launched credentials: certificates, associate degrees, bachelor's degrees and AI tracks. A group of courses counts only when the college awards it as a credential.
- A launch rests on an official program or credential source. Announced, approved or unconfirmed programs wait in `NEEDS-VERIFICATION.md`.
- Every item has a `source_url` that says what the item says, and an `as_of` date.
- Personal contact details stay out of the repo (`PERSONAL` in `scripts/common.py`).
- Pages stay self-contained: fonts, images and scripts live inside the HTML. The Content-Security-Policy blocks everything else.

## Changing the data

Read "How to refresh" in `README.md` first. Edit `data/naaic-map.json`; `scripts/site_data.py embed` copies it onto the single `const D={` line in `site/index.html`.

`check` skips the hand-written parts, so confirm these yourself: the "Updated" dates, `site/feed.xml` and the news filter counts.

Record edits that are not live yet under `## Unreleased` in `CHANGELOG.md`. Each public build gets an entry named by its hash (the command is at the top of that file), and the "`site/` folder is build" line moves to the new hash.

## Publishing

`site/` is the source of truth and is served exactly as it stands, so edit it directly.

Merging leaves the live map unchanged. Publishing is a separate manual step: a maintainer locks a copy of `site/`, records its fingerprint and a rollback point, takes screenshots, and uploads it to the host. Agents never merge or deploy.

## This repo is public

Code, data and pull requests live here. Planning lives in the private `National-Applied-AI-Consortium/naaic-ai-map-planning` repo.

- Pull request text, commit messages and code comments are public. Keep people's names, meeting notes, hosting accounts and budget details in the private issues.
- Link an issue as `National-Applied-AI-Consortium/naaic-ai-map-planning#24`, outside backticks, and describe the change in the pull request itself, because readers without access can't open the issue.
- CI runs `site_data.py check`, the tests and gitleaks on every pull request. Don't merge on a failure.

## Searching the site

`site/index.html` has single lines of 50-170 KB (embedded fonts, data). Trim search output: `grep -n PATTERN site/index.html | cut -c1-300`.

## Agent skills

### Issue tracker

Issues live in the private `National-Applied-AI-Consortium/naaic-ai-map-planning` repo, using the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Default label names. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context. See `docs/agents/domain.md`.
