from django.db import models


class Adjuntos(models.Model):
    programa = models.CharField(max_length=100, blank=True, null=True)
    id_asociado = models.IntegerField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    extension = models.CharField(max_length=20, blank=True, null=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    mime_type = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'adjuntos'


class Contratos(models.Model):
    representante = models.CharField(max_length=100, blank=True, null=True)
    cliente_propietario = models.CharField(max_length=100, blank=True, null=True)
    inmueble = models.IntegerField(blank=True, null=True)
    cliente_arrendatario = models.CharField(max_length=100, blank=True, null=True)
    fecha_contrato = models.DateField(blank=True, null=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_vigencia = models.DateField(blank=True, null=True)
    precio_canon = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    servicios_arrendador = models.CharField(max_length=255, blank=True, null=True)
    servicios_arrendatario = models.CharField(max_length=255, blank=True, null=True)
    codeudor1 = models.CharField(max_length=100, blank=True, null=True)
    codeudor2 = models.CharField(max_length=100, blank=True, null=True)
    codeudor3 = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contratos'


class Gastos(models.Model):
    programa = models.CharField(max_length=20, blank=True, null=True)
    id_asociado = models.IntegerField(blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    valor = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gastos'


class ImagenesInmueble(models.Model):
    id_asociado = models.IntegerField(blank=True, null=True)
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'imagenes_inmueble'


class Inmuebles(models.Model):
    representante = models.CharField(max_length=100, blank=True, null=True)
    cliente_propietario = models.CharField(max_length=100, blank=True, null=True)
    pais = models.CharField(max_length=100, blank=True, null=True)
    departamento = models.CharField(max_length=100, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    zona = models.CharField(max_length=100, blank=True, null=True)
    barrio = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=100, blank=True, null=True)
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

    class Meta:
        managed = False
        db_table = 'inmuebles'


class Personas(models.Model):
    tipo_persona = models.CharField(max_length=100, blank=True, null=True)
    asesor = models.CharField(max_length=100, blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    tipo_identificacion = models.CharField(max_length=100, blank=True, null=True)
    identificacion = models.CharField(max_length=100, blank=True, null=True)
    lugar_expedicion_identificacion = models.CharField(max_length=100, blank=True, null=True)
    pais = models.CharField(max_length=100, blank=True, null=True)
    departamento = models.CharField(max_length=100, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    telefono_movil = models.CharField(max_length=100, blank=True, null=True)
    telefono_fijo = models.CharField(max_length=100, blank=True, null=True)
    correo = models.CharField(max_length=200, blank=True, null=True)
    valoracion = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'personas'
