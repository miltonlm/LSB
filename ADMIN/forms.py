from django import forms
from django.db.models import Q
from .models import Personas, Inmuebles, Contratos
from datetime import date

TIPOS_PERSONA = [
    ('', 'SELECCIONAR'),
    ('PROPIETARIO', 'PROPIETARIO'),
    ('ARRENDATARIO', 'ARRENDATARIO'),
    ('CODEUDOR', 'CODEUDOR'),
    ('ASESOR', 'ASESOR'),
    ('REPRESENTANTE', 'REPRESENTANTE')
]

TIPOS_IDENTIFICACION = [
    ('', 'SELECCIONAR'),
    ('CC', 'CEDULA'),
    ('PA', 'PASAPORTE'),
    ('CE', 'CEDULA DE EXTRANJERIA'),
    ('RUT', 'RUT'),
    ('NIT', 'NIT')
]

TIPOS_INMUEBLES = [
    ('', 'SELECCIONAR'),
    ('CASA', 'CASA'),
    ('APARTAMENTO', 'APARTAMENTO'),
    ('APARTAESTUDIO', 'APARTAESTUDIO'),
    ('FINCA', 'FINCA'),
    ('OFICINA', 'OFICINA'),
    ('LOCAL', 'LOCALES')
]

TIPOS_OFERTA = [
    ('', 'SELECCIONAR'),
    ('ALQUILER', 'ALQUILER'),
    ('VENTA', 'VENTA')
]

ESTADOS_INMUEBLES = [
    ('', 'SELECCIONAR'),
    ('DISPONIBLE', 'DISPONIBLE'),
    ('OCUPADO', 'OCUPADO'),
    ('PROXIMAMENTE DISPONIBLE', 'PROXIMAMENTE DISPONIBLE')
]

PAISES = [
    ('', 'SELECCIONAR'),
    ('COLOMBIA', "COLOMBIA")
]

DEPARTAMENTOS = [
    ('', 'SELECCIONAR'),
    ('VALLE DEL CAUCA', 'VALLE DEL CAUCA')
]

CIUDADES = [
    ('', 'SELECCIONAR'),
    ('CALI', 'CALI'),
    ('PALMIRA', 'PALMIRA'),
    ('JAMUNDI', 'JAMUNDI'),
    ('ROLDANILLO', 'ROLDANILLO'),
    ('CARTAGO', 'CARTAGO'),
    ('BUENAVENTURA', 'BUENAVENTURA'),
    ('HONDA', 'HONDA'),
]

ZONAS = [
    ('', 'SELECCIONAR'),
    ('NORTE', 'NORTE'),
    ('SUR', 'SUR'),
    ('CENTRO', 'CENTRO'),
    ('ESTE', 'ESTE'),
    ('OESTE', 'OESTE')
]

SERVICIOS = [
    ('', 'SELECCIONAR'),
    ('AGUA', 'AGUA'),
    ('ENERGIA', 'ENERGIA'),
    ('GAS', 'GAS'),
    ('TV', 'TV'),
    ('INTERNET', 'INTERNET'),
    ('TELEFONIA', 'TELEFONIA'),
    ('ADMINISTRACION', 'ADMINISTRACION'),
    ('PARQUEADERO', 'PARQUEADERO')
]


class FormPersonas(forms.ModelForm):
    class Meta:
        model = Personas
        fields = '__all__'

    tipo_persona = forms.ChoiceField(choices=TIPOS_PERSONA)
    asesor = forms.ModelChoiceField(
        queryset=Personas.objects.filter(
            Q(tipo_persona='REPRESENTANTE') | Q(tipo_persona='ASESOR')
        ),
        required=False
    )
    tipo_identificacion = forms.ChoiceField(choices=TIPOS_IDENTIFICACION)
    lugar_expedicion_identificacion = forms.ChoiceField(choices=CIUDADES)
    fecha_creacion = forms.DateTimeField(widget=forms.HiddenInput, required=False)
    '''
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
    '''


class FormInmuebles(forms.ModelForm):
    class Meta:
        model = Inmuebles
        fields = '__all__'

    representante = forms.ModelChoiceField(
        queryset=Personas.objects.filter(
            Q(tipo_persona='REPRESENTANTE') | Q(tipo_persona='ASESOR')
        ),
        required=False,
    )
    zona = forms.ChoiceField(choices=ZONAS)
    tipo_inmueble = forms.ChoiceField(choices=TIPOS_INMUEBLES)
    estado = forms.ChoiceField(choices=ESTADOS_INMUEBLES)
    tipo_oferta = forms.ChoiceField(choices=TIPOS_OFERTA)

    '''representante = forms.ChoiceField(required=False,
                                      widget=forms.Select(attrs={'class': 'form-control'}),
                                      choices=(
                                          #(x.pk, x.nombre) for x in
                                          #     Personas.objects.filter(
                                          #         Q(tipo_persona='REPRESENTANTE')))
                                      ))
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
    '''


class FormContratos(forms.ModelForm):
    class Meta:
        model = Contratos
        fields = '__all__'

    representante = forms.ModelChoiceField(
        queryset=Personas.objects.filter(
            Q(tipo_persona='REPRESENTANTE') | Q(tipo_persona='ASESOR')
        ),
        required=False,
    )
    servicios_arrendador = forms.MultipleChoiceField(
        choices=SERVICIOS,
        widget=forms.CheckboxSelectMultiple(choices=SERVICIOS)
    )
    servicios_arrendatario = forms.MultipleChoiceField(
        choices=SERVICIOS,
        widget=forms.CheckboxSelectMultiple(choices=SERVICIOS)
    )
    fecha_contrato = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=date.today
    )
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=date.today
    )
    fecha_vigencia = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=date.today
    )

    '''representante = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'form-control'}),
                                      choices=(
                                      #    (x.identificacion, x.nombre) for x in
                                      #         Personas.objects.filter(tipo_persona="REPRESENTANTE")
                                      ))
    cliente_propietario = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                          label="Cliente Propietario")
    inmueble = forms.CharField(required=False, widget=forms.Select(attrs={'class': 'form-control'}), label="Inmueble")
    cliente_arrendatario = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                           label="Cliente Arrendatario")
    fecha_contrato = forms.CharField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    fecha_inicio = forms.CharField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    fecha_vigencia = forms.CharField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    precio_canon = forms.DecimalField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                      max_digits=10,
                                      decimal_places=2)
    servicios_arrendador = forms.MultipleChoiceField(choices=SERVICIOS,
                                                     widget=forms.CheckboxSelectMultiple(choices=SERVICIOS))
    servicios_arrendatario = forms.MultipleChoiceField(choices=SERVICIOS,
                                                       widget=forms.CheckboxSelectMultiple(choices=SERVICIOS))
    codeudor1 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    codeudor2 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    codeudor3 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    '''
