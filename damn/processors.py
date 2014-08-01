
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
    def __init__(self, name, alias, deps):
        self.name = name
        self.alias = alias
        self.deps = deps

class AssetMode(list):
    def __init__(self):
        self.aliases = {}

    def append(self, dep):
        # Update alias map
        if dep.alias:
            self.aliases[dep.alias] = dep.filename
        # Resolve dep aliases?
        super(AssetModel, self).append(dep)

class AssetRegistry(object):
    mode_map = settings.MODE_MAP

    def __init__(self):
        self.assets = {}

    def add_asset(self, name, alias, mode, deps):
        # Clearly, you must have a Mode if you have only an alias
        if mode is None:
            mode = self.mode_for_file(name)

        modeset = self.assets[mode]

        if name is None:
            name = modeset[alias]

        modeset.append(DependencyNode(name, alias, deps))

    def mode_for_file(self, filename):
        _, ext = os.path.splitext(filename)
        return self.mode_map.get(ext, ext)

    def render(self, context):
        tags = []
        for mode in self.assets.items():
            tags.extend(mode.render(context))
        return tags
