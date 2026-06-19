# Copyright 2026 The zb Authors
# SPDX-License-Identifier: MIT

import os

from sphinx.application import Sphinx


def setup(app: Sphinx):
    app.add_html_theme('zb', os.path.dirname(__file__))
