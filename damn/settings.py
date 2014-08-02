
from django.conf import settings

# Map of mode -> processor config
#   {
#       'js': {
#           'processor': 'damn.processors.ScriptProcessor',
#           ...
#       },
#   }
PROCESSORS = getattr(settings, 'DAMN_PROCESSORS', {})

# File extensin -> mode name
MODE_MAP = getattr(settings, 'DAMN_MODE_MAP', {})

# Map of maps of default mode aliases
#   {
#       'js': {
#           'jquery': 'js/libs/jquery-1.11.min.js',
#       },
#       'css': {
#           'bootstrap': 'css/vendors/bootstrap-3.0.min.js',
#       },
#   }
DEPS = getattr(settings, 'DAMN_DEPENDS', {})

MODE_ORDER = getattr(settings, 'DAMN_MODE_ORDER', ['css', 'js', ])
