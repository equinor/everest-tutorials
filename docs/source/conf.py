from importlib import metadata


# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'everest_tutorials'
copyright = '2025, Equinor ASA'
author = 'Equinor ASA'

try:
    dist_version = metadata.version("everest_tutorials")
except metadata.PackageNotFoundError:
    dist_version = "0.0.0"

# The short X.Y.Z version
version = ".".join(dist_version.split(".")[:3])
# The full version, including alpha/beta/rc tags
release = dist_version

rst_epilog = f"""
.. |everest_tutorial_drogon_download| replace:: https://github.com/equinor/everest-tutorials/releases/download/v{version}/everest-tutorials-drogon.tar.gz
"""

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_mdinclude",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.ifconfig",
    "sphinx.ext.viewcode",
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_title = f"{project}"
html_theme_options = {
    "source_repository": "https://github.com/equinor/everest-tutorials/",
    "source_branch": "main",
    "source_directory": "source/",
}

html_static_path = ['_static']

intersphinx_mapping = {
    "everest": ("https://everest.readthedocs.io/en/latest/", None),
}
