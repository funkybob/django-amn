
from django.conf import settings

PROCESSORS = getattr(settings, 'DAMN_PROCESSORS', {})

