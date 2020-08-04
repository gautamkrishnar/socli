"""
Contains all functions used for searching Stack Overflow and Google
"""

import os
import random
import re
import sys
import copy

from bs4 import BeautifulSoup
import requests
import urwid

import socli.printer
import socli.tui

uas = []  # User agent list
header = {}  # Request header
google_search = True
so_url = "http://stackoverflow.com"  # Site URL
so_qurl = "http://stackoverflow.com/search?q="  # Query URL
so_burl = "https://stackoverflow.com/?tab="  # Assuming browse URL
google_search_url = "https://www.google.com/search?q=site:www.stackoverflow.com+"  # Google search query URL


def get_questions_for_query(query, count=10):
    """
    Fetch questions for a query using Stack Overflow default search mechanism.
    Returned question urls are relative to SO homepage.
    At most 10 questions are returned. (Can be altered by passing count)
    :param query: User-entered query string
    :return: list of [ (question_text, question_description, question_url) ]
    """

    questions = []
    random_headers()

    search_res = requests.get(so_qurl + query, headers=header)
    captcha_check(search_res.url)
    soup = BeautifulSoup(search_res.text, 'html.parser')
    try:
        soup.find_all("div", class_="question-summary")[0]  # For explicitly raising exception
    except IndexError:
        socli.printer.print_warning("No results found...")
        sys.exit(0)
    tmp = (soup.find_all("div", class_="question-summary"))
    tmp1 = (soup.find_all("div", class_="excerpt"))
    i = 0
    while i < len(tmp) and i < count: # iterate over and limit results
        question_text = ' '.join((tmp[i].a.get_text()).split())
        question_text = question_text.replace("Q: ", "")
        question_desc = (tmp1[i].get_text()).replace("'\r\n", "")
        question_desc = ' '.join(question_desc.split())
        question_local_url = tmp[i].a.get("href")
        questions.append((question_text, question_desc, question_local_url))
        i += 1

    return questions


def get_questions_for_query_google(query, count=10):
    """
    Fetch questions for a query using Google search.
    Returned question urls are URLS to SO homepage.
    At most 10 questions are returned. (Can be altered by passing count)
    :param query: User-entered query string
    :return: list of [ (question_text, question_description, question_url) ]
    """
    i = 0
    questions = []
    random_headers()
    search_results = requests.get(google_search_url + query, headers=header)
    captcha_check(search_results.url)
    soup = BeautifulSoup(search_results.text, 'html.parser')
    try:
        soup.find_all("div", class_="g")[0]  # For explicitly raising exception
    except IndexError:
        socli.printer.print_warning("No results found...")
        sys.exit(0)
    for result in soup.find_all("div", class_="g"):
        if i == count:
            break
        try:
            question_title = result.find("div", class_="r").find("h3").get_text().replace(' - Stack Overflow', '')
            question_desc = result.find("span", class_="st").get_text()
            if question_desc == "":  # For avoiding instant answers
                raise NameError  # Explicit raising
            question_url = result.find("a").get("href")  # Retrieves the Stack Overflow link
            question_url = fix_google_url(question_url.lower())

            if question_url is None:
                i = i - 1
                continue

            questions.append([question_title, question_desc, question_url])
            i += 1
        except NameError:
            continue
        except AttributeError:
            continue

    # Check if there are any valid question posts
    if not questions:
        socli.printer.print_warning("No results found...")
        sys.exit(0)
    return questions


def get_question_stats_and_answer(url):
    """
    Fetch the content of a StackOverflow page for a particular question.
    :param url: full url of a StackOverflow question
    :return: tuple of ( question_title, question_desc, question_stats, answers )
    """
    random_headers()
    res_page = requests.get(url, headers=header)
    captcha_check(res_page.url)
    soup = BeautifulSoup(res_page.text, 'html.parser')
    dup_url = None
    question_title, question_desc, question_stats, dup_url = get_stats(soup)
    answers = [s.get_text() for s in soup.find_all("div", class_="post-text")][
                1:]  # first post is question, discard it.
    if len(answers) == 0:
        answers.append('No answers for this question ...')
    return question_title, question_desc, question_stats, answers, dup_url


def get_stats(soup):
    """
    Get Question stats
    :param soup:
    :return:
    """
    question_title = (soup.find_all("a", class_="question-hyperlink")[0].get_text())
    question_stats = (soup.find_all("div", class_="js-vote-count")[0].get_text())
    dup_url = None
    try:

        asked_info = soup.find("time").parent.get_text()
        active_info = soup.find("time").parent.findNext('div').get_text()
        viewed_info = soup.find("time").parent.findNext('div').findNext('div').get_text()
        question_stats = "Votes " + question_stats + " | " + asked_info + " | " + active_info + " | " + viewed_info
    except:
        question_stats = "Could not load statistics."
    question_desc = (soup.find_all("div", class_="post-text")[0])
    if '[duplicate]' in question_title:
        dup_answer = (soup.find_all("div", class_="post-text")[0])
        link = dup_answer.find('a')['href']
        link = so_url+link
        dup_url = copy.deepcopy(link)
        #using deepcopy else after the decompose of the first div, the url will be lost.
        question_desc.find('div').decompose()
    add_urls(question_desc)
    question_desc = question_desc.get_text()
    question_stats = ' '.join(question_stats.split())
    return question_title, question_desc, question_stats, dup_url


def add_urls(tags):
    """
    Adds the URL to any hyperlinked text found in a question
    or answer.
    :param tags:
    """
    images = tags.find_all("a")

    for image in images:
        if hasattr(image, "href"):
            image.string = "{} [{}]".format(image.text, image['href'])


def socli_interactive_windows(query):
    """
    Interactive mode basic implementation for windows, since urwid doesn't support CMD.
    :param query:
    :return:
    """
    try:
        search_res = requests.get(so_qurl + query)
        captcha_check(search_res.url)
        soup = BeautifulSoup(search_res.text, 'html.parser')
        try:
            soup.find_all("div", class_="question-summary")[0]  # For explictly raising exception
            tmp = (soup.find_all("div", class_="question-summary"))
            tmp1 = (soup.find_all("div", class_="excerpt"))
            i = 0
            question_local_url = []
            print(socli.printer.bold("\nSelect a question below:\n"))
            while i < len(tmp):
                if i == 10: break  # limiting results
                question_text = ' '.join((tmp[i].a.get_text()).split())
                question_text = question_text.replace("Q: ", "")
                question_desc = (tmp1[i].get_text()).replace("'\r\n", "")
                question_desc = ' '.join(question_desc.split())
                socli.printer.print_warning(str(i + 1) + ". " + socli.printer.display_str(question_text))
                question_local_url.append(tmp[i].a.get("href"))
                print("  " + socli.printer.display_str(question_desc) + "\n")
                i = i + 1
            try:
                op = int(socli.printer.inputs("\nType the option number to continue or any other key to exit:"))
                while 1:
                    if (op > 0) and (op <= i):
                        socli.printer.display_results(so_url + question_local_url[op - 1])
                        cnt = 1  # this is because the 1st post is the question itself
                        while 1:
                            global tmpsoup
                            qna = socli.printer.inputs(
                                "Type " + socli.printer.bold("o") + " to open in browser, " + socli.printer.bold("n") + " to next answer, " + socli.printer.bold(
                                    "b") + " for previous answer or any other key to exit:")
                            if qna in ["n", "N"]:
                                try:
                                    answer = (tmpsoup.find_all("div", class_="post-text")[cnt + 1].get_text())
                                    socli.printer.print_green("\n\nAnswer:\n")
                                    print("-------\n" + answer + "\n-------\n")
                                    cnt = cnt + 1
                                except IndexError as e:
                                    socli.printer.print_warning(" No more answers found for this question. Exiting...")
                                    sys.exit(0)
                                continue
                            elif qna in ["b", "B"]:
                                if cnt == 1:
                                    socli.printer.print_warning(" You cant go further back. You are on the first answer!")
                                    continue
                                answer = (tmpsoup.find_all("div", class_="post-text")[cnt - 1].get_text())
                                socli.printer.print_green("\n\nAnswer:\n")
                                print("-------\n" + answer + "\n-------\n")
                                cnt = cnt - 1
                                continue
                            elif qna in ["o", "O"]:
                                import webbrowser
                                if sys.platform.startswith('darwin'):
                                    browser = webbrowser.get('safari')
                                else:
                                    browser = webbrowser.get()
                                socli.printer.print_warning("Opening in your browser...")
                                browser.open(so_url + question_local_url[op - 1])
                            else:
                                break
                        sys.exit(0)
                    else:
                        op = int(input("\n\nWrong option. select the option no to continue:"))
            except Exception as e:
                socli.printer.showerror(e)
                socli.printer.print_warning("\n Exiting...")
                sys.exit(0)
        except IndexError:
            socli.printer.print_warning("No results found...")
            sys.exit(0)

    except UnicodeEncodeError:
        socli.printer.print_warning("\n\nEncoding error: Use \"chcp 65001\" command before using socli...")
        sys.exit(0)
    except requests.exceptions.ConnectionError:
        socli.printer.print_fail("Please check your internet connectivity...")
    except Exception as e:
        socli.printer.showerror(e)
        sys.exit(0)


def socli_interactive(query):
    """
    Interactive mode
    :return:
    """
    if sys.platform == 'win32':
        return socli_interactive_windows(query)

    class SelectQuestionPage(urwid.WidgetWrap):

        def display_text(self, index, question):
            question_text, question_desc, _ = question
            text = [
                ("warning", u"{}. {}\n".format(index, question_text)),
                question_desc + "\n",
                ]
            return text

        def __init__(self, questions):
            self.questions = questions
            self.cachedQuestions = [None for _ in range(10)]
            widgets = [self.display_text(i, q) for i, q in enumerate(questions)]
            self.questions_box = socli.tui.ScrollableTextBox(widgets)
            self.header = socli.tui.UnicodeText(('less-important', 'Select a question below:\n'))
            self.footerText = '0-' + str(len(self.questions) - 1) + ': select a question, any other key: exit.'
            self.errorText = socli.tui.UnicodeText.to_unicode('Question numbers range from 0-' +
                                                        str(len(self.questions) - 1) +
                                                        ". Please select a valid question number.")
            self.footer = socli.tui.UnicodeText(self.footerText)
            self.footerText = socli.tui.UnicodeText.to_unicode(self.footerText)
            frame = urwid.Frame(header=self.header,
                                body=urwid.Filler(self.questions_box, height=('relative', 100), valign='top'),
                                footer=self.footer)
            urwid.WidgetWrap.__init__(self, frame)

        # Override parent method
        def selectable(self):
            return True

        def keypress(self, size, key):
            if key in '0123456789':
                try:
                    question_url = self.questions[int(key)][2]
                    self.footer.set_text(self.footerText)
                    self.select_question(question_url, int(key))
                except IndexError:
                    self.footer.set_text(self.errorText)
            elif key in {'down', 'up'}:
                self.questions_box.keypress(size, key)
            else:
                raise urwid.ExitMainLoop()

        def select_question(self, url, index):
            if self.cachedQuestions[index] is not None:
                socli.tui.question_post = self.cachedQuestions[index]
                socli.tui.MAIN_LOOP.widget = socli.tui.question_post
            else:
                if not google_search:
                    url = so_url + url
                question_title, question_desc, question_stats, answers = get_question_stats_and_answer(url)
                socli.tui.question_post = socli.tui.QuestionPage((answers, question_title, question_desc, question_stats, url))
                self.cachedQuestions[index] = socli.tui.question_post
                socli.tui.MAIN_LOOP.widget = socli.tui.question_post

    socli.tui.display_header = socli.tui.Header()

    try:
        if google_search:
            questions = get_questions_for_query_google(query)
        else:
            questions = get_questions_for_query(query)
        question_page = SelectQuestionPage(questions)
        socli.tui.MAIN_LOOP = socli.tui.EditedMainLoop(question_page, socli.printer.palette)
        socli.tui.MAIN_LOOP.run()

    except UnicodeEncodeError:
        socli.printer.print_warning("\n\nEncoding error: Use \"chcp 65001\" command before using socli...")
        sys.exit(0)
    except requests.exceptions.ConnectionError:
        socli.printer.print_fail("Please check your internet connectivity...")
    except Exception as e:
        socli.printer.showerror(e)
        print("exiting...")
        sys.exit(0)


def socli_manual_search(query, rn):
    """
    Manual search by question index
    :param query:
    :param rn:
    :return:
    """
    if rn < 1:
        socli.printer.print_warning(
            "Count starts from 1. Use: \"socli -i 2 -q python for loop\" for the 2nd result for the query")
        sys.exit(0)
    query = socli.printer.urlencode(query)
    try:
        random_headers()
        # Set count = 99 so you can choose question numbers higher than 10
        count = 99
        res_url = None
        try:
            if google_search:
                questions = get_questions_for_query_google(query, count)
                res_url = questions[rn - 1][2]
            else:
                questions = get_questions_for_query(query, count)
                res_url = so_url + questions[rn - 1][2]
            socli.printer.display_results(res_url)
        except IndexError:
            socli.printer.print_warning("No results found...")
            sys.exit(1)
    except UnicodeEncodeError:
        socli.printer.print_warning("Encoding error: Use \"chcp 65001\" command before "
                         "using socli...")
        sys.exit(0)
    except requests.exceptions.ConnectionError:
        socli.printer.print_fail("Please check your internet connectivity...")
    except Exception as e:
        socli.printer.showerror(e)
        sys.exit(0)


def fix_google_url(url):
    """
    Fixes the url extracted from HTML when
    performing a google search
    :param url:
    :return: Correctly formatted URL to be used in requests.get
    """
    if "&sa=" in url:
        url = url.split("&")[0]
    if "/url?q=" in url[0:7]:
        url = url[7:]  # Removes the "/url?q=" prefix

    if url[:30] == "http://www.google.com/url?url=":
        # Used to get rid of this header and just retrieve the Stack Overflow link
        url = url[30:]

    if "http" not in url[:4]:
        url = "https://" + url  # Add the protocol if it doesn't already exist

    # Makes sure that we stay in the questions section of Stack Overflow
    if not bool(re.search(r"/questions/[0-9]+", url)) and not bool(re.search(r"\.com/a/[0-9]", url)):
        return None

    if url[:17] == "https:///url?url=":  # Resolves rare bug in which this is a prefix
        url = url[17:]

    return url


def captcha_check(url):
    """
    Exits program when there is a captcha, preventing any error.
    Users will have to manually verify their identity.
    :param url: URL from Stack Overflow
    :return:
    """
    if google_search:
        google_error_display_msg = "Google thinks you're a bot because you're issuing too many queries too quickly!" + \
                                   " Now you'll have to wait about an hour before you're unblocked... :(. " \
                                   "Use the -s tag to search via Stack Overflow instead."
        # Check if google detects user as a bot
        if re.search(r"ipv4\.google\.com/sorry", url):
            socli.printer.print_warning(google_error_display_msg)
            exit(0)
    else:
        if re.search(r"\.com/nocaptcha", url):  # Searching for stackoverflow captcha check
            socli.printer.print_warning("StackOverflow captcha check triggered. Please wait a few seconds before trying again.")
            exit(0)


def load_user_agents():
    """
    Loads the list of user agents from user_agents.txt
    :return:
    """
    global uas
    uas = []
    with open(os.path.join(os.path.dirname(__file__), "user_agents.txt"), 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.rstrip())
    random.shuffle(uas)


def random_headers():
    """
    Sets header variable to a random value
    :return:
    """
    global uas
    global header
    if uas == []:
        load_user_agents()
    ua = random.choice(uas)
    header = {"User-Agent": ua}
