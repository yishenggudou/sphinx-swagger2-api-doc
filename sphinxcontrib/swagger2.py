#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from docutils import nodes
from docutils.parsers.rst import directives, Directive
from docutils.statemachine import ViewList
from sphinx.util.nodes import nested_parse_with_titles
from .SwaggerAPIContext import SwaggerAPIContext

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class swagger(nodes.General, nodes.Element):
    pass


def html_visit_swagger_node(self, node):
    swagger_api_url = self.builder.config.swagger_api_url
    swagger_api_domain = self.builder.config.swagger_api_domain
    node["path"]
    # httpdomain_node = nodes.http(uri=refname, **node.attributes)
    # aspect = node["aspect"]
    # width = node["width"]
    # height = node["height"]
    # node.append(httpdomain_node)


def depart_swagger_node(self, node):
    pass


class SwaggerDirective(Directive):
    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        "desc": directives.unchanged,
        "title": directives.unchanged,
        "path": directives.unchanged,
        "summary": directives.unchanged,
        "method": directives.unchanged,
        
    }
    
    def run(self):
        env = self.state.document.settings.env
        warning = self.state.document.reporter.warning
        config = env.config
        """
        print(dir(self))
        print(dir(self.arguments))
        print(self.arguments)
        print(dir(self.content))
        print(self.content)
        for i in dir(self):
            if not i.startswith("_"):
                print("{0}{1}{2}".format('_' * 10, i, '_' * 10))
                print(getattr(self, i))
        """
        result_node = ViewList()
        o = SwaggerAPIContext(
            config['swagger_api_url'],
            self.options['method'].lower(),
            self.arguments[0],
            config["swagger_api_domain"],
            self.options['title'],
            desc=" ".join(self.content)
        )
        rst_context = o.get_rst_content()
        print(rst_context)
        node = nodes.section()
        node.document = self.state.document
        with StringIO(rst_context) as fr:
            for index, line in enumerate(fr):
                new_line = line.rstrip()
                print(new_line)
                result_node.append(new_line, "<swagger>")
        
        # Parse the rst.
        nested_parse_with_titles(self.state, result_node, node)
        return node.children


def depart_swagger_node(self, node):
    pass


_NODE_VISITORS = {
    'html': (html_visit_swagger_node, depart_swagger_node),
    'latex': (html_visit_swagger_node, depart_swagger_node),
    # 'latex': (latex_visit_swagger, latex_depart_swagger),
    # 'man': (unsupported_visit_plantuml, None),  # TODO
    # 'texinfo': (unsupported_visit_plantuml, None),  # TODO
    # 'text': (text_visit_plantuml, None),
}


def setup(app):
    app.setup_extension('sphinxcontrib.httpdomain')
    app.add_node(swagger, **_NODE_VISITORS)
    app.add_directive("swagger", SwaggerDirective)
    app.add_config_value('swagger_api_url', 'http://127.0.0.1:8080', 'http://127.0.0.1:8080')
    app.add_config_value('swagger_api_domain', 'example.com', 'example.com')
    return {'parallel_read_safe': True}
