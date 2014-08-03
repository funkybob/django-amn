
from importlib import import_module
import os.path

from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.exceptions import ImproperlyConfigured


class Processor(object):
    def __init__(self, config):
        self.config = config
        self.aliases = dict(config.get('aliases', {}))
        self.deps = config.get('deps', {})
        self.assets = {}

    def process(self, items):  # pragma: no cover
        raise NotImplementedError

    def resolve_deps(self):
        '''
        Return our notes in depedency order
        '''
        resolved = []
        pending = set()

        def resolve(filename, deps, resolved, pending):
            pending.add(filename)
            for dep in deps:
                # Resolve the alias
                dep = self.aliases.get(dep, dep)
                # Find the deps
                if not dep in self.assets:
                    if dep in self.deps:
                        self.add_asset(dep, None, self.deps[dep])
                    else:
                        raise Exception('Unable to satisfy dep: %r' % dep)
                edge = self.assets[dep]
                if dep in resolved:
                    continue
                if dep in pending:
                    raise Exception('Circular dependency: %s -> %s' % (filename, edge))
                resolve(dep, edge, resolved, pending)
            pending.remove(filename)
            resolved.append(filename)
            self.assets.pop(filename)

        # Keep going until there's nothing left
        # TODO: Find a deterministic approach
        while self.assets:
            # XXX This randomness is not good
            key = list(self.assets.keys())[0]
            resolve(key, self.assets[key], resolved, pending)

        return resolved

    def add_asset(self, filename, alias, deps):
        deps = tuple(deps)
        # Update alias map
        if alias:
            if filename is None:
                filename = self.aliases[alias]
            else:
                self.aliases[alias] = filename
        else:
            # Is it an alias:
            filename = self.aliases.get(filename, filename)
        # Are there configured deps?
        deps = deps + tuple(self.config.get('deps', {}).get(filename, ()))

        # Do we have this name already?
        try:
            orig = self.assets[filename]
        except KeyError:
            self.assets[filename] = tuple(deps)
        else:
            # Merge the deps
            orig.deps.update(deps)


class AssetRegistry(object):

    def __init__(self):
        self.mode_map = getattr(settings, 'DAMN_MODE_MAP', {})
        self.mode_configs = getattr(settings, 'DAMN_PROCESSORS', {})
        self.mode_order = getattr(settings, 'DAMN_MODE_ORDER', ['css', 'js'])
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
        config = self.mode_configs[mode]

        mod, cls = config['processor'].rsplit('.', 1)
        module = import_module(mod)
        return getattr(module, cls)(config)

    def render(self, context):
        result = []

        # Enforce ordering defined in settings
        modes = list(self.assets.keys())
        for mode in self.mode_order:
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
            '<script src="%s"></script>' % static(asset)
            for asset in assets
        ]


class LinkProcessor(Processor):
    def render(self):
        assets = self.resolve_deps()
        return [
            '<link rel="{}" type="{}" href="{}">'.format(
                self.config.get('rel', 'stylesheet'),
                self.config.get('type', 'text/css'),
                static(asset),
            )
            for asset in assets
        ]
