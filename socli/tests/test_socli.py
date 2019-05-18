"""
Tests for socli
"""

import unittest
import sys
import socli.socli as _socli
import socli.user as _user
import socli.search as _search

sys.path.append("..")


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

    def setUp(self):
        _search.load_user_agents()

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

    def test04_userJSON(self):
        try:
            _user.app_data = {"user": "John Smith"}
            _user.save_datafile()
            _user.load_datafile()
            _user.del_datafile()
        except Exception:
            raise SoCLITestingException("User JSON test failed.")

    def test05_userJSON(self):
        try:
            name = "John Smith"
            _user.app_data = {"user": name}
            _user.save_datafile()
            user = _user.retrieve_saved_profile()
            self.assertEqual(user, name)

            _user.del_datafile()
        except Exception:
            raise SoCLITestingException("User JSON test failed.")

    def test06_searchSO(self):
        try:
            _search.get_questions_for_query(self.squery)
        except Exception:
            raise SoCLITestingException("Search Stack Overflow test failed.")

    # def test07_searchGoogle(self):
    #     try:
    #         _search.get_questions_for_query_google(self.squery)
    #     except Exception:
    #         raise SoCLITestingException("Search Google test failed.")

    def test07_searchStats(self):
        try:
            _search.get_question_stats_and_answer(self.surl)
        except Exception:
            raise SoCLITestingException("Search SO stats test failed.")


class SoCLITestingException(Exception):

    def __init__(self, msg):
        super().__init__(msg)


if __name__ == "__main__":
    unittest.main()
