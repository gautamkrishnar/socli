# Stack overflow CLI
# Created by Gautam krishna R : www.github.com/gautamkrishnar
import sys, urllib, getopt, requests
from bs4 import BeautifulSoup

# Global vars:
DEBUG = False
soqurl = "http://stackoverflow.com/search?q="  # Query url
sourl = "http://stackoverflow.com"  # Site url
rn = -1  # Result number (for -r and --res)
ir = 0  # interactive mode off (for -i arg)
query = ""

# @param searchquery = Query to search on stackoverflow
def socli(query):
    query = urllib.parse.quote_plus(query)
    try:
        search_res = requests.get(soqurl+query, verify=False)
        soup = BeautifulSoup(search_res.text, 'html.parser')
        try:
            res_url = sourl + (soup.find_all("div", class_="question-summary")[0].a.get('href'))
        except IndexError:
            print("No results found...")
            sys.exit(1)
        dispres(res_url)
    except Exception as e:
        print("Please check your internet connectivity...")
        sys.exit(1)
#        print(e.__doc__)
#        print(e.message)

# Displays help
def helpman():
    print("Stack Overflow command line client:")
    print("\n\n\tUsage: socli [ Arguments ] < Search Query >\n\n")
    print("\n[ Arguments ] (optional):\n")
    print("--help or -h: Displays this help")
    print(
        "--query or -q: If any of the following commands are used then you must specify search query after the query argument")
    print(
        "--interactive or -i: To search in stack overflow and display the matching results. You can chose and browse any of the"
        " result interactively")
    print("--res or -r: To select and display a result manually and display its most voted answer. eg:- socli --res 2 "
          "-query foo bar: Displays the second search result of the query \"foo bar\"'s most voted answer")
    print("\n\n< Search Query >:")
    print("\n Query to search on Stack overflow")
    print("\nIf no commands are specified then socli will search the stack overfow and simply displays the"
          " first search result's most voted answer.")
    print("If a command is specified then it will work according to the command.")
    print("\n\nExamples:")
    print("\nsocli for loop in python")
    print("socli -iq while loop in python")


# Interactive mode:
def socli_interactive(query):
    try:
        search_res = requests.get(soqurl + query, verify=False)
        soup = BeautifulSoup(search_res.text, 'html.parser')
        try:
            soup.find_all("div", class_="question-summary")[0] # For explictly raising exception
            tmp=(soup.find_all("div", class_="question-summary"))
            tmp1 = (soup.find_all("div", class_="excerpt"))
            i=0
            question_local_url=[]
            print("\nSelect a question below:\n")
            while (i<len(tmp)):
                if i == 10: break  # limiting results
                question_text=' '.join((tmp[i].a.get_text()).split())
                question_desc=(tmp1[i].get_text()).replace("'\r\n","")
                question_desc=' '.join(question_desc.split())
                print(str(i+1)+"."+question_text.replace("Q: ",""))
                question_local_url.append(tmp[i].a.get("href"))
                print("  "+question_desc)
                print()

                i=i+1
            try:
                op=int(input("\n\nType the option no to continue:"))
                while 1:
                    if (op>0) and (op<=i):
                        dispres(sourl+question_local_url[op-1])
                        sys.exit(0)
                    else:
                        op = int(input("\n\nWrong option. select the option no to continue;"))
            except Exception:
                print("\n Type a number... Exiting...")
                sys.exit(1)
        except IndexError:
            print("No results found...")
            sys.exit(1)

    except UnicodeEncodeError:
        print("\n\nEncoding error: Use \"chcp 65001\" command before using socli...")
        sys.exit(0)
    except Exception as e:
        print("Please check your internet connectivity...")
        sys.exit(1)
#        print(e.__doc__)


# Manual search by question index
def socl_manusearch(query, rn):
    query = urllib.parse.quote_plus(query)
    try:
        search_res = requests.get(soqurl + query, verify=False)
        soup = BeautifulSoup(search_res.text, 'html.parser')
        try:
            res_url = sourl + (soup.find_all("div", class_="question-summary")[rn-1].a.get('href'))
        except IndexError:
            print("No results found...")
            sys.exit(1)
        dispres(res_url)
    except UnicodeEncodeError:
        print("Encoding error: Use \"chcp 65001\" command before using socli...")
        sys.exit(0)
    except Exception as e:
        print("Please check your internet connectivity...")
        sys.exit(1)
#        print(e.__doc__)


# Exits if query value is empty
def wrongsyn(query):
    if query == "":
        print("Wrong syntax!...\n")
        helpman()
        sys.exit(1)
    else:
        return

# Display result page
def dispres(url):
    res_page = requests.get(url + query, verify=False)
    soup = BeautifulSoup(res_page.text, 'html.parser')
    question_tittle=(soup.find_all("a", class_="question-hyperlink")[0].get_text())
    question_stats=(soup.find_all("span", class_="vote-count-post")[0].get_text())
    question_stats = "Votes "+question_stats + " | " + (((soup.find_all("div", class_="module question-stats")[0].get_text()).replace("\n", " ")).replace("     "," | "))
    question_desc=(soup.find_all("div", class_="post-text")[0].get_text())
    question_stats=' '.join(question_stats.split())
    print("\nQuestion: " + question_tittle)
    print(question_desc)
    print("\t"+question_stats)
    try:
        answer = (soup.find_all("div", class_="post-text")[1].get_text())
        print("\n\nAnswer:\n"+answer)
        return
    except IndexError as e:
        print("\n\nAnswer:\n\t No answer found for this question...")
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
            options, rem = getopt.getopt(sys.argv[1:], "ir:q:", ["query=", "res=", "interactive="])
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
                        print("Wrong syntax...!\n")
                        helpman()
                        sys.exit(0)
                if opt in ("-q", "--query"):
                    query = arg
                    if len(rem) > 0:
                        query = query + " " + " ".join(rem)

        if (rn == -1) and (ir == 0):
            socli(" ".join(sys.argv[1:]))
            sys.exit(0)
        elif (rn > 0):
            wrongsyn(query)
            socl_manusearch(query, rn)
            sys.exit(0)
        elif (rn==0):
            print("Count starts from 1. Use: \"socli -i 2 -q python for loop\" for the 2nd result for the query")
            sys.exit(0)
        elif (ir == 1):
            wrongsyn(query)
            socli_interactive(query)
            sys.exit(0)
        else:
            print("Wrong syntax...!\n")
            helpman()
            sys.exit(0)
