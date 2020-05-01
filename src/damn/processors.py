from importlib import import_module
import os.path

from django.conf import settings
from django.templatetags.static import static
from django.core.exceptions import ImproperlyConfigured


class Processor:
    def __init__(self, config):
        self.config = config
        self.aliases = dict(config.get("aliases", {}))
        self.deps = config.get("deps", {})
        self.assets = {}

    def alias_map(self, name):
        return self.aliases.get(name, name)

    def resolve_deps(self):
        """
        Return our notes in depedency order
        """
        resolved = []
        pending = set()

        # Resolve aliases for deps
        deps = {
            self.alias_map(name): {
                self.alias_map(dep)
                for dep in depset
            }
            for name, depset in self.deps.items()
        }

        # Resolve aliases for assets
        assets = {
            self.alias_map(name): {
                self.alias_map(dep)
                for dep in deps
            }
            for name, deps in self.assets.items()
        }

        # Inject configured deps to assets
        for key in assets:
            if key in deps:
                assets[key].update(deps[key])
                # Ensure that anything in Aliases has an implicit Deps entry
                for item in deps[key]:
                    deps.setdefault(item, set())

        all_deps = set(assets.keys())
        all_deps.update(*assets.values())

        missing = all_deps.difference(assets.keys())
        while missing:
            for req in missing:
                if req not in deps:
                    raise Exception("Unable to satisfy: %r" % req)
                new_deps = deps[req]
                assets[req] = new_deps
                all_deps.add(req)
                all_deps.update(new_deps)
            missing = all_deps.difference(assets.keys())

        for dep in all_deps:
            if "." not in dep:
                raise ImproperlyConfigured("Dependency looks like an alias: %r" % dep)

        def resolve(filename, deps, resolved, pending):
            pending.add(filename)
            for dep in deps:
                if dep in resolved:
                    continue
                if dep in pending:
                    raise Exception("Circular dependency: %s -> %s" % (filename, dep))
                edges = assets[dep]
                resolve(dep, edges, resolved, pending)
            pending.remove(filename)
            resolved.append(filename)
            assets.pop(filename)

        # Keep going until there's nothing left
        # TODO: Find a deterministic approach
        while assets:
            # XXX This randomness is not good
            key = sorted(assets.keys())[0]
            resolve(key, assets[key], resolved, pending)

        return resolved

    def add_asset(self, filename, alias, deps):
        deps = set(deps)
        # Update alias map
        if alias:
            self.aliases[alias] = filename

        # Do we have this name already?
        if filename in self.assets:
            self.assets[filename].update(deps)
        else:
            self.assets[filename] = deps


class AssetRegistry:
    def __init__(self):
        self.mode_map = getattr(settings, "DAMN_MODE_MAP", {})
        self.mode_configs = getattr(settings, "DAMN_PROCESSORS", {})
        self.mode_order = getattr(settings, "DAMN_MODE_ORDER", ["css", "js"])
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
        mode = ext.lstrip(".")
        return self.mode_map.get(mode, mode)

    def processor_for_mode(self, mode):
        config = self.mode_configs[mode]

        mod, cls = config["processor"].rsplit(".", 1)
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


#
# Default processors
#


class ScriptProcessor(Processor):
    def render(self):
        assets = self.resolve_deps()
        return ['<script src="%s"></script>' % static(asset) for asset in assets]


class LinkProcessor(Processor):
    def render(self):
        assets = self.resolve_deps()
        return [
            '<link rel="{}" type="{}" href="{}">'.format(
                self.config.get("rel", "stylesheet"), self.config.get("type", "text/css"), static(asset),
            )
            for asset in assets
        ]
