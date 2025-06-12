# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys
from pathlib import Path

sys.path.append(str(Path('sphinxext').resolve()))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'zb'
copyright = '2025, The zb Authors'
author = 'The zb Authors'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
    'sphinx.ext.githubpages',
    'zbluadomain',
    'zbtemplatefuncs',
]

myst_enable_extensions = [
    'attrs_block',
    'attrs_inline',
    'colon_fence',
    'fieldlist',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
primary_domain = 'lua'



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_baseurl = 'https://zb.256lights.llc/'
html_theme = 'alabaster'
html_theme_options = {
    "logo": "LogoRainbow.svg",
    "logo_name": True,
    "font_family": '"Titillium Web", sans-serif',
    "code_font_family": '"Go Mono", monospace',
    "github_button": True,
    "github_type": "star",
    "github_user": "256lights",
    "github_repo": "zb",
}
html_static_path = ['_static']
html_additional_pages = {
    'pkg/index': 'gopkg.html.jinja',
    'pkg/zbstore': 'gopkg.html.jinja',
}
