#!/usr/bin/env python3
"""Tests for the counting rules in refresh_ipeds_cip.py. Run from the repo root: python3 scripts/test_refresh_ipeds_cip.py"""
import unittest

from refresh_ipeds_cip import tally

UNIVERSITY = {"ICLEVEL": "1", "CONTROL": "2", "C21BASIC": "15", "STABBR": "PA"}
TWO_YEAR_PUBLIC = {"ICLEVEL": "2", "CONTROL": "1", "C21BASIC": "2", "STABBR": "AZ"}
BACC_GRANTING_PUBLIC = {"ICLEVEL": "1", "CONTROL": "1", "C21BASIC": "14", "STABBR": "TX"}
TWO_YEAR_FOR_PROFIT = {"ICLEVEL": "2", "CONTROL": "3", "C21BASIC": "8", "STABBR": "AZ"}


def row(unitid="1", major="1", level="7", total="10", cip="11.0102"):
    return {"UNITID": unitid, "CIPCODE": cip, "MAJORNUM": major, "AWLEVEL": level, "CTOTALT": total}


class TallyTest(unittest.TestCase):
    def test_total_counts_first_majors_in_the_ai_code_only(self):
        rows = [row(total="10"), row(major="2", total="3"), row(cip="11.0101", total="50")]
        result = tally({"c2024_a.csv": rows}, {"1": UNIVERSITY})
        self.assertEqual(result["total_completers"], 10)
        self.assertEqual(result["second_major_completers"], 3)

    def test_revised_file_replaces_the_original(self):
        files = {"c2022_a.csv": [row(total="711")], "c2022_a_rv.csv": [row(total="712")]}
        result = tally(files, {"1": UNIVERSITY})
        self.assertEqual(result["total_completers"], 712)
        self.assertEqual(result["release"], "final (revised)")

    def test_file_with_no_revised_copy_is_provisional(self):
        result = tally({"C2024_a.csv": [row()]}, {"1": UNIVERSITY})
        self.assertEqual(result["release"], "provisional")

    def test_a_zero_row_counts_as_reporting_but_not_as_having_completers(self):
        rows = [row("1", total="5"), row("2", total="0"), row("3", major="2", total="1")]
        result = tally({"c2024_a.csv": rows}, {u: UNIVERSITY for u in "123"})
        self.assertEqual(result["institutions_reporting"], 3)
        self.assertEqual(result["institutions_with_completers"], 1)

    def test_community_colleges_include_bacc_granting_publics_but_not_universities_or_private_colleges(self):
        directory = {"1": UNIVERSITY, "2": TWO_YEAR_PUBLIC, "3": BACC_GRANTING_PUBLIC, "4": TWO_YEAR_FOR_PROFIT}
        rows = [row("1", total="100"), row("2", level="3", total="7"), row("3", level="3", total="12"),
                row("4", level="3", total="40"), row("2", level="21", major="2", total="1")]
        result = tally({"c2024_a.csv": rows}, directory)
        self.assertEqual(result["community_college_completers"], 19)
        self.assertEqual(result["community_college_institutions_reporting"], 2)
        self.assertEqual(result["community_college_institutions_with_completers"], 2)

    def test_two_year_count_uses_the_ipeds_level_alone(self):
        directory = {"2": TWO_YEAR_PUBLIC, "3": BACC_GRANTING_PUBLIC, "4": TWO_YEAR_FOR_PROFIT}
        result = tally({"c2024_a.csv": [row(u) for u in directory]}, directory)
        self.assertEqual(result["two_year_institutions_reporting"], 2)

    def test_texas_count_uses_the_directory_state(self):
        directory = {"1": UNIVERSITY, "3": BACC_GRANTING_PUBLIC}
        result = tally({"c2024_a.csv": [row(u) for u in directory]}, directory)
        self.assertEqual(result["texas_institutions_reporting"], 1)

    def test_award_levels_merge_padded_and_unpadded_codes_and_split_out_community_colleges(self):
        directory = {"1": UNIVERSITY, "2": TWO_YEAR_PUBLIC}
        rows = [row("1", level="07", total="30"), row("1", level="7", total="2"), row("2", level="03", total="4"),
                row("1", level="3", total="1"), row("1", level="5", major="2", total="9")]
        result = tally({"c2024_a.csv": rows}, directory)
        self.assertEqual(result["levels"], {3: (5, 4), 7: (32, 0)})

    def test_an_award_level_with_no_known_label_stops_the_run(self):
        with self.assertRaises(KeyError):
            tally({"c2024_a.csv": [row(level="15")]}, {"1": UNIVERSITY})

    def test_college_rows_list_first_majors_at_community_colleges_including_zeros(self):
        directory = {"1": UNIVERSITY, "2": TWO_YEAR_PUBLIC}
        rows = [row("1"), row("2", level="03", total="4"), row("2", level="21", total="0"), row("2", level="21", major="2", total="1")]
        result = tally({"c2024_a.csv": rows}, directory)
        self.assertEqual(result["colleges"], [("2", 3, 4), ("2", 21, 0)])


if __name__ == "__main__":
    unittest.main()
