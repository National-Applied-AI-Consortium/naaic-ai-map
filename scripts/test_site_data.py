#!/usr/bin/env python3
"""Tests for the data check in site_data.py. Run from the repo root: python3 scripts/test_site_data.py"""
import unittest

from site_data import featured_problems

LOGO = "data:image/png;base64,iVBORw0KGgo="


def entry(**changes):
    e = {"outlet": "Sample Outlet", "excerpt": "A short excerpt.", "logo": LOGO,
         "source_url": "https://example.com/article", "date": "2026-10-15", "as_of": "2026-11-04"}
    e.update(changes)
    return {k: v for k, v in e.items() if v is not None}


class FeaturedEntries(unittest.TestCase):
    def test_entry_without_a_link_is_a_problem(self):
        problems = featured_problems([entry(source_url=None)])
        self.assertEqual(len(problems), 1)
        self.assertIn("source_url", problems[0])
        self.assertIn("Sample Outlet", problems[0])

    def test_entry_without_a_date_is_a_problem(self):
        problems = featured_problems([entry(date=None)])
        self.assertEqual(len(problems), 1)
        self.assertIn("date", problems[0])

    def test_date_the_page_cannot_show_is_a_problem(self):
        self.assertEqual(len(featured_problems([entry(date="October 2026")])), 1)
        self.assertEqual(len(featured_problems([entry(date="2026-13-45")])), 1)

    def test_month_only_date_is_fine(self):
        self.assertEqual(featured_problems([entry(date="2026-10")]), [])

    def test_entry_without_as_of_is_a_problem(self):
        problems = featured_problems([entry(as_of=None)])
        self.assertEqual(len(problems), 1)
        self.assertIn("as_of", problems[0])

    def test_logo_on_another_site_is_a_problem(self):
        problems = featured_problems([entry(logo="https://example.com/logo.png")])
        self.assertEqual(len(problems), 1)
        self.assertIn("logo", problems[0])

    def test_entry_without_a_logo_is_a_problem(self):
        self.assertEqual(len(featured_problems([entry(logo=None)])), 1)

    def test_logo_with_no_image_data_is_a_problem(self):
        self.assertEqual(len(featured_problems([entry(logo="data:image/")])), 1)

    def test_entry_without_an_outlet_or_excerpt_is_a_problem(self):
        self.assertEqual(len(featured_problems([entry(outlet=None)])), 1)
        self.assertEqual(len(featured_problems([entry(excerpt=None)])), 1)

    def test_complete_entry_and_no_entries_are_fine(self):
        self.assertEqual(featured_problems([entry()]), [])
        self.assertEqual(featured_problems([]), [])


if __name__ == "__main__":
    unittest.main()
