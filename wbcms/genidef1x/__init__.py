"""
Generates an IDEF1X ERD chart from Django, in the DOT Language.

Based in part on the `modelviz <http://code.google.com/p/django-command-extensions/source/browse/trunk/django_extensions/management/modelviz.py>` code in `django-command-extensions <http://code.google.com/p/django-command-extensions>`

Usage:
  ./idef1x.py --apps <app_names> -o <output_dot_file>
  dot -Tpng -o <output_png>.png <output_dot_file>
  dot -Tsvg -o <output_svg>.svg <output_dot_file>
  ...


"""
__version__ = "0.01"
__author__ = "Wes Turner <wes.turner@gmail.com"

