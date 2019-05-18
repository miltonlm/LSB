from django.db import models


class Paises(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return u'{}'.format(self.nombre)


class Departamentos(models.Model):
    pais = models.ForeignKey(
        Paises,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return u'{}'.format(self.nombre)


class Ciudades(models.Model):
    departamento = models.ForeignKey(
        Departamentos,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return u'{}'.format(self.nombre)


class Adjuntos(models.Model):
    programa = models.CharField(max_length=100, blank=True, null=True)
    id_asociado = models.IntegerField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    extension = models.CharField(max_length=20, blank=True, null=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    mime_type = models.CharField(max_length=200, blank=True, null=True)


class Gastos(models.Model):
    programa = models.CharField(max_length=20, blank=True, null=True)
    id_asociado = models.IntegerField(blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    valor = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)


class ImagenesInmueble(models.Model):
    id_asociado = models.IntegerField(blank=True, null=True)
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)


class Personas(models.Model):
    tipo_persona = models.CharField(max_length=100, blank=True, null=True)
    asesor = models.ForeignKey(
        'Personas',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='AsesorPersona'
    )
    nombre = models.CharField(max_length=255, blank=True, null=True)
    tipo_identificacion = models.CharField(max_length=100, blank=True, null=True)
    identificacion = models.CharField(max_length=100, blank=True, null=True)
    lugar_expedicion_identificacion = models.CharField(max_length=100, blank=True, null=True)
    pais = models.ForeignKey(
        Paises,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    departamento = models.ForeignKey(
        Departamentos,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    ciudad = models.ForeignKey(
        Ciudades,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    direccion = models.CharField(max_length=200, blank=True, null=True)
    telefono_movil = models.CharField(max_length=100, blank=True, null=True)
    telefono_fijo = models.CharField(max_length=100, blank=True, null=True)
    correo = models.CharField(max_length=200, blank=True, null=True)
    valoracion = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return u'{} - {}'.format(
            self.nombre,
            self.identificacion
        )


class Inmuebles(models.Model):
    representante = models.ForeignKey(
        Personas,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='Representante'
    )
    cliente_propietario = models.ForeignKey(
        Personas,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ClientePropietario'
    )
    pais = models.ForeignKey(
        Paises,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='PaisInmuebles'
    )
    departamento = models.ForeignKey(
        Departamentos,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='DepartamentoInmuebles'
    )
    ciudad = models.ForeignKey(
        Ciudades,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='CiudadInmuebles'
    )
    zona = models.CharField(max_length=100, blank=True, null=True)
    barrio = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=100, blank=True, null=True)
    direccion_adicional = models.CharField(max_length=100, blank=True, null=True)
    tipo_inmueble = models.CharField(max_length=100, blank=True, null=True)
    numero_habitaciones = models.IntegerField(blank=True, null=True)
    numero_banos = models.IntegerField(blank=True, null=True)
    numero_parqueaderos = models.IntegerField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    latitud = models.CharField(max_length=100, blank=True, null=True)
    longitud = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=100, blank=True, null=True)
    costo_canon = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    precio_canon = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    tipo_oferta = models.CharField(max_length=100)

    def __str__(self):
        return u'{} - {} - {} - {}'.format(
            self.tipo_inmueble,
            self.ciudad,
            self.barrio,
            self.direccion
        )


class Contratos(models.Model):
    representante = models.ForeignKey(
        Personas,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='RepresentanteContrato'
    )
    cliente_propietario = models.ForeignKey(
        Personas,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ClientePropietarioContrato'
    )
    inmueble = models.ForeignKey(
        Inmuebles,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='InmuebleContrato'
    )
    cliente_arrendatario = models.ForeignKey(
        Personas,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ClienteArrendatarioContrato'
    )
    fecha_contrato = models.DateField(blank=True, null=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_vigencia = models.DateField(blank=True, null=True)
    precio_canon = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    servicios_arrendador = models.CharField(max_length=255, blank=True, null=True)
    servicios_arrendatario = models.CharField(max_length=255, blank=True, null=True)
    codeudor1 = models.ForeignKey(
        Personas,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='Codeudor1Contrato'
    )
    codeudor2 = models.ForeignKey(
        Personas,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='Codeudor2Contrato'
    )
    codeudor3 = models.ForeignKey(
        Personas,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='Codeudor3Contrato'
    )
