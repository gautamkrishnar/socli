"""
# Stack overflow CLI
# Created by
# Gautam krishna R : www.github.com/gautamkrishnar
# And open source contributors at GitHub: https://github.com/gautamkrishnar/socli#contributors
"""

import argparse
import os
import sys
import urllib
import colorama
import requests
import urwid
from bs4 import BeautifulSoup
import random
import re
import textwrap
import subprocess
import textwrap

try:
    import simplejson as json
except ImportError:
    import json
try:
    JSONDecodeError = json.JSONDecodeError
except AttributeError:
    JSONDecodeError = ValueError


# Global vars:
DEBUG = False  # Set True for enabling debugging
soqurl = "http://stackoverflow.com/search?q="  # Query url
sourl = "http://stackoverflow.com"  # Site url
sburl="https://stackoverflow.com/?tab="
tag = ""  # tag based search
app_data = dict()  # Data file dictionary
data_file = os.path.join(os.path.dirname(__file__), "data.json")  # Data file location
query = ""  # Query
uas = []  # User agent list
header = {}  # Request header
br = True
google_search = True # Uses google search. Enabled by default.
google_search_url = "https://www.google.com/search?q=site:stackoverflow.com+" #Google search query URL
question_post = None #Used to see whether we are currently displaying a question post
question_page = None #Not None only if in interactive mode. Displays all the questions found.
header_for_display = None #Used as header to display question post
LOOP = None #Main Loop used to render widgets

int_url="https://api.stackexchange.com/2.2/questions?pagesize=1&fromdate=1505865600&order=desc&sort=hot&site=stackoverflow&filter=!Of_8jOSDGzxt79jzpisa)vWRNvJcb7(XI)6wn.qe(De&key=5SPES3J0Z4i7Yh)ov3ZKMA(("


#Palette for question post colors
palette = [('answer', 'default', 'default'),
           ('title', 'light green, bold', 'default'),
           ('heading', 'light green, bold', 'default'),
           ('metadata', 'dark green', 'default'),
           ('less-important', 'dark gray', 'default'),
           ('warning', 'yellow', 'default')
           ]

# Suppressing InsecureRequestWarning and many others
requests.packages.urllib3.disable_warnings()

### To support python 2:
if sys.version < '3.0.0':
    global FileNotFoundError
    FileNotFoundError = IOError


    def urlencode(inp):
        return urllib.quote_plus(inp)


    def dispstr(inp):
        return inp.encode('utf-8')


    def inputs(str=""):
        sys.stdout.write(str)
        tempx = raw_input()
        return tempx
else:
    def urlencode(inp):
        return urllib.parse.quote_plus(inp)


    def dispstr(inp):
        return inp


    def inputs(str=""):
        sys.stdout.write(str)
        tempx = input()
        return tempx


### Fixes windows active page code errors
def fixCodePage():
    if sys.platform == 'win32':
        if sys.stdout.encoding != 'cp65001':
            os.system("echo off")
            os.system("chcp 65001")  # Change active page code
            sys.stdout.write("\x1b[A")  # Removes the output of chcp command
            sys.stdout.flush()
            return
        else:
            return


# Bold and underline are not supported by colorama.
class bcolors:
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class UnicodeText(urwid.Text):
    """ encode all text to utf-8 """

    def __init__(self, text):
        # As we were encoding all text to utf-8 in output before with dispstr, do it automatically for all input
        text = UnicodeText.to_unicode(text)
        urwid.Text.__init__(self, text)

    @classmethod
    def to_unicode(cls, markup):
        """convert urwid text markup object to utf-8"""
        try:
            return dispstr(markup)
        except AttributeError:
            mapped = [cls.to_unicode(i) for i in markup]
            if isinstance(markup, tuple):
                return tuple(mapped)
            else:
                return mapped

class Header(UnicodeText):
    """
    Header of the question page. Event messages are recorded here.
    """

    def __init__(self):
        self.current_event = None
        UnicodeText.__init__(self, '')

    def event(self, event, message):
        self.current_event = event
        self.set_text(message)

    def clear(self, event):
        if self.current_event == event:
            self.set_text('')

class EditedMainLoop(urwid.MainLoop):

    def process_input(self, keys):
        super(EditedMainLoop, self).process_input(keys)
        global question_post
        if question_post != None:
            if 'window resize' in keys:
                question_post.keypress(question_post, 'window resize')

class QuestionPage(urwid.WidgetWrap):
    """
    Main container for urwid interactive mode.
    """

    def __init__(self, data):
        """
        Construct the Question Page.
        :param data: tuple of (answers, question_title, question_desc, question_stats, question_url)
        """
        answer_frame = self.makeFrame(data)
        urwid.WidgetWrap.__init__(self, answer_frame)

    def makeFrame(self, data):
        """
        Returns a new frame that is formatted correctly with respect to the window's dimensions.
        :param data: tuple of (answers, question_title, question_desc, question_stats, question_url)
        :return: a new urwid.Frame object
        """
        answers, question_title, question_desc, question_stats, question_url = data
        self.data = data
        self.question_desc = question_desc
        self.url = question_url
        self.answer_text = AnswerText(answers)
        self.screenHeight, screenWidth = subprocess.check_output(['stty', 'size']).split()
        self.question_text = urwid.BoxAdapter(QuestionDescription(question_desc), int(max(1, (int(self.screenHeight) - 9) / 2)))
        answer_frame = urwid.Frame(
            header= urwid.Pile( [
                header_for_display,
                QuestionTitle(question_title),
                self.question_text,
                QuestionStats(question_stats),
                urwid.Divider('-')
            ]),
            body=self.answer_text,
            footer= urwid.Pile([
                QuestionURL(question_url),
                UnicodeText(u'\u2191: previous answer, \u2193: next answer, o: open in browser, \u2190: back, q: quit').encode('utf-8'))
            ])
        )
        return answer_frame

    def keypress(self, size, key):
        if key in {'down', 'n', 'N'}:
            self.answer_text.next_ans()
        elif key in {'up', 'b', 'B'}:
            self.answer_text.prev_ans()
        elif key in {'o', 'O'}:
            import webbrowser
            header_for_display.event('browser', "Opening in your browser...")
            webbrowser.open(self.url)
        elif key == 'left':
            global question_post
            global question_page
            question_post = None
            if question_page is None:
                sys.exit(0)
            else:
                LOOP.widget = question_page
        elif key == 'window resize':
            screenHeight, screenWidth = subprocess.check_output(['stty', 'size']).split()
            if self.screenHeight != screenHeight:
                self._invalidate()
                answer_frame = self.makeFrame(self.data)
                urwid.WidgetWrap.__init__(self, answer_frame)
        elif key in {'q', 'Q'}:
            sys.exit(0)


class AnswerText(urwid.WidgetWrap):
    """Answers to the question.

    Long answers can be navigated up or down using the mouse.
    """

    def __init__(self, answers):
        urwid.WidgetWrap.__init__(self, UnicodeText(''))
        self._selectable = True  # so that we receive keyboard input
        self.answers = answers
        self.index = 0
        self.set_answer()

    def set_answer(self):
        """
        We must use a box adapter to get the text to scroll when this widget is already in
        a Pile from the main question page. Scrolling is necessary for long answers which are longer
        than the length of the terminal.
        """
        self.content = [('less-important', 'Answer: ')] + self.answers[self.index].split("\n")
        self._w = ScrollableTextBox(self.content)

    def prev_ans(self):
        """go to previous answer."""
        self.index -= 1
        if self.index < 0:
            self.index = 0
            header_for_display.event('answer-bounds', "No previous answers.")
        else:
            header_for_display.clear('answer-bounds')
        self.set_answer()

    def next_ans(self):
        """go to next answer."""
        self.index += 1
        if self.index > len(self.answers) - 1:
            self.index = len(self.answers) - 1
            header_for_display.event('answer-bounds', "No more answers.")
        else:
            header_for_display.clear('answer-bounds')
        self.set_answer()

    def __len__(self):
        """ return number of rows in this widget """
        return len(self.content)

class ScrollableTextBox(urwid.ListBox):
    """ Display input text, scrolling through when there is not enough room.

    Scrolling through text takes a little work to support on Urwid.
    """

    def __init__(self, content):
        """
        :param content: text string to be displayed
        """
        lines = [UnicodeText(line) for line in content]
        body = urwid.SimpleFocusListWalker(lines)
        urwid.ListBox.__init__(self, body)

    def mouse_event(self, size, event, button, col, row, focus):
        SCROLL_WHEEL_UP = 4
        SCROLL_WHEEL_DOWN = 5
        if button == SCROLL_WHEEL_DOWN:
            self.keypress(size, 'down')
        elif button == SCROLL_WHEEL_UP:
            self.keypress(size, 'up')
        else:
            return False
        return True

class QuestionTitle(UnicodeText):
    """ Title of the question,"""

    def __init__(self, title):
        text = ["Question: ", ('title', title), "\n"]
        UnicodeText.__init__(self, text)

#Must convert to BoxAdapter object if used as a flow widget.
class QuestionDescription(urwid.WidgetWrap):
    """ Description of the question """

    def __init__(self, description):
        urwid.WidgetWrap.__init__(self, UnicodeText(''))
        self.description = description
        self.set_description()

    def set_description(self):
        """
        We must use a box adapter to get the text to scroll when this widget is already in
        a Pile from the main question page. Scrolling is necessary for long questions which are longer
        than the length of the terminal.
        """
        self.content =  self.description.strip("\n").split("\n")
        self._w = ScrollableTextBox(self.content)

    def __len__(self):
        """ return number of rows in this widget """
        return len(self.content)

class QuestionStats(UnicodeText):
    """ Stats of the question,"""

    def __init__(self, stats):
        text = ["\n", ('metadata', stats)]
        UnicodeText.__init__(self, text)

class QuestionURL(UnicodeText):
    """ url of the question """

    def __init__(self, url):
        text = ["\n", ('heading', 'Question URL: '), url]
        UnicodeText.__init__(self, text)

def format_str(str, color):
    return "{0}{1}{2}".format(color, str, colorama.Style.RESET_ALL)


def print_header(str):
    print(format_str(str, colorama.Fore.MAGENTA))


def print_blue(str):
    print(format_str(str, colorama.Fore.BLUE))


def print_green(str):
    print(format_str(str, colorama.Fore.GREEN))


def print_warning(str):
    print(format_str(str, colorama.Fore.YELLOW))


def print_fail(str):
    print(format_str(str, colorama.Fore.RED))


def print_white(str):
    print(format_str(str, colorama.Fore.WHITE))


def make_header(str):
    return format_str(str, colorama.Fore.MAGENTA)


def make_blue(str):
    return format_str(str, colorama.Fore.BLUE)


def make_green(str):
    return format_str(str, colorama.Fore.GREEN)


def make_warning(str):
    return format_str(str, colorama.Fore.YELLOW)


def make_fail(str):
    return format_str(str, colorama.Fore.RED)


def make_white(str):
    return format_str(str, colorama.Fore.WHITE)


def bold(str):
    return (format_str(str, bcolors.BOLD))


def underline(str):
    return (format_str(str, bcolors.UNDERLINE))


## For testing exceptions
def showerror(e):
    if DEBUG == True:
        import traceback
        print("Error name: " + e.__doc__)
        print()
        print("Description: " + str(e))
        print()
        traceback.print_exc()
    else:
        return


def socli(query):
    """
    SOCLI Code
    :param query: Query to search on stackoverflow.
    If google_search is true uses google search to find the best result.
    Else use stackoverflow default search mechanism.
    :return:
    """
    query = urlencode(query)
    try:
        if google_search:
            questions = get_questions_for_query_google(query)
            res_url = questions[0][2]  # Gets the first result
            dispres(res_url)
        else:
            questions = get_questions_for_query(query)
            res_url = questions[0][2]
            dispres(sourl + res_url)  # Returned URL is relative to SO homepage
    except UnicodeEncodeError as e:
        showerror(e)
        print_warning("\n\nEncoding error: Use \"chcp 65001\" command before using socli...")
        sys.exit(0)
    except requests.exceptions.ConnectionError:
        print_fail("Please check your internet connectivity...")
    except Exception as e:
        showerror(e)
        sys.exit(0)


def helpman():
    """
    Displays help
    :return:
    """

    optionsText = make_header("Stack Overflow command line client:") + '\n' + \
        make_green("\n\n\tUsage: socli [ Arguments ] < Search Query >\n\n") + '\n' + \
        make_header("[ Arguments ] (optional):\n") + '\n' + \
        " " + bold("--help or -h") + " : Displays this help" + '\n' + \
        " " + bold("--query or -q") + \
          " : If any of the following commands are used then you " \
          "must specify search query after the query argument" + '\n' + \
        " " + bold("--interactive or -i") + " : To search in Stack Overflow" + \
                                              " and display the matching results. You can chose and " + \
                                                "browse any of the result interactively" + '\n' + \
        " " + bold("--res or -r") + \
          " : To select and display a result manually and display " + \
          "its most voted answer. \n    eg: " + \
          make_warning(("socli --res 2 --query foo bar")) + ": Displays the second search result of the query"  + \
          " \"foo bar\""  + '\n' + \
        " " + bold("--tag or -t") + \
              " : To search a query by tag on Stack Overflow.  Visit http://stackoverflow.com/tags to see the " + \
              "list of all tags." + \
              "\n    eg: " + make_warning(("socli --tag javascript,node.js --query foo bar")) + \
              ": Displays the search result of the query" + \
              " \"foo bar\" in Stack Overflow's javascript and node.js tags."  + '\n' + \
        " " + bold("--new or -n") + \
              " : Opens the Stack Overflow new questions page in your default browser. You can create a " + \
              "new question using it." + '\n' + \
        " " + bold("--user or -u") + \
              " : Displays information about the user provided as the next argument(optional). If no argument is provided" + \
              " it will ask the user to enter a default username. Now the user can run the command without the argument." + \
              "\n    eg: " + make_warning(("socli -u")) + ": Prompts and saves your username. Now you can just run " + \
              make_warning(("socli -u")) + " to see " + \
              "the stats.\n    " + make_warning(("socli -u 22656")) + ": Displays info about user ID 22656" + '\n' + \
        " " + bold("--del or -d") + \
              " : Deletes the configuration file generated by " + make_warning(("socli -u")) + " command." + '\n' + \
        " " + bold("--api or -a") + \
              " : Sets a custom API key for socli" + '\n' + \
        " " + bold("--sosearch or -s") + \
              " : SoCLI uses google search by default. Use this option to search Stack Overflow directly."

    helpText = make_header("\n\n< Search Query >:") + '\n' + \
        "\nQuery to search on Stack Overflow" + '\n' + \
        "\nIf no commands are specified then socli will search Stack " + \
              "Overflow and simply displays the first search result's " + \
              "most voted answer." + '\n' + \
        "If a command is specified then it will work according to the " + \
              "command." + '\n' + \
        make_header("\n\nExamples:\n") + '\n' + \
        '\t' + make_warning(("socli for loop in python")) + '\n' + \
        '\t' + make_warning(("socli -iq while loop in python")) + '\n' + \
        "\n\nSoCLI is an open source project hosted on github. Don't forget to star it if you liked it.\nUse GitHub" + \
              " issues to report problems: " + underline("http://github.com/gautamkrishnar/socli")

    screenHeight, screenWidth = subprocess.check_output(['stty', 'size']).split()
    subsequent_indent = '    '
    optionsText = '\n'.join(['\n'.join(textwrap.wrap(line, width=int(screenWidth) - len(subsequent_indent),
                 break_long_words=False, replace_whitespace=False, subsequent_indent=subsequent_indent))
                 for line in optionsText.splitlines() if optionsText.strip() != ''])

    helpText = '\n'.join(['\n'.join(textwrap.wrap(line, width=int(screenWidth),
                 break_long_words=False, replace_whitespace=False))
                 for line in helpText.splitlines() if helpText.strip() != ''])
    print(optionsText)
    print(helpText)


def get_questions_for_query(query, count=10):
    """
    Fetch questions for a query using stackoverflow default search mechanism.
    Returned question urls are relative to SO homepage.
    At most 10 questions are returned. (Can be altered by passing count)
    :param query: User-entered query string
    :return: list of [ (question_text, question_description, question_url) ]
    """
   
    questions = []
    randomheaders()
    
    if br==True:
        search_res = requests.get(sburl + query, headers=header)
        captchacheck(search_res.url)
        soup = BeautifulSoup(search_res.text, 'html.parser')
        try:
            soup.find_all("div", class_="question-summary")[0]  # For explicitly raising exception
        except IndexError:
            print_warning("No results found...")
            sys.exit(0)
        tmp = (soup.find_all("div", class_="question-summary"))
        i = 0
        while (i < len(tmp)):
            if i == count: break  # limiting results
            question_text = ' '.join((tmp[i].a.get_text()).split())
            question_text = question_text.replace("Q: ", "")
            q_tag = (soup.find_all("div", class_="question-summary"))[i]
            answers = [s.get_text() for s in q_tag.find_all("a", class_="post-tag")][0:]
            ques_tags = " ".join(str(x) for x in answers)
            question_local_url = tmp[i].a.get("href")
            questions.append((question_text,ques_tags, question_local_url))
            i = i + 1
    elif br==False:
        search_res = requests.get(soqurl + query, headers=header)
        captchacheck(search_res.url)
        soup = BeautifulSoup(search_res.text, 'html.parser')
        try:
            soup.find_all("div", class_="question-summary")[0]  # For explicitly raising exception
        except IndexError:
            print_warning("No results found...")
            sys.exit(0)
        tmp = (soup.find_all("div", class_="question-summary"))
        tmp1 = (soup.find_all("div", class_="excerpt"))
        i = 0
        while (i < len(tmp)):
            if i == count: break  # limiting results
            question_text = ' '.join((tmp[i].a.get_text()).split())
            question_text = question_text.replace("Q: ", "")
            question_desc = (tmp1[i].get_text()).replace("'\r\n", "")
            question_desc = ' '.join(question_desc.split())
            question_local_url = tmp[i].a.get("href")
            questions.append((question_text, question_desc, question_local_url))
            i = i + 1
        
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
    randomheaders()
    search_results = requests.get(google_search_url + query, headers=header)
    captchacheck(search_results.url)
    soup = BeautifulSoup(search_results.text, 'html.parser')
    try:
        soup.find_all("div", class_="g")[0]  # For explicitly raising exception
    except IndexError:
        print_warning("No results found...")
        sys.exit(0)
    for result in soup.find_all("div", class_="g"):
        if i == count:
            break
        try:
            question_title = result.find("h3", class_="r").get_text()[:-17]
            question_desc = result.find("span", class_="st").get_text()
            if question_desc=="": # For avoiding instant answers
                raise NameError #Explicit raising
            question_url = result.find("a").get("href") #Retrieves the Stack Overflow link
            question_url = fixGoogleURL(question_url)

            if question_url is None:
                i = i-1
                continue

            questions.append([question_title, question_desc, question_url])
            i += 1
        except NameError:
            continue
        except AttributeError:
            continue

    #Check if there are any valid question posts
    if not questions:
        print_warning("No results found...")
        sys.exit(0)
    return questions


def get_question_stats_and_answer(url):
    """
    Fetch the content of a StackOverflow page for a particular question.
    :param url: full url of a StackOverflow question
    :return: tuple of ( question_title, question_desc, question_stats, answers )
    """
    randomheaders()
    res_page = requests.get(url, headers=header)
    captchacheck(res_page.url)
    soup = BeautifulSoup(res_page.text, 'html.parser')
    question_title, question_desc, question_stats = get_stats(soup)
    answers = [s.get_text() for s in soup.find_all("div", class_="post-text")][
              1:]  # first post is question, discard it.
    if len(answers) == 0:
        answers.append('No answers for this question ...')
    return question_title, question_desc, question_stats, answers


def socli_interactive_windows(query):
    """
    Interactive mode
    :param query:
    :return:
    """
    try:
        search_res = requests.get(soqurl + query)
        captchacheck(search_res.url)
        soup = BeautifulSoup(search_res.text, 'html.parser')
        try:
            soup.find_all("div", class_="question-summary")[0]  # For explictly raising exception
            tmp = (soup.find_all("div", class_="question-summary"))
            tmp1 = (soup.find_all("div", class_="excerpt"))
            i = 0
            question_local_url = []
            print(bold("\nSelect a question below:\n"))
            while (i < len(tmp)):
                if i == 10: break  # limiting results
                question_text = ' '.join((tmp[i].a.get_text()).split())
                question_text = question_text.replace("Q: ", "")
                question_desc = (tmp1[i].get_text()).replace("'\r\n", "")
                question_desc = ' '.join(question_desc.split())
                print_warning(str(i + 1) + ". " + dispstr(question_text))
                question_local_url.append(tmp[i].a.get("href"))
                print("  " + dispstr(question_desc) + "\n")
                i = i + 1
            try:
                op = int(inputs("\nType the option no to continue or any other key to exit:"))
                while 1:
                    if (op > 0) and (op <= i):
                        dispres(sourl + question_local_url[op - 1])
                        cnt = 1  # this is because the 1st post is the question itself
                        while 1:
                            global tmpsoup
                            qna = inputs(
                                "Type " + bold("o") + " to open in browser, " + bold("n") + " to next answer, " + bold(
                                    "b") + " for previous answer or any other key to exit:")
                            if qna in ["n", "N"]:
                                try:
                                    answer = (tmpsoup.find_all("div", class_="post-text")[cnt + 1].get_text())
                                    print_green("\n\nAnswer:\n")
                                    print("-------\n" + answer + "\n-------\n")
                                    cnt = cnt + 1
                                except IndexError as e:
                                    print_warning(" No more answers found for this question. Exiting...")
                                    sys.exit(0)
                                continue
                            elif qna in ["b", "B"]:
                                if cnt == 1:
                                    print_warning(" You cant go further back. You are on the first answer!")
                                    continue
                                answer = (tmpsoup.find_all("div", class_="post-text")[cnt - 1].get_text())
                                print_green("\n\nAnswer:\n")
                                print("-------\n" + answer + "\n-------\n")
                                cnt = cnt - 1
                                continue
                            elif qna in ["o", "O"]:
                                import webbrowser
                                print_warning("Opening in your browser...")
                                webbrowser.open(sourl + question_local_url[op - 1])
                            else:
                                break
                        sys.exit(0)
                    else:
                        op = int(input("\n\nWrong option. select the option no to continue:"))
            except Exception as e:
                showerror(e)
                print_warning("\n Exiting...")
                sys.exit(0)
        except IndexError:
            print_warning("No results found...")
            sys.exit(0)

    except UnicodeEncodeError:
        print_warning("\n\nEncoding error: Use \"chcp 65001\" command before using socli...")
        sys.exit(0)
    except requests.exceptions.ConnectionError:
        print_fail("Please check your internet connectivity...")
    except Exception as e:
        showerror(e)
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
            self.questions_box = ScrollableTextBox(widgets)
            self.header = UnicodeText(('less-important', 'Select a question below:\n'))
            self.footerText = '0-' + str(len(self.questions) - 1) + ': select a question, any other key: exit.'
            self.errorText = UnicodeText.to_unicode('Question numbers range from 0-' + 
                                                    str(len(self.questions) - 1) + 
                                                    ". Please select a valid question number.")
            self.footer = UnicodeText(self.footerText)
            self.footerText = UnicodeText.to_unicode(self.footerText)
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
                except IndexError as e:
                    self.footer.set_text(self.errorText)
            elif key in {'down', 'up'}:
                self.questions_box.keypress(size, key)
            else:
                raise urwid.ExitMainLoop()

        def select_question(self, url, index):
            global question_post
            if self.cachedQuestions[index] != None:
                question_post = self.cachedQuestions[index]
                LOOP.widget = question_post
            else:
                if not google_search:
                    url = sourl + url
                question_title, question_desc, question_stats, answers = get_question_stats_and_answer(url)
                question_post = QuestionPage((answers, question_title, question_desc, question_stats, url))
                self.cachedQuestions[index] = question_post
                LOOP.widget = question_post

    global header_for_display
    global question_page
    global LOOP
    header_for_display = Header()

    try:
        if google_search:
            questions = get_questions_for_query_google(query)
        else:
            questions = get_questions_for_query(query)
        question_page = SelectQuestionPage(questions)
        LOOP = EditedMainLoop(question_page, palette)
        LOOP.run()

    except UnicodeEncodeError:
        print_warning("\n\nEncoding error: Use \"chcp 65001\" command before using socli...")
        sys.exit(0)
    except requests.exceptions.ConnectionError as e:
        print_fail("Please check your internet connectivity...")
    except Exception as e:
        showerror(e)
        print("exiting...")
        sys.exit(0)


def socl_manusearch(query, rn):
    """
    Manual search by question index
    :param query:
    :param rn:
    :return:
    """
    if rn < 1:
        print_warning(
            "Count starts from 1. Use: \"socli -i 2 -q python for loop\" for the 2nd result for the query")
        sys.exit(0)
    query = urlencode(query)
    try:
        randomheaders()
        #Set count = 99 so you can choose question numbers higher than 10
        count = 99
        res_url = None
        try:
            if google_search:
                questions = get_questions_for_query_google(query, count)
                res_url = questions[rn - 1][2]
            else:
                questions = get_questions_for_query(query, count)
                res_url = sourl + questions[rn - 1][2]
            dispres(res_url)
        except IndexError:
            print_warning("No results found...")
            sys.exit(1)
    except UnicodeEncodeError:
        print_warning("Encoding error: Use \"chcp 65001\" command before "
                      "using socli...")
        sys.exit(0)
    except requests.exceptions.ConnectionError:
        print_fail("Please check your internet connectivity...")
    except Exception as e:
        showerror(e)
        sys.exit(0)


def userpage(userid):
    """
    Stackoverflow user profile browsing
    :param userid:
    :return:
    """
    global app_data
    import stackexchange

    try:
        userid = int(userid)
    except ValueError as e:
        print_warning("\nUser ID must be an integer.")
        print(
            "\nFollow the instructions on this page to get your User ID: http://meta.stackexchange.com/a/111130")
        exit(1)

    try:
        if "api_key" not in app_data:
            app_data["api_key"] = None
        userprofile = stackexchange.Site(stackexchange.StackOverflow, app_key=app_data["api_key"]).user(userid)
        print(bold("\n User: " + userprofile.display_name.format()))
        print("\n\tReputations: " + userprofile.reputation.format())
        print_warning("\n\tBadges:")
        print("\t\t   Gold: " + str(userprofile.gold_badges))
        print("\t\t Silver: " + str(userprofile.silver_badges))
        print("\t\t Bronze: " + str(userprofile.bronze_badges))
        print("\t\t  Total: " + str(userprofile.badge_total))
        print_warning("\n\tStats:")
        total_questions = len(userprofile.questions.fetch())
        unaccepted_questions = len(userprofile.unaccepted_questions.fetch())
        accepted = total_questions - unaccepted_questions
        rate = accepted / float(total_questions) * 100
        print("\t\t Total Questions Asked: " + str(len(userprofile.questions.fetch())))
        print('\t\t        Accept rate is: %.2f%%.' % rate)
        #check if the user have answers and questions or no. 
        if userprofile.top_answer_tags.fetch():
            print('\nMost experienced on %s.' % userprofile.top_answer_tags.fetch()[0].tag_name)
        else:
            print("You have 0 answers")
        if userprofile.top_question_tags.fetch():
            print('Most curious about %s.' % userprofile.top_question_tags.fetch()[0].tag_name)
        else:
            print("You have 0 questions")
    except urllib.error.URLError:
        print_fail("Please check your internet connectivity...")
        exit(1)
    except Exception as e:
        showerror(e)
        if str(e) == "400 [bad_parameter]: `key` doesn't match a known application":
            print_warning("Wrong API key... Deleting the data file...")
            del_datafile()
            exit(1)
        elif str(e) in ("not enough values to unpack (expected 1, got 0)", "400 [bad_parameter]: ids"):
            global manual
            if manual == 1:
                print_warning("Wrong user ID specified...")
                helpman()
                exit(1)
            print_warning("Wrong user ID... Deleting the data file...")
            del_datafile()
            exit(1)

        # Reaches here when rate limit exceeds
        print_warning(
            "Stackoverflow exception. This might be caused due to the rate limiting: http://stackapps.com/questions/3055/is-there-a-limit-of-api-requests")
        print("Use http://stackapps.com/apps/oauth/register to register a new API key.")
        set_api_key()
        exit(1)


def set_api_key():
    """
    Sets a custom API Key
    :return:
    """
    global app_data
    api_key = inputs("Type an API key to continue: ")
    if len(api_key) > 0:
        app_data["api_key"] = api_key
        save_datafile()
    print_warning("\nAPI Key saved...")


def save_datafile():
    """
    Saves the app_data dictionary to a file named data_file
    :return:
    """
    # import json => Json imported globally
    global app_data
    global data_file
    with open(data_file, "w") as dataf:
        json.dump(app_data, dataf)


def load_datafile():
    """
    Loads the app_data dictionary form a file named data_file
    :return:
    """
    # import json => Json imported globally
    global app_data
    global data_file
    with open(data_file) as dataf:
        app_data = json.load(dataf)


def del_datafile():
    """
    Deletes the data file
    :return:
    """
    global data_file
    try:
        os.remove(data_file)
    except FileNotFoundError:
        print_warning("File not created.... Use socli -u to create a new configuration file.")
        exit(0)


def loaduseragents():
    """
    Loads the list of user agents from user_agents.txt
    :return:
    """
    global uas
    uas = []
    with open(os.path.join(os.path.dirname(__file__), "user_agents.txt"), 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[1:-1 - 1])
    random.shuffle(uas)


def randomheaders():
    """
    Sets header variable to a random value
    :return:
    """
    global uas
    global header
    ua = random.choice(uas)
    header = {"User-Agent": ua}


def wrongsyn(query):
    """
    Exits if query value is empty
    :param query:
    :return:
    """
    if query == "":
        print_warning("Wrong syntax!...\n")
        helpman()
        sys.exit(1)
    else:
        return


def get_stats(soup):
    """
    Get Question stats
    :param soup:
    :return:
    """
    question_title = (soup.find_all("a", class_="question-hyperlink")[0].get_text())
    question_stats = (soup.find_all("span", class_="vote-count-post")[0].get_text())
    try:
        question_stats = "Votes " + question_stats + " | " + (((soup.find_all("div", class_="module question-stats")[0]
                                                                .get_text()).replace("\n", " ")).replace("     "," | "))
    except IndexError as e:
        question_stats = "Could not load statistics."
    question_desc = (soup.find_all("div", class_="post-text")[0])
    add_urls(question_desc)
    question_desc = question_desc.get_text()
    question_stats = ' '.join(question_stats.split())
    return question_title, question_desc, question_stats


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


def hastags():
    """
    Gets the tags and adds them to query url
    :return:
    """
    global soqurl
    global tag
    for tags in tag:
        soqurl = soqurl + "[" + tags + "]" + "+"


def dispres(url):
    """
    Display result page
    :param url: URL of the search result
    :return:
    """
    global question_post
    global header_for_display
    global LOOP
    randomheaders()
    res_page = requests.get(url, headers=header)
    captchacheck(res_page.url)
    header_for_display = Header()
    question_title, question_desc, question_stats, answers = get_question_stats_and_answer(url)
    question_post = QuestionPage((answers, question_title, question_desc, question_stats, url))
    LOOP = EditedMainLoop(question_post, palette)
    LOOP.run()



def fixGoogleURL(url):
    """
    Fixes the url extracted from HTML when
    performing a google search
    :param url:
    :return: Correctly formatted URL to be used in requests.get
    """
    if "&sa=" in url:
        url=url.split("&")[0]
    if "/url?q=" in url[0:7]:
        url = url[7:] #Removes the "/url?q=" prefix

    if url[:30] == "http://www.google.com/url?url=": #Used to get rid of this header and just retrieve the Stack Overflow link
        url = url[30:]

    if "http" not in url[:4]:
        url = "https://" + url #Add the protocol if it doesn't already exist

    #Makes sure that we stay in the questions section of Stack Overflow
    if not bool(re.search("/questions/[0-9]+", url)) and not bool(re.search("\.com/a/[0-9]", url)):
        return None

    if url[:17] == "https:///url?url=": #Resolves rare bug in which this is a prefix
        url = url[17:]

    return url


def captchacheck(url):
    """
    Exits program when their is a captcha. Prevents errors.
    Users will have to manually verify their identity.
    :param url: URL of stackoverflow
    :return:
    """
    if google_search:
        googleErrorDisplayMessage = "Google thinks you're a bot because you're issuing too many queries too quickly! " + \
                                    "Now you'll have to wait about an hour before you're unblocked... :(. Use the -s tag " + \
                                    "to search via Stack Overflow instead."
        #Check if google detects user as a bot
        if re.search("ipv4\.google\.com/sorry", url):
            print_warning(googleErrorDisplayMessage)
            exit(0)
    else:
        if re.search("\.com/nocaptcha", url): # Searching for stackoverflow captcha check
            print_warning("StackOverflow captcha check triggered. Please wait a few seconds before trying again.")
            exit(0)

def retrieveSavedProfile():
    """
    Retrieves the user's saved profile after a "socli -u" command.
    Asks the user to enter a User ID and saves it if a previous file is not found.

    :return: The user's ID as an integer
    """
    global data_file
    global app_data
    user = None
    try:
        load_datafile()
        if "user" in app_data:
            user = app_data["user"]
        else:
            raise FileNotFoundError  # Manually raising to get value
    except JSONDecodeError:
        # This maybe some write failures
        del_datafile()
        print_warning("Error in parsing the data file, it will be now deleted. Please rerun the "
                      "socli -u command.")
        exit(1)
    except FileNotFoundError:
        print_warning("Default user not set...\n")
        try:
            # Code to execute when first time user runs socli -u
            app_data['user'] = int(inputs("Enter your Stackoverflow User ID: "))
            save_datafile()
            user = app_data['user']
            print_green("\nUserID saved...\n")
        except ValueError:
            print_warning("\nUser ID must be an integer.")
            print(
                "\nFollow the instructions on this page to get your User ID: http://meta.stackexchange.com/a/111130")
            exit(1)
    return user

def parseArguments(command):
    """
    Parses the command into arguments and flags
    :param command: the command in list form
    :return: an object that contains the values for all arguments

    Currently, all help messages are not in use and helpman() is the default.
    Need to implement nicer --help format in the future.
    """
    parser = argparse.ArgumentParser(description=textwrap.dedent('Stack Overflow command line client'), add_help=False)

    #Comment this line out if you want to use argparse's default help function
    parser.add_argument('--help', '-h', action='store_true', help='Show this help message and exit')

    #Flags that return true if present and false if not
    parser.add_argument('--new', '-n', action='store_true', help=textwrap.dedent("Opens the stack overflow new questions page in your "
                                                                "default browser. You can create a new question using it."))
    parser.add_argument('--interactive', '-i', action='store_true', help=textwrap.dedent("To search in Stack Overflow and display the matching results. You can choose and browse any of the results interactively"))
    parser.add_argument('--debug', action='store_true', help="Turn debugging mode on")
    parser.add_argument('--sosearch', '-s', action='store_true', help="Searches directly on Stack Overflow instead of using Google")
    parser.add_argument('--api', '-a', action='store_true', help="Sets a custom API key for socli")
    parser.add_argument('--delete', '-d', action='store_true', help="Deletes the configuration file generated by socli -u command")

    
    #Accepts 1 argument. Returns None if flag is not present and
    #'STORED_USER' if flag is present, but no argument is supplied
    parser.add_argument('--user', '-u', nargs='?', const='(RANDOM_STRING_CONSTANT)', type=str, help="Displays information about the user "
                                                                            "provided as the next argument(optional). If no argument is provided "
                                                                            "it will ask the user to enter a default username. Now the user "
                                                                            "can run the command without the argument")

    #Accepts one or more arguments
    parser.add_argument('--tag', '-t', nargs='+', help="To search a query by tag on stack overflow."
                                                      "Visit http://stackoverflow.com/tags to see the list of all tags."
                                                      "\n   eg:- socli --tag javascript,node.js --query "
                                                      "foo bar: Displays the search result of the query"
                                                      " \"foo bar\" in stack overflow's javascript and node.js tags")
    parser.add_argument('--query', '-q', nargs='+', default=[], help="If any of the following commands are used then you " \
          "must specify this option and a query following it.")
    parser.add_argument('--browse', '-b', nargs='+', default=[], help="Searches for ten hot,week and interesting questions on today's page ")
    #Accepts 0 or more arguments. Used to catch query if no flags are present
    parser.add_argument('userQuery', nargs='*', help=argparse.SUPPRESS)

    #Accepts 1 argument
    parser.add_argument('--res', '-r', type=int, help="To select and display a result manually and display "
                                                  "its most voted answer. \n   eg:- socli --res 2 --query "
                                                  "foo bar: Displays the second search result of the query"
                                                  " \"foo bar\"'s most voted answer")

    namespace = parser.parse_args(command)
    return namespace


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
            self.questions_box = ScrollableTextBox(widgets)
            self.header = UnicodeText(('less-important', 'Select a question below:\n'))
            self.footerText = '0-' + str(len(self.questions) - 1) + ': select a question, any other key: exit.'
            self.errorText = UnicodeText.to_unicode('Question numbers range from 0-' + 
                                                    str(len(self.questions) - 1) + 
                                                    ". Please select a valid question number.")
            self.footer = UnicodeText(self.footerText)
            self.footerText = UnicodeText.to_unicode(self.footerText)
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
                except IndexError as e:
                    self.footer.set_text(self.errorText)
            elif key in {'down', 'up'}:
                self.questions_box.keypress(size, key)
            else:
                raise urwid.ExitMainLoop()

        def select_question(self, url, index):
            global question_post
            if self.cachedQuestions[index] != None:
                question_post = self.cachedQuestions[index]
                LOOP.widget = question_post
            else:
                if not google_search:
                    url = sourl + url
                question_title, question_desc, question_stats, answers = get_question_stats_and_answer(url)
                question_post = QuestionPage((answers, question_title, question_desc, question_stats, url))
                self.cachedQuestions[index] = question_post
                LOOP.widget = question_post

    global header_for_display
    global question_page
    global LOOP
    header_for_display = Header()

    try:
        if google_search:
            questions = get_questions_for_query_google(query)
        else:
            #print('hurr')
            questions = get_questions_for_query(query_tag)
            #print(questions)  

        question_page = SelectQuestionPage(questions)

        LOOP = EditedMainLoop(question_page, palette)
        LOOP.run()

    except UnicodeEncodeError:
        print_warning("\n\nEncoding error: Use \"chcp 65001\" command before using socli...")
        sys.exit(0)
    except requests.exceptions.ConnectionError as e:
        print_fail("Please check your internet connectivity...")
    except Exception as e:
        showerror(e)
        #print("Hurra")
        print("exiting...")
        sys.exit(0)

    except UnicodeEncodeError:
        print_warning("\n\nEncoding error: Use \"chcp 65001\" command before using socli...")
        sys.exit(0)
    except requests.exceptions.ConnectionError:
        print_fail("Please check your internet connectivity...")
    except Exception as e:
        showerror(e)
        sys.exit(0)


def main():
    """
    The main logic for how options in a command is checked.
    """

    global query
    global google_search
    namespace = parseArguments(sys.argv[1:])
    loaduseragents() #Populates the user agents array
    query_tag=' '.join(namespace.browse)
    #print (namespace.userQuery)
    query = ' '.join(namespace.query) + ' ' + ' '.join(namespace.userQuery)
    #print(query1)

    if namespace.help:
        helpman()
        sys.exit(0)
    if namespace.debug: #If --debug flag is present
        global DEBUG
        DEBUG = True
    if namespace.new: #If --new flag is present
        import webbrowser
        print_warning("Opening stack overflow in your browser...")
        webbrowser.open(sourl + "/questions/ask")
        sys.exit(0)
    if namespace.api: #If --api flag is present
        set_api_key()
        sys.exit(0)
    if namespace.user != None: #If --user flag is present
        # Stackoverflow user profile support
        user = None
        if namespace.user != '(RANDOM_STRING_CONSTANT)': #If user provided a user ID
            global manual  # Manual mode from command line
            manual = 1
            user = namespace.user
        else: #If user did not provide a user id
            user = retrieveSavedProfile()
        userpage(user)
        sys.exit(0)
    if namespace.delete: #If --delete flag is present
        del_datafile()
        print_warning("Data files deleted...")
        sys.exit(0)
    if namespace.sosearch: #If --sosearch flag is present
        google_search = False
    if namespace.tag: #If --tag flag is present
        global tag
        google_search = False
        tag = namespace.tag
        hastags()
    if namespace.res != None: #If --res flag is present
        questionNumber = namespace.res
        if namespace.query != [] or namespace.tag != None: #There must either be a tag or a query
            socl_manusearch(query, questionNumber)
        else:
            print_warning('You must specify a query or a tag. For example, use: "socli -r 3 -q python for loop" '
                'to retrieve the third result when searching about "python for loop". You can also use "socli -r 3 -t python" '
                'to retrieve the third result when searching for posts with the "python" tag.')
    if namespace.browse:
            google_search=False
            socli_browse_interactive(query_tag)
    elif namespace.query != [] or namespace.tag != None: #If query and tag are not both empty
        if namespace.interactive:
            socli_interactive(query)   
        else:
            socli(query)
    elif query != ' ' and not (namespace.tag or namespace.res or namespace.interactive or namespace.browse): #If there are no flags
        socli(query)
    else:
        #Help text for interactive mode
        if namespace.interactive and namespace.query == [] and namespace.tag == None:
            print_warning('You must specify a query or a tag. For example, use: "socli -iq python for loop" '
                'to search about "python for loop" in interactive mode. You can also use "socli -it python" '
                'to search posts with the "python" tag in interactive mode.')
        else:
            helpman()

if __name__ == '__main__':
    main()
