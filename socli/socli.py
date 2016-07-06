# Stack overflow CLI
# Created by Gautam krishna R : www.github.com/gautamkrishnar

import getopt
import os
import sys
import urllib

import requests
from bs4 import BeautifulSoup

# Global vars:
DEBUG = True # Set True for enabling debugging
soqurl = "http://stackoverflow.com/search?q="  # Query url
sourl = "http://stackoverflow.com"  # Site url
rn = -1  # Result number (for -r and --res)
ir = 0  # interactive mode off (for -i arg)
query = ""


### To support python 2:
if sys.version < '3.0.0':
    def urlencode(inp):
        return urllib.quote_plus(inp)
    def dispstr(inp):
        return inp.encode('utf-8')
    def inputs(str):
        return raw_input(str)
else:
    def urlencode(inp):
        return urllib.parse.quote_plus(inp)
    def dispstr(inp):
        return inp
    def inputs(str):
        return input(str)

### To implement colors:
# From https://github.com/django/django/blob/master/django/core/management/color.py
def supports_color():
    """
    Returns True if the running system's terminal supports color,
    and False otherwise.
    """
    plat = sys.platform
    supported_platform = plat != 'Pocket PC' and (plat != 'win32' or 'ANSICON' in os.environ)
    # To detect windows 10 cmd. Windows 10 cmd supports color by default
    if os.name == "nt":
        x = sys.getwindowsversion()[0]
        if x == 10:
            try:
                test_shell = os.environ['SHELL']  # If running with a shell like cygwin this is set
            except Exception:
                return True
    # isatty is not always implemented, #6223.
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    if not supported_platform or not is_a_tty:
        return False
    return True


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def format_str(str, color):
    _color = color if supports_color() else ''
    _endc = bcolors.ENDC if supports_color() else ''
    return "{0}{1}{2}".format(_color, str, _endc)


def print_header(str):
    print(format_str(str, bcolors.HEADER))


def print_blue(str):
    print(format_str(str, bcolors.OKBLUE))


def print_green(str):
    print(format_str(str, bcolors.OKGREEN))


def print_warning(str):
    print(format_str(str, bcolors.WARNING))


def print_fail(str):
    print(format_str(str, bcolors.FAIL))


def bold(str):
    return (format_str(str, bcolors.BOLD))


def underline(str):
    return (format_str(str, bcolors.UNDERLINE))

## For testing exceptions
def showerror(e):
    if DEBUG == True:
        import traceback
        print("Error name: "+ e.__doc__)
        print()
        print("Description: "+str(e))
        print()
        traceback.print_exc()
    else:
        return


### SOCLI Code
# @param searchquery = Query to search on stackoverflow
def socli(query):
    query = urlencode(query)
    try:
        search_res = requests.get(soqurl + query, verify=False)
        soup = BeautifulSoup(search_res.text, 'html.parser')
        try:
            res_url = sourl + (soup.find_all("div", class_="question-summary")[0].a.get('href'))
        except IndexError:
            print_warning("No results found...")
            sys.exit(0)
        dispres(res_url)
    except UnicodeEncodeError as e:
        showerror(e)
        print_warning("\n\nEncoding error: Use \"chcp 65001\" command before using socli...")
        sys.exit(0)
    except requests.exceptions.ConnectionError:
        print_fail("Please check your internet connectivity...")
    except Exception as e:
        showerror(e)
        sys.exit(0)

# Displays help
def helpman():
    print_header("Stack Overflow command line client:")
    print_green("\n\n\tUsage: socli [ Arguments ] < Search Query >\n\n")
    print_header("\n[ Arguments ] (optional):\n")
    print(" " + bold("--help or -h") + " : Displays this help")
    print(" " + bold("--query or -q") +
          " : If any of the following commands are used then you " \
          "must specify search query after the query argument")
    print(" " + bold("--interactive or -i") + " : To search in stack overflow"
                                              " and display the matching results. You can chose and "
                                              "browse any of the result interactively")
    print(" " + bold("--res or -r") +
          " : To select and display a result manually and display "
          "its most voted answer. \n   eg:- socli --res 2 -query "
          "foo bar: Displays the second search result of the query"
          " \"foo bar\"'s most voted answer")
    print_header("\n\n< Search Query >:")
    print("\n Query to search on Stack overflow")
    print("\nIf no commands are specified then socli will search the stack "
          "overfow and simply displays the first search result's "
          "most voted answer.")
    print("If a command is specified then it will work according to the "
          "command.")
    print_header("\n\nExamples:\n")
    print(bold("socli") + " for loop in python")
    print(bold("socli -iq") + " while loop in python")


# Interactive mode:
def socli_interactive(query):
    try:
        search_res = requests.get(soqurl + query, verify=False)
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
                question_text = question_text.replace("Q: ","")
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
                            qna = inputs("Type " + bold("o") + " to open in browser, " + bold("n") + " to next answer, "+ bold("b") + " for previous answer or any other key to exit:")
                            if qna in ["n", "N"]:
                                try:
                                    answer = (tmpsoup.find_all("div",class_="post-text")[cnt + 1].get_text())
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
                                answer = (tmpsoup.find_all("div",class_="post-text")[cnt + 1].get_text())
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
            sys.exit(1)

    except UnicodeEncodeError:
        print_warning("\n\nEncoding error: Use \"chcp 65001\" command before using socli...")
        sys.exit(0)
    except requests.exceptions.ConnectionError:
        print_fail("Please check your internet connectivity...")
    except Exception as e:
        showerror(e)
        sys.exit(0)


# Manual search by question index
def socl_manusearch(query, rn):
    query = urlencode(query)
    try:
        search_res = requests.get(soqurl + query, verify=False)
        soup = BeautifulSoup(search_res.text, 'html.parser')
        try:
            res_url = sourl + (soup.find_all("div", class_="question-summary")[rn - 1].a.get('href'))
        except IndexError:
            print_warning("No results found...")
            sys.exit(1)
        dispres(res_url)
    except UnicodeEncodeError:
        print_warning("Encoding error: Use \"chcp 65001\" command before "
                      "using socli...")
        sys.exit(0)
    except requests.exceptions.ConnectionError:
        print_fail("Please check your internet connectivity...")
    except Exception as e:
        showerror(e)
        sys.exit(0)


# print(e.__doc__)


# Exits if query value is empty
def wrongsyn(query):
    if query == "":
        print_warning("Wrong syntax!...\n")
        helpman()
        sys.exit(1)
    else:
        return


# Get Question stats
def get_stats(soup):
    question_tittle = (soup.find_all("a",class_="question-hyperlink")[0].get_text())
    question_stats = (soup.find_all("span",class_="vote-count-post")[0].get_text())
    question_stats = "Votes " + question_stats + " | " + (((soup.find_all("div",\
                        class_="module question-stats")[0].get_text()).replace("\n", " ")).replace("     "," | "))
    question_desc = (soup.find_all("div", class_="post-text")[0])
    add_urls(question_desc)
    question_desc = question_desc.get_text()
    question_stats = ' '.join(question_stats.split())
    return question_tittle, question_desc, question_stats


def add_urls(tags):
    """
    Adds the URL to any hyperlinked text found in a question
    or answer.
    """
    images = tags.find_all("a")

    for image in images:
        if hasattr(image, "href"):
            image.string = "{} [{}]".format(image.text, image['href'])


# Display result page
def dispres(url):
    res_page = requests.get(url + query, verify=False)
    soup = BeautifulSoup(res_page.text, 'html.parser')
    question_tittle, question_desc, question_stats = get_stats(soup)
    print_warning("\nQuestion: " + dispstr(question_tittle))
    print(dispstr(question_desc))
    print("\t" + underline(question_stats))
    try:
        answer = (soup.find_all("div", class_="post-text"))[1]
        add_urls(answer)
        answer = (soup.find_all("div", class_="post-text")[1].get_text())
        global tmpsoup
        tmpsoup = soup
        print_green("\n\nAnswer:\n")
        print("-------\n" + dispstr(answer) + "\n-------\n")
        return
    except IndexError as e:
        print_warning("\n\nAnswer:\n\t No answer found for this question...")
        sys.exit(0);


# Main
def main():
    global rn  # Result number (for -r and --res)
    global ir  # interactive mode off (for -i arg)
    global query
    # IF there is no command line options or if it is help argument:
    if (len(sys.argv) == 1) or ((sys.argv[1] == "-h") or (sys.argv[1] == "--help")):
        helpman()
        sys.exit(0)
    else:
        try:
            options, rem = getopt.getopt(sys.argv[1:],"nir:q:", ["query=", "res=", "interactive=", "new"])
        except getopt.GetoptError:
            helpman()
            sys.exit(1)

        # Gets the CL Args
        if 'options' in locals():
            for opt, arg in options:
                if opt in ("-i", "--interactive"):
                    ir = 1  # interactive mode on
                if opt in ("-r", "--res"):
                    try:
                        rn = int(arg)
                    except ValueError:
                        print_warning("Wrong syntax...!\n")
                        helpman()
                        sys.exit(0)
                if opt in ("-q", "--query"):
                    query = arg
                    if len(rem) > 0:
                        query = query + " " + " ".join(rem)
                if opt in ("-n", "--new"):
                    import webbrowser
                    print_warning("Opening stack overflow in your browser...")
                    webbrowser.open(sourl + "/questions/ask")
                    sys.exit(0)
        if (rn == -1) and (ir == 0):
            socli(" ".join(sys.argv[1:]))
            sys.exit(0)
        elif (rn > 0):
            wrongsyn(query)
            socl_manusearch(query, rn)
            sys.exit(0)
        elif (rn == 0):
            print_warning("Count starts from 1. Use: \"socli -i 2 -q python for loop\" for the 2nd result for the query")
            sys.exit(0)
        elif (ir == 1):
            wrongsyn(query)
            socli_interactive(query)
            sys.exit(0)
        else:
            print_warning("Wrong syntax...!\n")
            helpman()
            sys.exit(0)


if __name__ == '__main__':
    main()
