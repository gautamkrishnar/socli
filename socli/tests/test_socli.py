"""
Tests for socli
"""

import sys
import socli.socli as _socli
import socli.user as _user
import socli.search as _search

sys.path.append("..")


squery = "python for loop"
surl = "https://stackoverflow.com/questions/522563/accessing-the-index-in-for-loops?rq=1"

def test_wrongsyn():
    """ socli.wrongsyn() detects `"sdf"` as non-empty string """
    assert _socli.wrongsyn("sdf") == None

def test_fix_google_url():
    """ socli.fix_google_url() adds `https` protocol if not existent yet """
    url = _search.fix_google_url("www.example.com/questions/1234")
    assert url == "https://www.example.com/questions/1234"

def load_user_agents():
    _search.load_user_agents()

def test_parse_query():
    command = "python for loop".split()
    namespace = _socli.parse_arguments(command)

    assert not namespace.api
    assert namespace.browse == []
    assert not namespace.debug
    assert not namespace.delete
    assert not namespace.help
    assert not namespace.interactive
    assert not namespace.new
    assert namespace.query == []
    assert namespace.userQuery == "python for loop".split()
    assert not namespace.res
    assert not namespace.sosearch
    assert not namespace.tag
    assert not namespace.user
    assert not namespace.open_url

def test_parse_help():
    command = "-h".split()
    namespace = _socli.parse_arguments(command)

    assert not namespace.api
    assert namespace.browse == []
    assert not namespace.debug
    assert not namespace.delete
    assert namespace.help
    assert not namespace.interactive
    assert not namespace.new
    assert namespace.query == []
    assert not namespace.res
    assert not namespace.sosearch
    assert not namespace.tag
    assert not namespace.user
    assert not namespace.open_url

def test_parse_interactive():
    command = "-iq python for loop".split()
    namespace = _socli.parse_arguments(command)

    assert not namespace.api
    assert namespace.browse == []
    assert not namespace.debug
    assert not namespace.delete
    assert not namespace.help
    assert namespace.interactive
    assert not namespace.new
    assert namespace.query == "python for loop".split()
    assert not namespace.res
    assert not namespace.sosearch
    assert not namespace.tag
    assert not namespace.user
    assert not namespace.open_url

def test_parse_open_url():
    command = "--open-url https://stackoverflow.com/questions/20639180/explanation-of-how-nested-list-comprehension-works ".split()
    namespace = _socli.parse_arguments(command)

    assert not namespace.api
    assert namespace.browse == []
    assert not namespace.debug
    assert not namespace.delete
    assert not namespace.help
    assert not namespace.interactive
    assert not namespace.new
    assert namespace.query == []
    assert not namespace.res
    assert not namespace.sosearch
    assert not namespace.tag
    assert not namespace.user
    assert namespace.open_url!=[]

def test_user_json():
    try:
        _user.app_data = {"user": "John Smith"}
        _user.save_datafile()
        _user.load_datafile()
        _user.del_datafile()
    except Exception:
        raise SoCLITestingException("User JSON test failed.")

    try:
        name = "John Smith"
        _user.app_data = {"user": name}
        _user.save_datafile()
        user = _user.retrieve_saved_profile()
        assert user == name
        _user.del_datafile()
    except Exception:
        raise SoCLITestingException("User JSON test failed.")


def test_searchSO():
    try:
         _search.get_questions_for_query(squery)
    except Exception:
        raise SoCLITestingException("Search Stack Overflow test failed.")


def test_searchStats():
    try:
        _search.get_question_stats_and_answer(surl)
    except Exception:
        raise SoCLITestingException("Search SO stats test failed.")


class SoCLITestingException(Exception):

    def __init__(self, msg):
        super().__init__(msg)
