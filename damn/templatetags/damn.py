
from django import template
from django.utils.safestring import mark_safe

from ..processors import AssetRegistry


register = template.Library()


class AssetsNode(template.Node):

    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        context.render_context['AMN'] = AssetRegistry()

        content = self.nodelist.render(context)

        # Now output out tags
        extra_tags = '\n'.join(context.render_context['AMN'].render(context))

        return mark_safe(extra_tags) + content


@register.tag
def assets(parser, token):
    nodelist = parser.parse()
    return AssetsNode(nodelist)


@register.simple_tag(takes_context=True)
def asset(context, filename=None, *args, **kwargs):
    '''
    {% asset alias mode=? ... %}
    {% asset file.js ...  %}
    {% asset name depends depends... %}

    alias = short name for asset
    file = static relative filename
    mode = asset mode [inferred from filename extension]
    args == dependencies [aliases or files]
    '''
    alias = kwargs.get('alias')
    mode = kwargs.get('mode')
    if alias is None and filename is None:
        raise template.TemplateSyntaxError(
            'asset tag requires at least one of name or alias'
        )
    if filename is None and mode is None:
        raise template.TemplateSyntaxError(
            'asset tag reqires mode when using an alias'
        )
    if alias == filename:
        raise template.TemplateSyntaxError(
            'Attempt to alias asset to itself.'
        )
    context.render_context['AMN'].add_asset(filename=filename, alias=alias, mode=mode, deps=args)

    return ''
