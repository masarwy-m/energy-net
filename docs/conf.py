# Configuration file for Sphinx documentation builder.
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------

project = 'energy-net'
author = 'CLAIR'
copyright = 'Copyright © CLAIR'
version = '0.0.1'
release = '0.0.1'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.githubpages',
    # Add more extensions as needed
]

# The name of the main (index) file, without the file extension.
master_doc = 'index'

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
