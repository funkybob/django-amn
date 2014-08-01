
from django.core.exceptions import ImproperlyConfigured
from importlib import import_module

from . import settings


class Processor(object):
    def __init__(self, name, config):
        self.name = name
        self.config = config

    def process(self, items):
        raise NotImplementedError


def find_processor(name):
    try:
        config = settings.PROCESSORS[name]
    except KeyError:
        raise ImproperlyConfigured('No configuration for asset processor %r' % name)

    mod, cls = config['class'].rsplit('.')
    module = import_module(mod)
    return getattr(module, cls)(name, config)


class DependencyNode(object):
    def __init__(self, name, alias, mode, deps):
        self.name = name
        self.alias = alias
        self.mode = mode
        self.deps = deps


class AssetModel(list):
    def __init__(self):
        self.aliases = {}

    def append(self, dep):
        # Update alias map
        if dep.alias:
            self.aliases[dep.alias] = dep.filename
        super(AssetModel, self).append(dep)

class AssetRegistry(object):
    mode_map = {
    }

    def __init__(self):
        self.assets = defaultdict(list)

    def add_asset(self, name, alias, mode, deps):
        self.assets[mode].append(DependencyNode())

    def mode_for_file(self, filename):
        _, ext = os.path.splitext(filename)
        return self.mode_map.get(ext, ext)

