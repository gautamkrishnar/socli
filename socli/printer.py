"""
Contains all functions used for printing.
Uses colorama for formatting.
"""

import subprocess
import sys
import textwrap
import urllib

import colorama
import requests

from socli import search as search, tui as tui

DEBUG = False

# Bold and underline are not supported by colorama.
_BOLD = '\033[1m'
_UNDERLINE = '\033[4m'

palette = [('answer', 'default', 'default'),
           ('title', 'light green, bold', 'default'),
           ('heading', 'light green, bold', 'default'),
           ('metadata', 'dark green', 'default'),
           ('less-important', 'dark gray', 'default'),
           ('warning', 'yellow', 'default')
           ]

if sys.version < '3.0.0':
    global FileNotFoundError
    FileNotFoundError = IOError

    def urlencode(inp):
        return urllib.quote_plus(inp)

    def display_str(inp):
        return inp.encode('utf-8')

    def inputs(str=""):
        sys.stdout.write(str)
        tempx = raw_input()
        return tempx
else:
    def urlencode(inp):
        return urllib.parse.quote_plus(inp)

    def display_str(inp):
        return inp

    def inputs(str=""):
        sys.stdout.write(str)
        tempx = input()
        return tempx


def format_str(string, color):
    return "{0}{1}{2}".format(color, string, colorama.Style.RESET_ALL)


def print_header(string):
    print(format_str(string, colorama.Fore.MAGENTA))


def print_blue(string):
    print(format_str(string, colorama.Fore.BLUE))


def print_green(string):
    print(format_str(string, colorama.Fore.GREEN))


def print_warning(string):
    print(format_str(string, colorama.Fore.YELLOW))


def print_fail(string):
    print(format_str(string, colorama.Fore.RED))


def print_white(string):
    print(format_str(string, colorama.Fore.WHITE))


def make_header(string):
    return format_str(string, colorama.Fore.MAGENTA)


def make_blue(string):
    return format_str(string, colorama.Fore.BLUE)


def make_green(string):
    return format_str(string, colorama.Fore.GREEN)


def make_warning(string):
    return format_str(string, colorama.Fore.YELLOW)


def make_fail(string):
    return format_str(string, colorama.Fore.RED)


def make_white(string):
    return format_str(string, colorama.Fore.WHITE)


def bold(string):
    return format_str(string, _BOLD)


def underline(string):
    return format_str(string, _UNDERLINE)


# For testing exceptions
def showerror(e):
    if DEBUG:
        import traceback
        print("Error name: " + e.__doc__)
        print()
        print("Description: " + str(e))
        print()
        traceback.print_exc()
    else:
        return


def helpman():
    """
    Displays help
    :return:
    """

    options_text = make_header("Stack Overflow command line client:") + '\n' + \
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
                   make_warning(
                       "socli --res 2 --query foo bar") + ": Displays the second search result of the query" + \
                   " \"foo bar\"" + '\n' + \
                   " " + bold("--tag or -t") + \
                   " : To search a query by tag on Stack Overflow.  Visit http://stackoverflow.com/tags to see the " + \
                   "list of all tags." + \
                   "\n    eg: " + make_warning("socli --tag javascript,node.js --query foo bar") + \
                   ": Displays the search result of the query" + \
                   " \"foo bar\" in Stack Overflow's javascript and node.js tags." + '\n' + \
                   " " + bold("--new or -n") + \
                   " : Opens the Stack Overflow new questions page in your default browser. You can create a " + \
                   "new question using it." + '\n' + \
                   " " + bold("--user or -u") + \
                   " : Displays information about the user provided as the next argument(optional). " \
                   "If no argument is provided it will ask the user to enter a default username. " \
                   "Now the user can run the command without the argument." + \
                   "\n    eg: " + make_warning(
        "socli -u") + ": Prompts and saves your username. Now you can just run " + \
                   make_warning("socli -u") + " to see " + \
                   "the stats.\n    " + make_warning(
        "socli -u 22656") + ": Displays info about user ID 22656" + '\n' + \
                   " " + bold("--del or -d") + \
                   " : Deletes the configuration file generated by " + make_warning("socli -u") + " command." + '\n' + \
                   " " + bold("--api or -a") + \
                   " : Sets a custom API key for socli" + '\n' + \
                   " " + bold("--sosearch or -s") + \
                   " : SoCLI uses google search by default. Use this option to search Stack Overflow directly." + '\n' \
                   " " + bold("--open-url or -o") + \
                   " : Opens the given url in socli " +  '\n'

    help_text = make_header("\n\n< Search Query >:") + '\n' + \
               "\nQuery to search on Stack Overflow" + '\n' + \
               "\nIf no commands are specified then socli will search Stack " + \
               "Overflow and simply displays the first search result's " + \
               "most voted answer." + '\n' + \
               "If a command is specified then it will work according to the " + \
               "command." + '\n' + \
               make_header("\n\nExamples:\n") + '\n' + \
               '\t' + make_warning("socli for loop in python") + '\n' + \
               '\t' + make_warning("socli -iq while loop in python") + '\n' + \
               "\n\nSoCLI is an open source project hosted on github. Don't forget to star it if you liked it.\nUse GitHub" + \
               " issues to report problems: " + underline("http://github.com/gautamkrishnar/socli")

    screen_height, screen_width = subprocess.check_output(['stty', 'size']).split()
    subsequent_indent = '    '
    options_text = '\n'.join(['\n'.join(textwrap.wrap(line, width=int(screen_width) - len(subsequent_indent),
                                                      break_long_words=False, replace_whitespace=False,
                                                      subsequent_indent=subsequent_indent))
                              for line in options_text.splitlines() if options_text.strip() != ''])

    help_text = '\n'.join(['\n'.join(textwrap.wrap(line, width=int(screen_width),
                                                  break_long_words=False, replace_whitespace=False))
                          for line in help_text.splitlines() if help_text.strip() != ''])
    print(options_text)
    print(help_text)


def display_results(url):
    """
    Display result page
    :param url: URL of the search result
    :return:
    """
    search.random_headers()
    res_page = requests.get(url, headers=search.header)
    search.captcha_check(res_page.url)
    tui.display_header = tui.Header()
    question_title, question_desc, question_stats, answers, dup_url = search.get_question_stats_and_answer(url)
    tui.question_post = tui.QuestionPage((answers, question_title, question_desc, question_stats, url, dup_url))
    tui.MAIN_LOOP = tui.EditedMainLoop(tui.question_post, palette)
    tui.MAIN_LOOP.run()
