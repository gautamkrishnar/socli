"""
Contains all functions used for socli authentication
"""
import os

from functools import wraps
from getpass import getpass

from bs4 import BeautifulSoup
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
LOGOUT_URL = BASE_URL + 'users/logout'


def login_required(func):
    """
    :desc: decorator method to check user's login status
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        :desc: Wrapper to check if user is logged in, if the
               stored cookies contain cookie named `acct`
               and is not expired.
        """

        is_login = False
        resp = {'success': False, 'message': 'You are not logged in!'}

        if os.path.exists(COOKIES_FILE_PATH):
            cookiejar = LWPCookieJar(filename=COOKIES_FILE_PATH)
            cookiejar.load()

            for cookie in cookiejar:
                if cookie.name == 'acct':
                    expiry_time_obj = datetime.utcfromtimestamp(cookie.expires)

                    if datetime.now() > expiry_time_obj:
                        is_login = True

            if not is_login:
                os.remove(COOKIES_FILE_PATH)
            else:
                return func(*args, **kwargs)

        return resp

    return wrapper


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
        return {'success': False, 'message': 'Email/Password field left blank.'}

    resp = {'success': False}
    data = {'email': email, 'password': password}
    session = get_session()
    session.cookies = LWPCookieJar(filename=COOKIES_FILE_PATH)

    resp_obj = session.post(LOGIN_URL, data=data)

    if resp_obj.status_code == 200:
        if resp_obj.url == BASE_URL:
            session.cookies.save(ignore_expires=True, ignore_discard=True)
            resp['success'] = True
            resp['message'] = 'Successfully Logged In!'
        else:
            resp['message'] = 'Incorrect credentials'
    else:
        resp['message'] = 'Stackoverflow is probably down. Please try again.'

    return resp


@login_required
def logout():
    """
    :desc: Logout a user. Deletes the cookies.
    """

    session = get_session()
    logout_page_resp = session.get(LOGOUT_URL)
    resp = {'success': False}

    soup = BeautifulSoup(logout_page_resp.content, 'html.parser')
    fkey_input = soup.find('input', attrs={'name': 'fkey'})

    if fkey_input:
        data = {'fkey': fkey_input['value']}
        resp_obj = session.post(LOGOUT_URL, data=data)

        if resp_obj.url == BASE_URL:
            if os.path.exists(COOKIES_FILE_PATH):
                os.remove(COOKIES_FILE_PATH)

            resp['success'] = True
            resp['message'] = 'Successfully Logged Out!'
        else:
            resp['message'] = 'There were some problems. Please try again!'
    else:
        resp['message'] = 'There were some problems. Please try again!'

    return resp

