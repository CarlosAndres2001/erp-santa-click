from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def dict_sum(value, arg):
    """
    Suma el valor de una clave específica (arg) en una lista de diccionarios (value).
    """
    total = Decimal('0.00')
    if isinstance(value, list):
        for item in value:
            try:
                amount = Decimal(item.get(arg) or 0)
                total += amount
            except Exception:
                continue 
    return total