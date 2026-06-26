from django import template
from gym.models import Modulo, PermisoRol

register = template.Library()

@register.inclusion_tag('partials/menu_items.html', takes_context=True)
def render_sidebar_menu(context):
    user = context['request'].user
    if not user.is_authenticated:
        return {'modulos_padre': []}

    # Si es administrador, ve todo. Si no, filtramos por sus permisos.
    if user.rol.nombre.lower() == 'administrador':
        # Obtenemos módulos raíz (los que no tienen padre)
        padres = Modulo.objects.filter(modulo_padre__isnull=True, is_active=True).order_by('orden')
    else:
        # Obtenemos los códigos de módulos donde el usuario tiene permiso de 'ver'
        permisos_codigos = PermisoRol.objects.filter(
            rol=user.rol, 
            puede_ver=True
        ).values_list('modulo__codigo', flat=True)
        
        # Filtramos padres que tengan hijos con permiso O que el padre mismo tenga permiso
        padres = Modulo.objects.filter(
            modulo_padre__isnull=True, 
            is_active=True,
            codigo__in=permisos_codigos
        ).order_by('orden').distinct()

    return {
        'modulos_padre': padres,
        'user_permisos': permisos_codigos if user.rol.nombre.lower() != 'administrador' else None,
        'is_admin': user.rol.nombre.lower() == 'administrador',
        'request': context['request']
    }