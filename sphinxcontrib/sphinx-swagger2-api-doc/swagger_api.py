#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from docutils import nodes
from docutils.parsers.rst import directives, Directive


class swagger(nodes.General, nodes.Element): pass


def visit_youtube_node(self, node):
    aspect = node["aspect"]
    width = node["width"]
    height = node["height"]


def depart_youtube_node(self, node):
    pass


class Swagger(Directive):
    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        "width": directives.unchanged,
        "height": directives.unchanged,
        "aspect": directives.unchanged,
    }

    def run(self):
        if "aspect" in self.options:
            aspect = self.options.get("aspect")
            m = re.match("(\d+):(\d+)", aspect)
            if m is None:
                raise ValueError("invalid aspect ratio %r" % aspect)
            aspect = tuple(int(x) for x in m.groups())
        else:
            aspect = None
        width = get_size(self.options, "width")
        height = get_size(self.options, "height")
        return [swagger(id=self.arguments[0], aspect=aspect, width=width, height=height)]


def setup(app):
    app.add_node(swagger, html=(visit_youtube_node, depart_youtube_node))
    app.add_directive("swagger", Swagger)
