project = 'django-sms'
copyright = '2021, Roald Nefs'
author = 'Roald Nefs'
release = '0.2.0'

extensions = ['m2r2']
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
source_suffix = ['.rst', '.md']

html_theme = 'alabaster'
html_theme_options = {
    "description": "A Django app for sending SMS with interchangeable backends.",
    "show_powered_by": False,
    "github_user": "roaldnefs",
    "github_repo": "django-sms",
    "github_button": True,
    "github_banner": True,
    "show_related": False,
}
html_static_path = ['_static']
