"""
Stack Overflow CLI (SoCLI)
Created by
Gautam Krishna R : www.github.com/gautamkrishnar

Tests 1 through to 17 designed and implemented by Liam Byrne (www.github.com/byrneliam2)

Tests for SoCLI
"""

import argparse
import unittest
import sys
sys.path.append("..")

import socli.socli as _socli
import socli.printer as _print
import socli.user as _user
import socli.search as _search

import legacy.o_socli as _osocli


class TestSoCLI(unittest.TestCase):

    squery = "python for loop"
    surl = "https://stackoverflow.com/questions/522563/accessing-the-index-in-for-loops?rq=1"

    def test_wrongsyn(self):
        """ socli.wrongsyn() detects `"sdf"` as non-empty string """
        self.assertEqual(_socli.wrongsyn("sdf"), None)

    def test_fixGoogleURL(self):
        """ socli.fixGoogleURL() adds `https` protocol if not existent yet """
        url = _search.fix_google_url("www.example.com/questions/1234")
        self.assertEqual(url, "https://www.example.com/questions/1234")

    # -------------------------------------------------------------------------

    def setUp(self):
        _search.load_user_agents()
        _osocli.loaduseragents()

    def test01_socliParse(self):
        command = "python for loop".split()
        namespace = _socli.parse_arguments(command)

        self.assertFalse(namespace.api)
        self.assertTrue(namespace.browse == [])
        self.assertFalse(namespace.debug)
        self.assertFalse(namespace.delete)
        self.assertFalse(namespace.help)
        self.assertFalse(namespace.interactive)
        self.assertFalse(namespace.new)
        self.assertTrue(namespace.query == [])
        self.assertFalse(namespace.res)
        self.assertFalse(namespace.sosearch)
        self.assertFalse(namespace.tag)
        self.assertFalse(namespace.user)

    def test02_socliParse(self):
        command = "-h".split()
        namespace = _socli.parse_arguments(command)

        self.assertFalse(namespace.api)
        self.assertTrue(namespace.browse == [])
        self.assertFalse(namespace.debug)
        self.assertFalse(namespace.delete)
        self.assertTrue(namespace.help)
        self.assertFalse(namespace.interactive)
        self.assertFalse(namespace.new)
        self.assertTrue(namespace.query == [])
        self.assertFalse(namespace.res)
        self.assertFalse(namespace.sosearch)
        self.assertFalse(namespace.tag)
        self.assertFalse(namespace.user)

    def test03_socliParse(self):
        command = "-iq python for loop".split()
        namespace = _socli.parse_arguments(command)

        self.assertFalse(namespace.api)
        self.assertTrue(namespace.browse == [])
        self.assertFalse(namespace.debug)
        self.assertFalse(namespace.delete)
        self.assertFalse(namespace.help)
        self.assertTrue(namespace.interactive)
        self.assertFalse(namespace.new)
        self.assertTrue(namespace.query == [x for x in command if (not x.startswith("-"))])
        self.assertFalse(namespace.res)
        self.assertFalse(namespace.sosearch)
        self.assertFalse(namespace.tag)
        self.assertFalse(namespace.user)

    @unittest.skip
    def test04_socliParse(self):
        command = "-q".split()
        try:
            _socli.parse_arguments(command)
        except (argparse.ArgumentError, SystemExit):
            pass

    # Check there has been no difference in formatting due to modularizing

    def test05_printFormat(self):
        self.assertEqual(repr(_print.make_header("Header")),
                         repr(_osocli.make_header("Header")))

    def test06_printFormat(self):
        self.assertEqual(repr(_print.make_blue("Blue")),
                         repr(_osocli.make_blue("Blue")))

    def test07_printFormat(self):
        self.assertEqual(repr(_print.make_green("Green")),
                         repr(_osocli.make_green("Green")))

    def test08_printFormat(self):
        self.assertEqual(repr(_print.make_warning("Warning")),
                         repr(_osocli.make_warning("Warning")))

    def test09_printFormat(self):
        self.assertEqual(repr(_print.make_fail("Fail")),
                         repr(_osocli.make_fail("Fail")))

    def test10_printFormat(self):
        self.assertEqual(repr(_print.make_white("White")),
                         repr(_osocli.make_white("White")))

    def test11_printFormat(self):
        self.assertEqual(repr(_print.bold("Bold")),
                         repr(_osocli.format_str("Bold", _osocli.bcolors.BOLD)))

    def test12_printFormat(self):
        self.assertEqual(repr(_print.underline("Underline")),
                         repr(_osocli.format_str("Underline", _osocli.bcolors.UNDERLINE)))

    def test13_userJSON(self):
        try:
            _user.app_data = {"user": "John Smith"}
            _user.save_datafile()
            _user.load_datafile()
            _user.del_datafile()
        except Exception:
            raise SoCLITestingException("User JSON test failed.")

    def test14_userJSON(self):
        try:
            name = "John Smith"
            _user.app_data = {"user": name}
            _user.save_datafile()
            user = _user.retrieve_saved_profile()
            self.assertEqual(user, name)

            _user.del_datafile()
        except Exception:
            raise SoCLITestingException("User JSON test failed.")

    def test15_searchSO(self):
        try:
            _search.get_questions_for_query(self.squery)
        except Exception:
            raise SoCLITestingException("Search Stack Overflow test failed.")

    def test16_searchGoogle(self):
        try:
            _search.get_questions_for_query_google(self.squery)
        except Exception:
            raise SoCLITestingException("Search Google test failed.")

    def test17_searchStats(self):
        try:
            _search.get_question_stats_and_answer(self.surl)
        except Exception:
            raise SoCLITestingException("Search SO stats test failed.")

    @unittest.skip
    def test18_searchSO(self):
        try:
            self.assertEqual(_search.get_questions_for_query(self.squery),
                             _osocli.get_questions_for_query(self.squery))
        except Exception:
            raise SoCLITestingException("Search Stack Overflow test failed.")

    @unittest.skip
    def test19_searchGoogle(self):
        try:
            self.assertEqual(_search.get_questions_for_query_google(self.squery),
                             _osocli.get_questions_for_query_google(self.squery))
        except Exception:
            raise SoCLITestingException("Search Google test failed.")

    @unittest.skip
    def test20_searchStats(self):
        try:
            self.assertEqual(_search.get_question_stats_and_answer(self.surl),
                             _osocli.get_question_stats_and_answer(self.surl))
        except Exception:
            raise SoCLITestingException("Search SO stats test failed.")


class SoCLITestingException(Exception):

    def __init__(self, msg):
        super().__init__(msg)


if __name__ == "__main__":
    unittest.main()
