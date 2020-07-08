"""
# Stack Overflow CLI
# Created by
# Gautam Krishna R : www.github.com/gautamkrishnar
# And open source contributors at GitHub: https://github.com/gautamkrishnar/socli#contributors
"""

import os
import re
import sys
import logging
import requests
from bs4 import BeautifulSoup
import urwid
import urllib3

try:
    import simplejson as json
except ImportError:
    import json
try:
    JSONDecodeError = json.JSONDecodeError
except AttributeError:
    JSONDecodeError = ValueError

# Importing SoCli modules
import socli.tui as tui
import socli.user as user_module
import socli.search as search
import socli.printer as printer
from socli.parser import parse_arguments
from socli.printer import display_results


tag = ""  # tag based search
query = ""  # Query

# Suppressing InsecureRequestWarning and many others
urllib3.disable_warnings()
# logger for debugging
logger = logging.getLogger(__name__)

# Switch on logging of the requests module.
def debug_requests_on():
    try:
        from http.client import HTTPConnection
        HTTPConnection.set_debuglevel(HTTPConnection, 1)
    except ImportError:
        import httplib
        httplib.HTTPConnection.debuglevel = 2

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger('requests.packages.urllib3')
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

# Fixes windows active page code errors
def fix_code_page():
    if sys.platform == 'win32':
        if sys.stdout.encoding != 'cp65001':
            os.system("echo off")
            os.system("chcp 65001")  # Change active page code
            sys.stdout.write("\x1b[A")  # Removes the output of chcp command
            sys.stdout.flush()
            return
        else:
            return


def wrongsyn(query):
    """
    Exits if query value is empty
    :param query:
    :return:
    """
    if query == "":
        printer.print_warning("Wrong syntax!...\n")
        printer.helpman()
        sys.exit(1)
    else:
        return


def has_tags():
    """
    Gets the tags and adds them to query url
    :return:
    """
    global tag
    for tags in tag:
        search.so_qurl = search.so_qurl + "[" + tags + "]" + "+"


def socli(query):
    """
    SoCLI Code
    :param query: Query to search on Stack Overflow.
    If google_search is true uses Google search to find the best result.
    Else, use Stack Overflow default search mechanism.
    :return:
    """
    query = printer.urlencode(query)
    try:
        if search.google_search:
            questions = search.get_questions_for_query_google(query)
            res_url = questions[0][2]  # Gets the first result
            display_results(res_url)
        else:
            questions = search.get_questions_for_query(query)
            res_url = questions[0][2]
            display_results(search.so_url + res_url)  # Returned URL is relative to SO homepage
    except UnicodeEncodeError as e:
        printer.showerror(e)
        printer.print_warning("\n\nEncoding error: Use \"chcp 65001\" command before using socli...")
        sys.exit(0)
    except requests.exceptions.ConnectionError:
        printer.print_fail("Please check your internet connectivity...")
    except Exception as e:
        printer.showerror(e)
        sys.exit(0)


def socli_browse_interactive_windows(query_tag):
    """
    Interactive mode for -b browse
    :param query_tag:
    :return:
    """
    try:
        search_res = requests.get(search.so_burl + query_tag)
        search.captcha_check(search_res.url)
        soup = BeautifulSoup(search_res.text, 'html.parser')
        try:
            soup.find_all("div", class_="question-summary")[0]  # For explicitly raising exception
            tmp = (soup.find_all("div", class_="question-summary"))
            i = 0
            question_local_url = []
            print(printer.bold("\nSelect a question below:\n"))
            while i < len(tmp):
                if i == 10:
                    break  # limiting results
                question_text = ' '.join((tmp[i].a.get_text()).split())
                question_text = question_text.replace("Q: ", "")
                printer.print_warning(str(i + 1) + ". " + printer.display_str(question_text))
                q_tag = (soup.find_all("div", class_="question-summary"))[i]
                answers = [s.get_text() for s in q_tag.find_all("a", class_="post-tag")][0:]
                ques_tags = " ".join(str(x) for x in answers)
                question_local_url.append(tmp[i].a.get("href"))
                print("  " + printer.display_str(ques_tags) + "\n")
                i = i + 1
            try:
                op = int(printer.inputs("\nType the option no to continue or any other key to exit:"))
                while 1:
                    if (op > 0) and (op <= i):
                        display_results(search.so_burl + question_local_url[op - 1])
                        cnt = 1  # this is because the 1st post is the question itself
                        while 1:
                            global tmpsoup
                            qna = printer.inputs(
                                "Type " + printer.bold("o") + " to open in browser, " + printer.bold(
                                    "n") + " to next answer, " + printer.bold(
                                    "b") + " for previous answer or any other key to exit:")
                            if qna in ["n", "N"]:
                                try:
                                    answer = (tmpsoup.find_all("div", class_="post-text")[cnt + 1].get_text())
                                    printer.print_green("\n\nAnswer:\n")
                                    print("-------\n" + answer + "\n-------\n")
                                    cnt = cnt + 1
                                except IndexError:
                                    printer.print_warning(" No more answers found for this question. Exiting...")
                                    sys.exit(0)
                                continue
                            elif qna in ["b", "B"]:
                                if cnt == 1:
                                    printer.print_warning(" You cant go further back. You are on the first answer!")
                                    continue
                                answer = (tmpsoup.find_all("div", class_="post-text")[cnt - 1].get_text())
                                printer.print_green("\n\nAnswer:\n")
                                print("-------\n" + answer + "\n-------\n")
                                cnt = cnt - 1
                                continue
                            elif qna in ["o", "O"]:
                                import webbrowser
                                printer.print_warning("Opening in your browser...")
                                webbrowser.open(search.so_burl + question_local_url[op - 1])
                            else:
                                break
                        sys.exit(0)
                    else:
                        op = int(input("\n\nWrong option. select the option no to continue:"))
            except Exception as e:
                printer.showerror(e)
                printer.print_warning("\n Exiting...")
                sys.exit(0)
        except IndexError:
            printer.print_warning("No results found...")
            sys.exit(0)

    except UnicodeEncodeError:
        printer.print_warning("\n\nEncoding error: Use \"chcp 65001\" command before using socli...")
        sys.exit(0)
    except requests.exceptions.ConnectionError:
        printer.print_fail("Please check your internet connectivity...")
    except Exception as e:
        printer.showerror(e)
        sys.exit(0)


def socli_browse_interactive(query_tag):
    """
    Interactive mode
    :return:
    """
    if sys.platform == 'win32':
        return socli_browse_interactive_windows(query_tag)

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
            self.questions_box = tui.ScrollableTextBox(widgets)
            self.header = tui.UnicodeText(('less-important', 'Select a question below:\n'))
            self.footerText = '0-' + str(len(self.questions) - 1) + ': select a question, any other key: exit.'
            self.errorText = tui.UnicodeText.to_unicode('Question numbers range from 0-' +
                                                        str(len(self.questions) - 1) +
                                                        ". Please select a valid question number.")
            self.footer = tui.UnicodeText(self.footerText)
            self.footerText = tui.UnicodeText.to_unicode(self.footerText)
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
                tui.question_post = self.cachedQuestions[index]
                tui.MAIN_LOOP.widget = tui.question_post
            else:
                if not search.google_search:
                    url = search.so_url + url
                question_title, question_desc, question_stats, answers = search.get_question_stats_and_answer(url)
                question_post = tui.QuestionPage((answers, question_title, question_desc, question_stats, url))
                self.cachedQuestions[index] = question_post
                tui.MAIN_LOOP.widget = question_post

    tui.display_header = tui.Header()

    try:
        if search.google_search:
            questions = search.get_questions_for_query_google(query)
        else:
            # print('hurr')
            questions = search.get_questions_for_query(query_tag)
            # print(questions)

        question_page = SelectQuestionPage(questions)

        tui.MAIN_LOOP = tui.EditedMainLoop(question_page, printer.palette)
        tui.MAIN_LOOP.run()

    except UnicodeEncodeError:
        printer.print_warning("\n\nEncoding error: Use \"chcp 65001\" command before using socli...")
        sys.exit(0)
    except requests.exceptions.ConnectionError:
        printer.print_fail("Please check your internet connectivity...")
    except Exception as e:
        printer.showerror(e)
        # print("Hurra")
        print("exiting...")
        sys.exit(0)


def main():
    """
    The main logic for how options in a command is checked.
    """
    global query
    namespace = parse_arguments(sys.argv[1:])
    search.load_user_agents()  # Populates the user agents array
    query_tag = ' '.join(namespace.browse)  # Tags

    # Query
    if namespace.query:
        # Query when args are present
        query = ' '.join(namespace.query)
    elif namespace.userQuery:
        # Query without any args
        query = ' '.join(namespace.userQuery)

    if namespace.help:
        # Display command line syntax
        printer.helpman()
        sys.exit(0)

    if namespace.debug:  # If --debug flag is present
        # Prints out error used for debugging
        printer.DEBUG = True
        debug_requests_on()

    if namespace.new:  # If --new flag is present
        # Opens StackOverflow website in the browser to create a  new question
        import webbrowser
        printer.print_warning("Opening stack overflow in your browser...")
        webbrowser.open(search.so_url + "/questions/ask")
        sys.exit(0)

    if namespace.api:  # If --api flag is present
        # Sets custom API key
        user_module.set_api_key()
        sys.exit(0)

    if namespace.user is not None:  # If --user flag is present
        # Stackoverflow user profile support
        if namespace.user != '(RANDOM_STRING_CONSTANT)':  # If user provided a user ID
            user_module.manual = 1  # Enabling manual mode
            user = namespace.user
        else:  # If user did not provide a user id
            user = user_module.retrieve_saved_profile()  # Reading saved user id from app data
        user_module.user_page(user)
        sys.exit(0)

    if namespace.delete:  # If --delete flag is present
        # Deletes user data
        user_module.del_datafile()
        printer.print_warning("Data files deleted...")
        sys.exit(0)

    if namespace.sosearch:  # If --sosearch flag is present
        # Disables google search
        search.google_search = False

    if namespace.tag:  # If --tag flag is present
        global tag
        search.google_search = False
        tag = namespace.tag
        has_tags()  # Adds tags to StackOverflow url (when not using google search.
    if namespace.open_url:
        import webbrowser
        open_in_browser=False
        display_condition=True
        url_to_use=namespace.open_url[0]
        if re.findall(r"^https:\/\/",url_to_use) !=[]:
            pass
        else:
            url_to_use="https://" + url_to_use
        try:
            if url_to_use == "https://stackoverflow.com/questions/":
                raise Exception('URL Error')
            if url_to_use == "https://www.stackoverflow.com/questions/":
                raise Exception('URL Error')
            requests.get(url_to_use)
        except Exception:
            printer.print_warning("Error, could be:\n- invalid url\n- url cannot be opened in socli\n- internet connection error")
            sys.exit(0)
        nostackoverflow=re.findall(r"stackoverflow\.com",url_to_use)
        if nostackoverflow == []:
            open_in_browser=True
            display_condition=False
            printer.print_warning("Your url is not a stack overflow url.\nOpening in your browser...")
        tag_matcher=re.findall(r"\/tag.+\/",url_to_use)
        blog_matcher=re.findall(r"blog",url_to_use)
        if tag_matcher != []:
            extracted_tag=""
            if re.findall(r"tagged",url_to_use) == []:
                extracted_tag=re.split(r"\/",url_to_use)[4]
            else:
                extracted_tag=re.split(r"\/",url_to_use)[5]
            open_in_browser=False
            display_condition=False
            tag=extracted_tag
            search.socli_interactive(tag)
        if blog_matcher != []:
            open_in_browser=True
            display_condition=False
            printer.print_warning("Your url belongs to blog")
            printer.print_warning("Opening in browser...")
        if display_condition:
            open_in_browser=False
            display_results(url_to_use)
        if open_in_browser:
            webbrowser.open(url_to_use)
    if namespace.res is not None:  # If --res flag is present
        # Automatically displays the result specified by the number
        question_number = namespace.res
        if namespace.query != [] or namespace.tag is not None:  # There must either be a tag or a query
            search.socli_manual_search(query, question_number)
        else:
            printer.print_warning('You must specify a query or a tag. For example, use: "socli -r 3 -q python for loop" '
                             'to retrieve the third result when searching about "python for loop". '
                             'You can also use "socli -r 3 -t python" '
                             'to retrieve the third result when searching for posts with the "python" tag.')

    if namespace.browse:
        # Browse mode
        search.google_search = False
        socli_browse_interactive(query_tag)
    elif namespace.query != [] or namespace.tag is not None:  # If query and tag are not both empty
        if namespace.interactive:
            search.socli_interactive(query)
        else:
            socli(query)
    elif query not in [' ', ''] and not (
            namespace.tag or namespace.res or namespace.interactive or namespace.browse):  # If there are no flags
        socli(query)
    else:
        # Help text for interactive mode
        if namespace.interactive and namespace.query == [] and namespace.tag is None:
            printer.print_warning('You must specify a query or a tag. For example, use: "socli -iq python for loop" '
                             'to search about "python for loop" in interactive mode. '
                             'You can also use "socli -it python" '
                             'to search posts with the "python" tag in interactive mode.')
        else:
            printer.helpman()



if __name__ == '__main__':
    main()
