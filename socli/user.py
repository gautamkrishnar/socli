"""
Contains all functions used for user authentication and user metadata fetching.
"""

import json
import os

import socli.printer as pr

app_data = dict()  # Data file dictionary
data_file = os.path.join(os.path.dirname(__file__), "data.json")  # Data file location


def user_page(user_id):
    """
    Stack Overflow user profile browsing
    :param user_id:
    :return:
    """
    global app_data
    import stackexchange

    try:
        user_id = int(user_id)
    except ValueError:
        pr.print_warning("\nUser ID must be an integer.")
        print(
            "\nFollow the instructions on this page to get your User ID: http://meta.stackexchange.com/a/111130")
        exit(1)

    try:
        from urllib.error import URLError
    except ImportError:
        from urllib import URLError
    try:
        user_id = int(user_id)
    except ValueError:
        pr.print_warning("\nUser ID must be an integer.")
        print(
            "\nFollow the instructions on this page to get your User ID: http://meta.stackexchange.com/a/111130")
        exit(1)

    try:
        if "api_key" not in app_data:
            app_data["api_key"] = None
        userprofile = stackexchange.Site(stackexchange.StackOverflow, app_key=app_data["api_key"]).user(user_id)
        print(pr.bold("\n User: " + userprofile.display_name.format()))
        print("\n\tReputations: " + userprofile.reputation.format())
        pr.print_warning("\n\tBadges:")
        print("\t\t   Gold: " + str(userprofile.gold_badges))
        print("\t\t Silver: " + str(userprofile.silver_badges))
        print("\t\t Bronze: " + str(userprofile.bronze_badges))
        print("\t\t  Total: " + str(userprofile.badge_total))
        pr.print_warning("\n\tStats:")
        total_questions = len(userprofile.questions.fetch())
        unaccepted_questions = len(userprofile.unaccepted_questions.fetch())
        accepted = total_questions - unaccepted_questions
        print("\t\t Total Questions Asked: " + str(len(userprofile.questions.fetch())))
        try:
            # the following division might raise ZeroDivisionError if
            # total_questions is zero, so we wrap it in try-except.
            rate = accepted / float(total_questions) * 100
            print('\t\t        Accept rate is: %.2f%%.' % rate)
        except ZeroDivisionError:
            pass # if total_question is zero we don't print accept rate.

        # check if the user have answers and questions
        if userprofile.top_answer_tags.fetch():
            print('\nMost experienced on %s.' % userprofile.top_answer_tags.fetch()[0].tag_name)
        else:
            print("You have 0 answers")
        if userprofile.top_question_tags.fetch():
            print('Most curious about %s.' % userprofile.top_question_tags.fetch()[0].tag_name)
        else:
            print("You have 0 questions")
    except URLError:
        pr.print_fail("Please check your internet connectivity...")
        exit(1)
    except Exception as e:
        pr.showerror(e)
        if str(e) == "400 [bad_parameter]: `key` doesn't match a known application":
            pr.print_warning("Wrong API key... Deleting the data file...")
            del_datafile()
            exit(1)
        elif str(e) in ("not enough values to unpack (expected 1, got 0)", "400 [bad_parameter]: ids"):
            global manual
            if manual == 1:
                pr.print_warning("Wrong user ID specified...")
                pr.helpman()
                exit(1)
            pr.print_warning("Wrong user ID... Deleting the data file...")
            del_datafile()
            exit(1)

        # Reaches here when rate limit exceeds
        pr.print_warning(
            "Stack Overflow exception. This might be caused due to the rate limiting: "
            "http://stackapps.com/questions/3055/is-there-a-limit-of-api-requests")
        print("Use http://stackapps.com/apps/oauth/register to register a new API key.")
        set_api_key()
        exit(1)


def set_api_key():
    """
    Sets a custom API Key
    :return:
    """
    global app_data
    try:
        api_key = pr.inputs("Type an API key to continue (^C to abort): ")
        if len(api_key) > 0:
            app_data["api_key"] = api_key
            save_datafile()
        pr.print_warning("\nAPI Key saved...")
    except KeyboardInterrupt:
        print("Aborted.")


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
        pr.print_warning("File not created.... Use socli -u to create a new configuration file.")
        exit(0)


def retrieve_saved_profile():
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
    except json.JSONDecodeError:
        # This maybe some write failures
        del_datafile()
        pr.print_warning("Error in parsing the data file, it will be now deleted. Please rerun the "
                         "socli -u command.")
        exit(1)
    except FileNotFoundError:
        pr.print_warning("Default user not set...\n")
        try:
            # Code to execute when first time user runs socli -u
            app_data['user'] = int(pr.inputs("Enter your Stackoverflow User ID: "))
            save_datafile()
            user = app_data['user']
            pr.print_green("\nUserID saved...\n")
        except ValueError:
            pr.print_warning("\nUser ID must be an integer.")
            print(
                "\nFollow the instructions on this page to get your User ID: http://meta.stackexchange.com/a/111130")
            exit(1)
    return user
