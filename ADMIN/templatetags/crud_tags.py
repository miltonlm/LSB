from django import template
from ADMIN.models import *


register = template.Library()


@register.simple_tag
def model_description(**kwargs):
    field = kwargs['field']
    value = kwargs['value']

    try:
        if value:
            val = value

            if field == 'asesor' or field == 'cliente_propietario' or\
                    field == 'cliente_arrendatario' or field == 'codeudor1' or\
                    field == 'codeudor2' or field == 'codeudor3' or field == 'representante':
                val = Personas.objects.get(pk=value)
            elif field == 'inmueble':
                val = Inmuebles.objects.get(pk=value)
            elif field == 'pais':
                val = Paises.objects.get(pk=value)
            elif field == 'departamento':
                val = Departamentos.objects.get(pk=value)
            elif field == 'ciudad':
                val = Ciudades.objects.get(pk=value)

            return str(val)
    except:
        return value

    return value
