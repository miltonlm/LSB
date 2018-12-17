from django import forms
from django.db.models import Q

from .models import Personas, Inmuebles, Contratos

TIPOS_PERSONA = [
    ('PROPIETARIO', 'PROPIETARIO'),
    ('ARRENDATARIO', 'ARRENDATARIO'),
    ('CODEUDOR', 'CODEUDOR'),
    ('ASESOR', 'ASESOR'),
    ('REPRESENTANTE', 'REPRESENTANTE')
]

TIPOS_IDENTIFICACION = [
    ('CC', 'CEDULA'),
    ('PA', 'PASAPORTE'),
    ('CE', 'CEDULA DE EXTRANJERIA'),
    ('RUT', 'RUT'),
    ('NIT', 'NIT')
]

TIPOS_INMUEBLES = [
    ('CASA', 'CASA'),
    ('APARTAMENTO', 'APARTAMENTO'),
    ('APARTAESTUDIO', 'APARTAESTUDIO'),
    ('FINCA', 'FINCA'),
    ('OFICINA', 'OFICINA'),
    ('LOCAL', 'LOCALES')
]

TIPOS_OFERTA = [
    ('ALQUILER', 'ALQUILER'),
    ('VENTA', 'VENTA')
]

ESTADOS_INMUEBLES = [
    ('DISPONIBLE', 'DISPONIBLE'),
    ('OCUPADO', 'OCUPADO'),
    ('PROXIMAMENTE DISPONIBLE', 'PROXIMAMENTE DISPONIBLE')
]

PAISES = [
    ('COLOMBIA', "COLOMBIA")
]

DEPARTAMENTOS = [
    ('VALLE DEL CAUCA', 'VALLE DEL CAUCA')
]

CIUDADES = [
    ('CALI', 'CALI'),
    ('PALMIRA', 'PALMIRA'),
    ('JAMUNDI', 'JAMUNDI'),
    ('ROLDANILLO', 'ROLDANILLO'),
    ('CARTAGO', 'CARTAGO'),
    ('BUENAVENTURA', 'BUENAVENTURA')
]

ZONAS = [
    ('NORTE', 'NORTE'),
    ('SUR', 'SUR'),
    ('CENTRO', 'CENTRO'),
    ('ESTE', 'ESTE'),
    ('OESTE', 'OESTE')
]

SERVICIOS = [
    ('AGUA', 'AGUA'),
    ('ENERGIA', 'ENERGIA'),
    ('GAS', 'GAS'),
    ('TV', 'TV'),
    ('INTERNET', 'INTERNET'),
    ('TELEFONIA', 'TELEFONIA'),
    ('ADMINISTRACION', 'ADMINISTRACION'),
    ('PARQUEADERO', 'PARQUEADERO')
]


class FP(forms.ModelForm):
    class Meta:
        model = Personas
        fields = ['tipo_persona',
                  'asesor',
                  'nombre',
                  'tipo_identificacion',
                  'identificacion',
                  'lugar_expedicion_identificacion',
                  'pais',
                  'departamento',
                  'ciudad',
                  'direccion',
                  'telefono_movil',
                  'telefono_fijo',
                  'correo',
                  'valoracion',
                  'fecha_creacion',
                  'password']

    tipo_persona = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'form-control'}),
                                     choices=TIPOS_PERSONA)
    asesor = forms.ChoiceField(required=False,
                               widget=forms.Select(attrs={'class': 'form-control'}),
                               choices=((x.pk, x.nombre) for x in
                                        Personas.objects.filter(
                                            Q(tipo_persona='REPRESENTANTE') | Q(tipo_persona='ASESOR'))))
    nombre = forms.CharField(max_length=255, label='Nombre', widget=forms.TextInput(attrs={'class': 'form-control'}))
    tipo_identificacion = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'form-control'}),
                                            choices=TIPOS_IDENTIFICACION)
    identificacion = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    lugar_expedicion_identificacion = forms.CharField(max_length=255,
                                                      widget=forms.Select(attrs={'class': 'form-control'},
                                                                          choices=CIUDADES))
    pais = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'form-control'}), choices=PAISES)
    departamento = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'form-control'}),
                                     choices=DEPARTAMENTOS)
    ciudad = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'form-control'}), choices=CIUDADES)
    direccion = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefono_movil = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefono_fijo = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    correo = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    valoracion = forms.DecimalField(max_digits=3, decimal_places=2,
                                    widget=forms.NumberInput(attrs={'class': 'form-control'}))
    fecha_creacion = forms.DateField(required=False, widget=forms.DateInput(attrs={'disabled': 'disabled'}))
    password = forms.CharField(max_length=255, required=False,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class FI(forms.ModelForm):
    class Meta:
        model = Inmuebles
        fields = ['cliente_propietario',
                  'pais',
                  'departamento',
                  'ciudad',
                  'zona',
                  'barrio',
                  'direccion',
                  'tipo_inmueble',
                  'numero_habitaciones',
                  'numero_banos',
                  'numero_parqueaderos',
                  'descripcion',
                  'latitud',
                  'longitud',
                  'estado',
                  'costo_canon',
                  'precio_canon',
                  'tipo_oferta']

    representante = forms.ChoiceField(required=False,
                                      widget=forms.Select(attrs={'class': 'form-control'}),
                                      choices=((x.pk, x.nombre) for x in
                                               Personas.objects.filter(
                                                   Q(tipo_persona='REPRESENTANTE'))))
    cliente_propietario = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': "form-control"}))
    pais = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'form-control'}), choices=PAISES)
    departamento = forms.CharField(required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': True}))
    ciudad = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'form-control'}), choices=CIUDADES)
    zona = forms.CharField(required=False, max_length=255,
                           widget=forms.Select(choices=ZONAS, attrs={'class': "form-control"}))
    barrio = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': True}))
    direccion = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': "form-control"}))
    tipo_inmueble = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'form-control'}),
                                      choices=TIPOS_INMUEBLES)
    numero_habitaciones = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': "form-control"}))
    numero_banos = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': "form-control"}))
    numero_parqueaderos = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': "form-control"}))
    descripcion = forms.CharField(max_length=255, widget=forms.Textarea(attrs={'class': 'form-control'}))
    latitud = forms.CharField(max_length=255, widget=forms.HiddenInput(attrs={'class': 'form-control'}))
    longitud = forms.CharField(max_length=255, widget=forms.HiddenInput(attrs={'class': 'form-control'}))
    estado = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'form-control'}),
                               choices=ESTADOS_INMUEBLES)
    costo_canon = forms.DecimalField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                     max_digits=10,
                                     decimal_places=2)
    precio_canon = forms.DecimalField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                      max_digits=10,
                                      decimal_places=2)
    tipo_oferta = forms.CharField(required=True, widget=forms.Select(attrs={'class': 'form-control'},
                                                                     choices=TIPOS_OFERTA))


class FC(forms.ModelForm):
    class Meta:
        model = Contratos
        fields = ['representante',
                  'cliente_propietario',
                  'inmueble',
                  'cliente_arrendatario',
                  'fecha_contrato',
                  'fecha_inicio',
                  'fecha_vigencia',
                  'precio_canon',
                  'servicios_arrendatario',
                  'servicios_arrendador',
                  'codeudor1',
                  'codeudor2',
                  'codeudor3']

    id = forms.HiddenInput()
    representante = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'form-control'}),
                                      choices=((x.identificacion, x.nombre) for x in
                                               Personas.objects.filter(tipo_persona="REPRESENTANTE")))
    cliente_propietario = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                          label="Cliente Propietario")
    inmueble = forms.CharField(required=False, widget=forms.Select(attrs={'class': 'form-control'}), label="Inmueble")
    cliente_arrendatario = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                           label="Cliente Arrendatario")
    fecha_contrato = forms.CharField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    fecha_inicio = forms.CharField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    fecha_vigencia = forms.CharField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    precio_canon = forms.DecimalField(max_digits=10, decimal_places=2)
    servicios_arrendador = forms.MultipleChoiceField(choices=SERVICIOS,
                                                     widget=forms.CheckboxSelectMultiple(choices=SERVICIOS))
    servicios_arrendatario = forms.MultipleChoiceField(choices=SERVICIOS,
                                                       widget=forms.CheckboxSelectMultiple(choices=SERVICIOS))
    codeudor1 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    codeudor2 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    codeudor3 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
