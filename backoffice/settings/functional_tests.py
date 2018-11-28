import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Fucntional Tests settings
FUNCT_TESTS_CONFIG = {
    'DEFAULT_WAITING_TIME': int(os.environ.get('FT_DEFAULT_WAITING_TIME', 10)),
    'BROWSER': os.environ.get('FT_BROWSER', 'FIREFOX'),
    'VIRTUAL_DISPLAY': os.environ.get('FT_VIRTUAL_DISPLAY', 'True').lower() == 'true',
    'DISPLAY_WIDTH': int(os.environ.get('FT_DISPLAY_WIDTH', 1920)),
    'DISPLAY_HEIGHT': int(os.environ.get('FT_DISPLAY_HEIGHT', 1080)),
    'GECKO_DRIVER': os.environ.get('FT_GECKO_DRIVER', os.path.join(BASE_DIR, 'base/tests/functional/drivers/geckodriver')),
    'TAKE_SCREENSHOTS': os.environ.get('FT_TAKE_SCREENSHOTS', 'False').lower() == 'true',
    'SCREENSHOTS_DIR': os.environ.get('FT_SCREENSHOT_DIR', os.path.join(BASE_DIR, 'base/tests/functional/screenshots')),
    'HTML_REPORTS': os.environ.get('FT_HTML_REPORTS', 'False').lower() == 'true',
    'HTML_REPORTS_DIR': os.environ.get('FT_HTML_REPORTS_DIR', os.path.join(BASE_DIR, 'base/tests/functional/html_reports')),
    'HTML_REPORTS_STATIC_DIR': os.environ.get('FT_HTML_REPORTS_STATIC_DIR', os.path.join(BASE_DIR, 'base/tests/functional/html_reports/static')),
    'DASHBOARD': {
        'PAGE_TITLE': 'OSIS',
    },
    'LOGIN': {
        'PAGE_TITLE': 'OSIS',
    },
    'LEARNING_UNITS': {
        'BY_ACTIVITY_LINKS': ('lnk_catalog', 'lnk_learning_units'),
    }
}