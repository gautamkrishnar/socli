"""
# Stack Overflow CLI
# Created by
# Gautam Krishna R : www.github.com/gautamkrishnar
# And open source contributors at GitHub: https://github.com/gautamkrishnar/socli#contributors
"""

import argparse
import os
import sys
import textwrap

import requests
from bs4 import BeautifulSoup
import urwid

import tui as tui
import user as us
import search as se
import printer as pr

try:
    import simplejson as json
except ImportError:
    import json
try:
    JSONDecodeError = json.JSONDecodeError
except AttributeError:
    JSONDecodeError = ValueError

tag = ""  # tag based search
query = ""  # Query

int_url = "https://api.stackexchange.com/2.2/questions?pagesize=1&fromdate=1505865600" \
          "&order=desc&sort=hot&site=stackoverflow" \
          "&filter=!Of_8jOSDGzxt79jzpisa)vWRNvJcb7(XI)6wn.qe(De&key=5SPES3J0Z4i7Yh)ov3ZKMA(("

# Suppressing InsecureRequestWarning and many others
requests.packages.urllib3.disable_warnings()


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
        pr.print_warning("Wrong syntax!...\n")
        pr.helpman()
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
        se.so_qurl = se.so_qurl + "[" + tags + "]" + "+"

# =====================================================================================================================


def socli(query):
    """
    SoCLI Code
    :param query: Query to search on Stack Overflow.
    If google_search is true uses Google search to find the best result.
    Else, use Stack Overflow default search mechanism.
    :return:
    """
    query = pr.urlencode(query)
    try:
        if se.google_search:
            questions = se.get_questions_for_query_google(query)
            res_url = questions[0][2]  # Gets the first result
            display_results(res_url)
        else:
            questions = se.get_questions_for_query(query)
            res_url = questions[0][2]
            display_results(se.so_url + res_url)  # Returned URL is relative to SO homepage
    except UnicodeEncodeError as e:
        pr.showerror(e)
        pr.print_warning("\n\nEncoding error: Use \"chcp 65001\" command before using socli...")
        sys.exit(0)
    except requests.exceptions.ConnectionError:
        pr.print_fail("Please check your internet connectivity...")
    except Exception as e:
        pr.showerror(e)
        sys.exit(0)


def display_results(url):
    """
    Display result page
    :param url: URL of the search result
    :return:
    """
    se.random_headers()
    res_page = requests.get(url, headers=se.header)
    se.captcha_check(res_page.url)
    tui.display_header = tui.Header()
    question_title, question_desc, question_stats, answers = se.get_question_stats_and_answer(url)
    tui.question_post = tui.QuestionPage((answers, question_title, question_desc, question_stats, url))
    tui.MAIN_LOOP = tui.EditedMainLoop(tui.question_post, pr.palette)
    tui.MAIN_LOOP.run()


def parse_arguments(command):
    """
    Parses the command into arguments and flags
    :param command: the command in list form
    :return: an object that contains the values for all arguments

    Currently, all help messages are not in use and helpman() is the default.
    Need to implement nicer --help format in the future.
    """
    parser = argparse.ArgumentParser(description=textwrap.dedent('Stack Overflow command line client'), add_help=False)

    # Comment this line out if you want to use argparse's default help function
    parser.add_argument('--help', '-h', action='store_true', help='Show this help message and exit')

    # Flags that return true if present and false if not
    parser.add_argument('--new', '-n', action='store_true',
                        help=textwrap.dedent("Opens the stack overflow new questions page in your "
                                             "default browser. You can create a new question using it."))
    parser.add_argument('--interactive', '-i', action='store_true', help=textwrap.dedent(
        "To search in Stack Overflow and display the matching results. "
        "You can choose and browse any of the results interactively"))
    parser.add_argument('--debug', action='store_true', help="Turn debugging mode on")
    parser.add_argument('--sosearch', '-s', action='store_true',
                        help="Searches directly on Stack Overflow instead of using Google")
    parser.add_argument('--api', '-a', action='store_true', help="Sets a custom API key for socli")
    parser.add_argument('--delete', '-d', action='store_true',
                        help="Deletes the configuration file generated by socli -u command")

    # Accepts 1 argument. Returns None if flag is not present and
    # 'STORED_USER' if flag is present, but no argument is supplied
    parser.add_argument('--user', '-u', nargs='?', const='(RANDOM_STRING_CONSTANT)', type=str,
                        help="Displays information about the user "
                             "provided as the next argument(optional). If no argument is provided "
                             "it will ask the user to enter a default username. Now the user "
                             "can run the command without the argument")

    # Accepts one or more arguments
    parser.add_argument('--tag', '-t', nargs='+', help="To search a query by tag on stack overflow."
                                                       "Visit http://stackoverflow.com/tags to see the list of all "
                                                       "tags.\n   eg:- socli --tag javascript,node.js --query "
                                                       "foo bar: Displays the search result of the query"
                                                       " \"foo bar\" in stack overflow's javascript and node.js tags")
    parser.add_argument('--query', '-q', nargs='+', default=[],
                        help="If any of the following commands are used then you "
                             "must specify this option and a query following it.")
    parser.add_argument('--browse', '-b', nargs='+', default=[],
                        help="Searches for ten hot,week and interesting questions on today's page ")
    # Accepts 0 or more arguments. Used to catch query if no flags are present
    parser.add_argument('userQuery', nargs='*', help=argparse.SUPPRESS)

    # Accepts 1 argument
    parser.add_argument('--res', '-r', type=int, help="To select and display a result manually and display "
                                                      "its most voted answer. \n   eg:- socli --res 2 --query "
                                                      "foo bar: Displays the second search result of the query"
                                                      " \"foo bar\"'s most voted answer")

    namespace = parser.parse_args(command)
    return namespace


# ========================= BROWSE FEATURE                                            =================================
# ========================= WIP, has been left untouched for the sake of this project =================================
# ========================= Should probably be moved into the search module           =================================


def socli_browse_interactive_windows(query_tag):
    """
    Interactive mode for -b browse
    :param query_tag:
    :return:
    """
    try:
        search_res = requests.get(se.so_burl + query_tag)
        se.captcha_check(search_res.url)
        soup = BeautifulSoup(search_res.text, 'html.parser')
        try:
            soup.find_all("div", class_="question-summary")[0]  # For explicitly raising exception
            tmp = (soup.find_all("div", class_="question-summary"))
            i = 0
            question_local_url = []
            print(pr.bold("\nSelect a question below:\n"))
            while i < len(tmp):
                if i == 10:
                    break  # limiting results
                question_text = ' '.join((tmp[i].a.get_text()).split())
                question_text = question_text.replace("Q: ", "")
                pr.print_warning(str(i + 1) + ". " + pr.display_str(question_text))
                q_tag = (soup.find_all("div", class_="question-summary"))[i]
                answers = [s.get_text() for s in q_tag.find_all("a", class_="post-tag")][0:]
                ques_tags = " ".join(str(x) for x in answers)
                question_local_url.append(tmp[i].a.get("href"))
                print("  " + pr.display_str(ques_tags) + "\n")
                i = i + 1
            try:
                op = int(pr.inputs("\nType the option no to continue or any other key to exit:"))
                while 1:
                    if (op > 0) and (op <= i):
                        display_results(se.so_burl + question_local_url[op - 1])
                        cnt = 1  # this is because the 1st post is the question itself
                        while 1:
                            global tmpsoup
                            qna = pr.inputs(
                                "Type " + pr.bold("o") + " to open in browser, " + pr.bold(
                                    "n") + " to next answer, " + pr.bold(
                                    "b") + " for previous answer or any other key to exit:")
                            if qna in ["n", "N"]:
                                try:
                                    answer = (tmpsoup.find_all("div", class_="post-text")[cnt + 1].get_text())
                                    pr.print_green("\n\nAnswer:\n")
                                    print("-------\n" + answer + "\n-------\n")
                                    cnt = cnt + 1
                                except IndexError:
                                    pr.print_warning(" No more answers found for this question. Exiting...")
                                    sys.exit(0)
                                continue
                            elif qna in ["b", "B"]:
                                if cnt == 1:
                                    pr.print_warning(" You cant go further back. You are on the first answer!")
                                    continue
                                answer = (tmpsoup.find_all("div", class_="post-text")[cnt - 1].get_text())
                                pr.print_green("\n\nAnswer:\n")
                                print("-------\n" + answer + "\n-------\n")
                                cnt = cnt - 1
                                continue
                            elif qna in ["o", "O"]:
                                import webbrowser
                                pr.print_warning("Opening in your browser...")
                                webbrowser.open(se.so_burl + question_local_url[op - 1])
                            else:
                                break
                        sys.exit(0)
                    else:
                        op = int(input("\n\nWrong option. select the option no to continue:"))
            except Exception as e:
                pr.showerror(e)
                pr.print_warning("\n Exiting...")
                sys.exit(0)
        except IndexError:
            pr.print_warning("No results found...")
            sys.exit(0)

    except UnicodeEncodeError:
        pr.print_warning("\n\nEncoding error: Use \"chcp 65001\" command before using socli...")
        sys.exit(0)
    except requests.exceptions.ConnectionError:
        pr.print_fail("Please check your internet connectivity...")
    except Exception as e:
        pr.showerror(e)
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
                if not se.google_search:
                    url = se.so_url + url
                question_title, question_desc, question_stats, answers = se.get_question_stats_and_answer(url)
                question_post = tui.QuestionPage((answers, question_title, question_desc, question_stats, url))
                self.cachedQuestions[index] = question_post
                tui.MAIN_LOOP.widget = question_post

    tui.display_header = tui.Header()

    try:
        if se.google_search:
            questions = se.get_questions_for_query_google(query)
        else:
            # print('hurr')
            questions = se.get_questions_for_query(query_tag)
            # print(questions)

        question_page = SelectQuestionPage(questions)

        tui.MAIN_LOOP = tui.EditedMainLoop(question_page, pr.palette)
        tui.MAIN_LOOP.run()

    except UnicodeEncodeError:
        pr.print_warning("\n\nEncoding error: Use \"chcp 65001\" command before using socli...")
        sys.exit(0)
    except requests.exceptions.ConnectionError:
        pr.print_fail("Please check your internet connectivity...")
    except Exception as e:
        pr.showerror(e)
        # print("Hurra")
        print("exiting...")
        sys.exit(0)

# =====================================================================================================================


def main():
    """
    The main logic for how options in a command is checked.
    """
    global query
    namespace = parse_arguments(sys.argv[1:])
    se.load_user_agents()  # Populates the user agents array
    query_tag = ' '.join(namespace.browse)
    # print (namespace.userQuery)
    query = ' '.join(namespace.query) + ' ' + ' '.join(namespace.userQuery)
    # print(query1)
    if namespace.help:
        pr.helpman()
        sys.exit(0)
    if namespace.debug:  # If --debug flag is present
        pr.DEBUG = True
    if namespace.new:  # If --new flag is present
        import webbrowser
        pr.print_warning("Opening stack overflow in your browser...")
        webbrowser.open(se.so_url + "/questions/ask")
        sys.exit(0)
    if namespace.api:  # If --api flag is present
        us.set_api_key()
        sys.exit(0)
    if namespace.user is not None:  # If --user flag is present
        # Stackoverflow user profile support
        if namespace.user != '(RANDOM_STRING_CONSTANT)':  # If user provided a user ID
            us.manual = 1
            user = namespace.user
        else:  # If user did not provide a user id
            user = us.retrieve_saved_profile()
        us.user_page(user)
        sys.exit(0)
    if namespace.delete:  # If --delete flag is present
        us.del_datafile()
        pr.print_warning("Data files deleted...")
        sys.exit(0)
    if namespace.sosearch:  # If --sosearch flag is present
        se.google_search = False
    if namespace.tag:  # If --tag flag is present
        global tag
        se.google_search = False
        tag = namespace.tag
        has_tags()
    if namespace.res is not None:  # If --res flag is present
        question_number = namespace.res
        if namespace.query != [] or namespace.tag is not None:  # There must either be a tag or a query
            se.socli_manual_search(query, question_number)
        else:
            pr.print_warning('You must specify a query or a tag. For example, use: "socli -r 3 -q python for loop" '
                             'to retrieve the third result when searching about "python for loop". '
                             'You can also use "socli -r 3 -t python" '
                             'to retrieve the third result when searching for posts with the "python" tag.')
    if namespace.browse:
        se.google_search = False
        socli_browse_interactive(query_tag)
    elif namespace.query != [] or namespace.tag is not None:  # If query and tag are not both empty
        if namespace.interactive:
            se.socli_interactive(query)
        else:
            socli(query)
    elif query != ' ' and not (
            namespace.tag or namespace.res or namespace.interactive or namespace.browse):  # If there are no flags
        socli(query)
    else:
        # Help text for interactive mode
        if namespace.interactive and namespace.query == [] and namespace.tag is None:
            pr.print_warning('You must specify a query or a tag. For example, use: "socli -iq python for loop" '
                             'to search about "python for loop" in interactive mode. '
                             'You can also use "socli -it python" '
                             'to search posts with the "python" tag in interactive mode.')
        else:
            pr.helpman()


if __name__ == '__main__':
    main()
