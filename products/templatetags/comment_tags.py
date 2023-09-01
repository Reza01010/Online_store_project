from django import template

register = template.Library()


@register.filter
def only_active_comment(comments):
    return comments.filter(active=True)# comments.exclude(active=False)


@register.filter()
def trans_number(number):
    number = str(number)
    table = number.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
    return number.translate(table)
