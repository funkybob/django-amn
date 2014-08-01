
from django import template

from damn.processors import find_processor
from damn.utils import AssetRegistry, DepNode


register = template.Library()


class AssetsNode(template.Node):

    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        context.render_context['AMN'] = AssetRegistry()

        content = self.nodelist.render(context)

        # Now output out tags
        extra_tags = '\n'.join(context.render_context['AMN'].items())

        return mark_safe(extra_tags) + content


@register.tag
def assets(parser, token):
    nodelist = parser.parse()
    return AssetsNode(nodelist)


@register.simpletag(takes_context=True)
def asset(context, name=None, alias=None, mode=None, *args):
    '''
    {% asset alias mode=? ... %}
    {% asset file.js ...  %}
    {% asset name depends depends... %}

    alias = short name for asset
    file = static relative filename
    mode = asset mode [inferred from filename extension]
    args == dependencies [aliases or files]
    '''
    if alias is None and name is None:
        raise template.TemplateSyntaxError(
            'asset tag requires at least one of name or alias'
        )
    if name is None and mode is None:
        raise template.TemplateSyntaxError(
            'asset tag reqires mode when using an alias'
        )
    context.render_context['AMN'].add_asset(name=name, alias=alias, mode=mode, deps=args)

    return ''
