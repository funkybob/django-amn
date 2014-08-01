
from collections import defaultdict
import os.path

from django.core.exceptions import ImproperlyConfigured
from importlib import import_module

from . import settings


class Processor(object):
    def __init__(self, name, config):
        self.name = name
        self.config = config

    def process(self, items):
        raise NotImplementedError

    def resolve_deps(self):
        '''
        Return our notes in depedency order
        '''
        resolved = []
        pending = set()
        self.items[0]._resolve(resolved, pending)
        return resolved


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
        self.deps = set(deps)

    def _resolve(self, resolved, pending):
        pending.add(self)
        for edge in self.deps:
            if edge in resolved:
                continue
            if edge in pending:
                raise Exception('Circular dependency: %s -> %s' % (self, edge))
            edge._resolve(resolved)
        pending.remove(self)
        resolved.append(self)


class AssetMode(list):
    '''
    Holds all the DepNodes for a given mode
    '''

    def __init__(self):
        self.aliases = {}

    def append(self, dep):
        # Update alias map
        if dep.alias:
            self.aliases[dep.alias] = dep.filename
        # Do we have this name already?
        try:
            orig = self.index(dep)
            # Merge the deps
            orig.deps.update(dep.deps)
        except ValueError:
            super(AssetMode, self).append(self)

        # Resolve dep aliases?
        super(AssetMode, self).append(dep)


class AssetRegistry(object):
    mode_map = settings.MODE_MAP

    def __init__(self):
        self.assets = defaultdict(AssetMode)

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
        mode = ext.lstrip('.')
        return self.mode_map.get(mode, mode)

    def render(self, context):
        tags = []
        for mode in self.assets.items():
            tags.extend(mode.render(context))
        return tags

    def items(self):
        return self.assets.items()

#
# Default processors
#

class ScriptProcessor(Processor):
    def process(self):
        assets = self.resolve()
        return [
            '<script src="%s"></script>' % static(asset)
            for asset in assets
        ]

