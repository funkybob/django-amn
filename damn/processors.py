
from importlib import import_module
import os.path

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.exceptions import ImproperlyConfigured

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
        raise ImproperlyConfigured(
            'No configuration for asset processor %r' % name
        )

    mod, cls = config['class'].rsplit('.')
    module = import_module(mod)
    return getattr(module, cls)(name, config)


class DependencyNode(object):
    def __init__(self, name, deps):
        self.name = name
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


class AssetMode(object):
    '''
    Holds all the DepNodes for a given mode
    '''

    def __init__(self, default_aliases):
        self.aliases = dict(default_aliases)
        self.assets = {}

    def add_asset(self, filename, alias, deps):
        # Update alias map
        if alias:
            if filename is None:
                filename = self.aliases[alias]
            else:
                self.aliases[alias] = filename
        # Do we have this name already?
        try:
            orig = self.assets[filename]
        except KeyError:
            self.asserts[filename] = DependencyNode(filename, alias, deps)
        else:
            # Merge the deps
            orig.deps.update(deps)


class AssetRegistry(object):
    mode_map = settings.MODE_MAP

    def __init__(self):
        self.assets = {}

    def add_asset(self, filename, alias, mode, deps):
        # Clearly, you must have a Mode if you have only an alias
        if mode is None:
            mode = self.mode_for_file(filename)

        try:
            modeset = self.assets[mode]
        except KeyError:
            self.assets[mode] = modeset = AssetMode(settings.DEPS.get(mode, {}))
        modeset.add_asset(filename, alias, deps)

    def mode_for_file(self, filename):
        _, ext = os.path.splitext(filename)
        mode = ext.lstrip('.')
        return self.mode_map.get(mode, mode)

    def render(self, context):
        return [
            mode.render()
            for mode in self.assets.values()
        ]

    def __getitem__(self, key):
        return self.assets[key]

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
