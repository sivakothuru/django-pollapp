from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'polldb'
     }
}

from django.conf import settings


COVERAGE_TEST_RUNNER = getattr(settings, 'COVERAGE_TEST_RUNNER',
                             'django_coverage.coverage_runner.CoverageRunner')


COVERAGE_USE_CACHE = getattr(settings, 'COVERAGE_USE_CACHE', False)

COVERAGE_CODE_EXCLUDES = getattr(settings, 'COVERAGE_CODE_EXCLUDES',[
                                    'def __unicode__\(self\):',
                                    'def get_absolute_url\(self\):',
                                    'from .* import .*', 'import .*',
                                 ])

COVERAGE_PATH_EXCLUDES = getattr(settings, 'COVERAGE_PATH_EXCLUDES',
                                 [r'.svn'])


COVERAGE_ADDITIONAL_MODULES = getattr(settings, 'COVERAGE_ADDITIONAL_MODULES', [])


COVERAGE_MODULE_EXCLUDES = getattr(settings, 'COVERAGE_MODULE_EXCLUDES',
                                   ['tests$', 'settings$', 'urls$', 'locale$',
                                    'common.views.test', '__init__', 'django',
                                    'migrations'])


# Specify the directory where you would like the coverage report to create

COVERAGE_REPORT_HTML_OUTPUT_DIR = getattr(settings,
                                          'COVERAGE_REPORT_HTML_OUTPUT_DIR',
                                          None)

# True => html reports by 55minutes
# False => html reports by coverage.py
COVERAGE_CUSTOM_REPORTS = getattr(settings, 'COVERAGE_CUSTOM_REPORTS', True)



COVERAGE_USE_STDOUT = getattr(settings, 'COVERAGE_USE_STDOUT', COVERAGE_REPORT_HTML_OUTPUT_DIR is None)

COVERAGE_BADGE_TYPE = getattr(settings, 'COVERAGE_BADGE_TYPE', 'drone.io')