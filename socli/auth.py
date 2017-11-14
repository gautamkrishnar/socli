import os

from getpass import getpass
from requests import Session

# Supporting input in Python 2/3
try:
    input = raw_input
except NameError:
    pass

# Supporting LWPCookieJar in Python 2/3
try:
    from http.cookiejar import LWPCookieJar
except ImportError:
    from cookielib import LWPCookieJar

COOKIES_FILE_PATH = '.cookies'
BASE_URL = 'https://stackoverflow.com/'
LOGIN_URL = BASE_URL + 'users/login'


def get_session():
    """
    :desc: Builds session from the saved cookies, if present.
           Otherwise, a new session is created.
    :return: requests.Session object
    """

    session = Session()

    if os.path.exists(COOKIES_FILE_PATH):
        session.cookies = LWPCookieJar(filename=COOKIES_FILE_PATH)
        session.cookies.load(ignore_discard=True, ignore_expires=True)

    return session


def login_prompt():
    """
    :desc: Prompts the user to enter email and password
    :return: (email, password)
    """

    email = input('Email: ')
    password = getpass()

    return (email, password)


def login(email, password):
    """
    :desc: Logs a user in.
    :param: email - Email of the user - required
            password - Password of the user - required
    :return: `dict`
    """

    if email == '' or password == '':
        return {'error': 'Email/Password field left blank.'}

    resp = {}
    data = {'email': email, 'password': password}
    session = get_session()
    session.cookies = LWPCookieJar(filename=COOKIES_FILE_PATH)

    resp_obj = session.post(LOGIN_URL, data=data)

    if resp_obj.status_code == 200:
        if resp_obj.url == BASE_URL:
            session.cookies.save(ignore_expires=True, ignore_discard=True)
            resp['error'] = None
        else:
            resp['error'] = 'Incorrect credentials'
    else:
        resp['error'] = 'Stackoverflow is probably down. Please try again.'

    return resp

