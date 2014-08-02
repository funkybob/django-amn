
from importlib import import_module
import os.path

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.exceptions import ImproperlyConfigured

from . import settings


class Processor(object):
    def __init__(self, config):
        self.config = config
        self.aliases = dict(config.get('aliases', {}))
        self.assets = {}

    def process(self, items):
        raise NotImplementedError

    def resolve_deps(self):
        '''
        Return our notes in depedency order
        '''
        resolved = []
        pending = set()

        # Get a copy
        assets = dict(self.assets)

        def resolve(item, resolved, pending):
            pending.add(item)
            for dep in item.deps:
                dep = self.aliases.get(dep, dep)
                edge = self.assets[dep]
                if edge in resolved:
                    continue
                if edge in pending:
                    raise Exception('Circular dependency: %s -> %s' % (item, edge))
                resolve(edge, resolved, pending)
            pending.remove(item)
            resolved.append(item)
            assets.pop(item.filename)

        # Keep going until there's nothing left
        # TODO: Find a deterministic approach
        while assets:
            # XXX This randomness is not good
            resolve(assets[list(assets.keys())[0]], resolved, pending)

        return resolved

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
            self.assets[filename] = DependencyNode(filename, deps)
        else:
            # Merge the deps
            orig.deps.update(deps)


class DependencyNode(object):
    '''
    A container for filename + dependencies
    '''
    def __init__(self, filename, deps):
        self.filename = filename
        self.deps = set(deps)

    def __repr__(self):
        return u'{} [{}]'.format(self.filename, self.deps)


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
            # Find the Processor for this mode
            modeset = self.processor_for_mode(mode)
            self.assets[mode] = modeset
        modeset.add_asset(filename, alias, deps)

    def mode_for_file(self, filename):
        _, ext = os.path.splitext(filename)
        mode = ext.lstrip('.')
        return self.mode_map.get(mode, mode)

    def processor_for_mode(self, mode):
        config = settings.PROCESSORS[mode]

        mod, cls = config['processor'].rsplit('.', 1)
        module = import_module(mod)
        return getattr(module, cls)(config)

    def render(self, context):
        result = []

        # Enforce ordering defined in settings
        modes = list(self.assets.keys())
        for mode in settings.MODE_ORDER:
            if mode in modes:
                result.extend(self.assets[mode].render())
                modes.remove(mode)

        # Then handle what's leftover
        for mode in modes:
            result.extend(self.assets[mode].render())
        return result

    def __getitem__(self, key):
        return self.assets[key]

#
# Default processors
#


class ScriptProcessor(Processor):
    def render(self):
        assets = self.resolve_deps()
        return [
            '<script src="%s"></script>' % static(asset.filename)
            for asset in assets
        ]


class LinkProcessor(Processor):
    def render(self):
        assets = self.resolve_deps()
        return [
            '<link rel="{}" type="{}" href="{}">'.format(
                self.config.get('rel', 'stylesheet'),
                self.config.get('type', 'text/css'),
                static(asset.filename),
            )
            for asset in assets
        ]
