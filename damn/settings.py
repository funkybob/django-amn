
from django.conf import settings

PROCESSORS = getattr(settings, 'DAMN_PROCESSORS', {})

MODE_MAP = getattr(settings, 'DAMN_MODE_MAP', {})
