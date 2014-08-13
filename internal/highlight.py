__author__ = 'Gareth Coles'

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer

from internal.singleton import Singleton


class Highlight(object, metaclass=Singleton):
    """
    A simple utility class for highlighting code using Pygments.
    """

    def __init__(self):
        self.formatter = HtmlFormatter(cssclass="highlight", style="borland")

    def highlight(self,
                  code: "A string specifying the code to highlight",
                  language: "Optionally, the name of the language"=None):
        if language:
            return highlight(code, get_lexer_by_name(language), self.formatter)

        return highlight(code, guess_lexer(code), self.formatter)

    def get_css(self):
        return self.formatter.get_style_defs(".highlight")
