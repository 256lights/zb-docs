import os

from sphinx.application import Sphinx


def setup(app: Sphinx):
    app.add_html_theme('zb', os.path.dirname(__file__))
