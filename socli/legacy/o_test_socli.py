# Test for socli.socli
# ~~~~~~~~~~~~~~~~~~~~


import o_socli as _socli


def test_wrongsyn():
    """ socli.wrongsyn() detects `"sdf"` as non-empty string """
    assert _socli.wrongsyn("sdf") is None


def test_fixGoogleURL():
    """ socli.fixGoogleURL() adds `https` protocol if not existent yet """
    url = _socli.fix_google_url("www.example.com/questions/1234")
    assert url == "https://www.example.com/questions/1234"
