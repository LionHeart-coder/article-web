from django import template

register = template.Library()


@register.filter
def textarea(field, rows):
    field.field.widget.attrs = {'rows': rows, 'cols': 40}
    return field


@register.filter
def add_id(field, new_id):
    field.field.widget.attrs = {'id': "comment_id_" + str(new_id)}
    return field
