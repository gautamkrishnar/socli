"""
Urwid-based class hierarchy that forms the front end of the SoCLI application.
"""

import sys
import subprocess
import urwid

import socli.printer as pr

question_post = None
question_page = None
display_header = None
MAIN_LOOP = None


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
            return pr.display_str(markup)
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
        if question_post is not None:
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
        answer_frame = self.make_frame(data)
        urwid.WidgetWrap.__init__(self, answer_frame)

    def make_frame(self, data):
        """
        Returns a new frame that is formatted correctly with respect to the window's dimensions.
        :param data: tuple of (answers, question_title, question_desc, question_stats, question_url)
        :return: a new urwid.Frame object
        """
        answers, question_title, question_desc, question_stats, question_url, dup_url = data
        self.data = data
        self.question_desc = question_desc
        self.url = question_url
        self.dup_url = dup_url
        self.answer_text = AnswerText(answers)
        self.screenHeight, screenWidth = subprocess.check_output(
            ['stty', 'size']).split()
        self.question_text = urwid.BoxAdapter(QuestionDescription(question_desc),
                                              int(max(1, (int(self.screenHeight) - 9) / 2)))
        if dup_url:
            answer_frame = urwid.Frame(
                header=urwid.Pile([
                    display_header,
                    QuestionTitle(question_title),
                    self.question_text,
                    QuestionStats(question_stats),
                    urwid.Divider('-')
                ]),
                body=self.answer_text,
                footer=urwid.Pile([
                    QuestionURL(question_url),
                    UnicodeText(
                        u'\u2191: previous answer, \u2193: next answer, o: open in browser, \u2190: back, d: visit duplicated question, q: quit')
                ])
            )
        else:
            answer_frame = urwid.Frame(
            header=urwid.Pile([
                display_header,
                QuestionTitle(question_title),
                self.question_text,
                QuestionStats(question_stats),
                urwid.Divider('-')
            ]),
            body=self.answer_text,
            footer=urwid.Pile([
                QuestionURL(question_url),
                UnicodeText(
                    u'\u2191: previous answer, \u2193: next answer, o: open in browser, \u2190: back, q: quit')
            ])
        )
        return answer_frame

    def keypress(self, size, key):
        """
        Overrides keypress in superclass, so don't fall for the trap! size parameter is needed!
        """
        if key in {'down', 'n', 'N'}:
            self.answer_text.next_ans()
        elif key in {'up', 'b', 'B'}:
            self.answer_text.prev_ans()
        elif key in {'o', 'O'}:
            import webbrowser
            display_header.event('browser', "Opening in your browser...")
            webbrowser.open(self.url)
        elif key == 'left':
            global question_post
            global question_page
            question_post = None
            if question_page is None:
                sys.exit(0)
            else:
                MAIN_LOOP.widget = question_page
        elif key == 'window resize':
            screen_height, screen_width = subprocess.check_output(['stty', 'size']).split()
            if self.screenHeight != screen_height:
                self._invalidate()
                answer_frame = self.make_frame(self.data)
                urwid.WidgetWrap.__init__(self, answer_frame)
        elif key in {'q', 'Q'}:
            sys.exit(0)
        elif key in {'d', 'D'}:
            if self.dup_url:
                pr.display_results(self.dup_url)


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
            display_header.event('answer-bounds', "No previous answers.")
        else:
            display_header.clear('answer-bounds')
        self.set_answer()

    def next_ans(self):
        """go to next answer."""
        self.index += 1
        if self.index > len(self.answers) - 1:
            self.index = len(self.answers) - 1
            display_header.event('answer-bounds', "No more answers.")
        else:
            display_header.clear('answer-bounds')
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


# Must convert to BoxAdapter object if used as a flow widget.
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
        self.content = self.description.strip("\n").split("\n")
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
