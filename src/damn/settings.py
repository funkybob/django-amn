from django.conf import settings

# Map of mode -> processor config
#   {
#       'js': {
#           'processor': 'damn.processors.ScriptProcessor',
#           'aliases': {},
#       },
#   }
PROCESSORS = getattr(settings, "DAMN_PROCESSORS", {})

# File extension -> mode name
MODE_MAP = getattr(settings, "DAMN_MODE_MAP", {})

MODE_ORDER = getattr(settings, "DAMN_MODE_ORDER", ["css", "js",])
