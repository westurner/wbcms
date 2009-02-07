requirements = [
        {'name':'flup',
            'package':'flup',
            'dist'='pypi'},
      {
        'name': 'django-freetext',
        'package': 'free_text',
        'dist': 'git',
        'url': 'git://github.com/lincolnloop/django-freetext.git',
    }, {
        'name': 'html2text.py',
        'dist': 'wget',
        'url': 'http://www.aaronsw.com/2002/html2text/html2text.py',
    }, {
        'name': 'python-dateutil',
        'dist': 'pypi',
        'rev': '1.4.1',
        'url':'http://pypi.python.org/pypi/dateutil',
    }
#, {
#        'name': 'django-trunk',
#        'dist':'git',
#        'url':'git://github.com/django/django.git',
#    }
, {
        'name':'django-tagging',
        'package':'tagging',
        'dist':'svn',
        'rev':'149',
        'url':'http://django-tagging.googlecode.com/svn/trunk'
    }, {
        'name':'django-command-extensions',
        'dist':'svn',
        #'rev':'135',
        'url':' http://django-command-extensions.googlecode.com/svn/trunk',
    }, {
        'name':'django-template-utils',
        'dist':'svn',
        'rev':'109',
        'url':'http://django-template-utils.googlecode.com/svn/trunk',
    },{
        'name':'django-debug-toolbar',
        'dist':'git',
        'url':'git://github.com/robhudson/django-debug-toolbar.git'
    },{
        'name':'django-pagination',
        'dist':'svn',
        'url':'http://django-pagination.googlecode.com/svn/trunk/'
    }
]
