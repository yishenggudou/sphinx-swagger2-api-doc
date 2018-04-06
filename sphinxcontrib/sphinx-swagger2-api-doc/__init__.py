"""
    sphinxcontrib.sphinx-swagger2-api-doc
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    a tools for sphinx gen doc from swagger2 api

    :copyright: Copyright 2017 by yishenggudou <yishenggudou@gmail.com>
    :license: BSD, see LICENSE for details.
"""

import pbr.version

if False:
    # For type annotations
    from typing import Any, Dict  # noqa
    from sphinx.application import Sphinx  # noqa

__version__ = pbr.version.VersionInfo(
    'sphinx-swagger2-api-doc').version_string()


def setup(app):
    # type: (Sphinx) -> Dict[unicode, Any]
    return {'version': __version__, 'parallel_read_safe': True}
