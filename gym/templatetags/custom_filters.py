# custom_filters.py
from django import template

register = template.Library()

@register.filter
def precio(precios_dict, clave_str):
    """
    Busca el precio usando la clave de cadena 'producto_id,canal_id'.
    (Suponiendo que el diccionario de la vista tiene claves de CADENA).
    """
    try:
        # Si la clave de la vista es una CADENA (ej. '1,1'), no necesitamos convertir a tupla.
        # Pero tu código de vista mostró CLAVES DE TUPLA (int, int).
        # Eliminemos la conversión a tupla.
        
        # Primero, verifica que la clave de entrada es la que se usa en la vista:
        producto_id, canal_id = clave_str.split(',') 
        clave_tupla = (int(producto_id), int(canal_id)) # <--- Tu clave de vista usa tuplas de INT
        
        # Retorna el precio buscando la tupla en el diccionario.
        return precios_dict.get(clave_tupla)
    except:
        return None