__author__ = 'Gareth Coles'

import os
import markdown2

from internal.highlight import Highlight
from internal.singleton import Singleton

MARKDOWN_EXTRAS = [
    "code-friendly",  # Don't use `_` and `__` for `em` and `strong`
    "fenced-code-blocks",  # GitHub fenced code blocks with syntax highlighting
    "markdown-in-html",  # Add markdown="1" to a block html tag to have it
                         # parsed as markdown
]

TEMPLATE = """{description}

{code}
"""

CODE_TEMPLATE = """<div class="ui fluid accordion">
    <div class="title">
        <i class="dropdown icon"></i>
        JSON
    </div>
    <div class="content">
        <div class="ui secondary code-segment segment">
            {json}
        </div>
    </div>
    <div class="title">
        <i class="dropdown icon"></i>
        XML
    </div>
    <div class="content">
        <div class="ui secondary code-segment segment">
            {xml}
        </div>
    </div>
</div>
"""


class ApiManager(object, metaclass=Singleton):
    apis = {}

    highlighter = None
    markdowner = None

    def __init__(self):
        self.highlighter = Highlight()
        self.markdowner = markdown2.Markdown(extras=MARKDOWN_EXTRAS)

    def add_route(self,
                  route: "The API route itself",
                  method: "The HTTP method for this route",
                  text: "Text description for JSON, should be short",
                  markdown: "Name of Markdown file for HTML description"):
        api_route = {}

        if route in self.apis:
            api_route = self.apis[route]

        if method in api_route:
            return False  # Already exists

        if not os.path.exists("markdown/{0}.md".format(markdown)):
            return False

        description = self.markdowner.convert(
            open("markdown/{0}.md".format(markdown), "r").read()
        )

        code = ""
        if (os.path.exists("markdown/json/{0}.json".format(markdown)) and
                os.path.exists("markdown/xml/{0}.xml".format(markdown))):
            json_h = self.highlighter.highlight(
                open("markdown/json/{0}.json".format(markdown), "r").read(),
                "json"
            )

            xml_h = self.highlighter.highlight(
                open("markdown/xml/{0}.xml".format(markdown), "r").read(),
                "xml"
            )

            code = CODE_TEMPLATE.format(json=json_h, xml=xml_h)

        api_route[method] = {
            "text": text,
            "html": TEMPLATE.format(description=description, code=code)
        }

        self.apis[route] = api_route

        return True
