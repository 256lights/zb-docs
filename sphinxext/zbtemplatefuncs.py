# Copyright 2025 The zb Authors
# SPDX-License-Identifier: MIT

from typing import Any, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from docutils import nodes
    from sphinx.application import Sphinx

def setup_html_page_context(app: 'Sphinx', pagename: str, templatename: str, context: Dict[str, Any], doctree: 'nodes.document') -> Optional[str]:
    def strip_index(s: str) -> str:
        suffix = '/index'
        return s[:-len(suffix)] if s.endswith(suffix) else s
    context['strip_index'] = strip_index

def setup(app: 'Sphinx'):
    app.connect('html-page-context', setup_html_page_context)
