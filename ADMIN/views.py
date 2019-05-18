from datetime import datetime
from urllib.parse import quote_plus
from urllib.request import urlopen

from django.core import serializers
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from ADMIN.numero_letras import numero_a_moneda
from ADMIN.forms import *
from ADMIN.models import *

import json
import locale
import pdfkit
import tempfile
import os


def index(request):
    context = {
    }

    return render(request, 'index.html', context)


def crud(request, tabla, id=0):
    if request.method == 'POST':
        form = eval('Form%s' % tabla)(request.POST)

        if id > 0:
            form = eval('Form%s' % tabla)(
                request.POST,
                instance=eval(tabla).objects.get(pk=id)
            )

        if form.is_valid():
            form.save()
            return HttpResponse(
                content=json.dumps({'ok': True}),
                content_type="application/json"
            )
        else:
            return HttpResponse(
                content=json.dumps({'ok': False, 'errors': form.errors}),
                content_type="application/json"
            )
    elif request.method == 'DELETE':
        if id > 0:
            persona = eval(tabla).objects.get(pk=id)

            persona.delete()

            return HttpResponse(
                json.dumps({'ok': True}),
                content_type="application/json"
            )
    else:
        if id > 0:
            dataf = eval(tabla).objects.get(pk=id)

            return HttpResponse(
                serializers.serialize("json", [dataf]),
                content_type="application/json"
            )

        data = eval(tabla).objects.all()
        context = {
            'form': eval('Form%s' % tabla)(),
            'data': serializers.serialize("python", data),
            'data2': data,
            'nombre_programa': tabla
        }
        return render(request, 'crud.html', context)


def qr(request):
    if request.method == "POST":
        funcion = request.POST["funcion"]

        if funcion == "geoservice":
            pais = "COLOMBIA"
            ciudad = request.POST["ciudad"]
            direccion = request.POST["direccion"]
            address = quote_plus(pais + ", " + ciudad + ", " + direccion)
            url = urlopen(
                "https://maps.googleapis.com/maps/api/geocode/json?address=" + address +
                "&key=AIzaSyA73XI98g4X_eyF3G5b8chj-E37bVgrBPY"
            )
            texto = url.read()

            return HttpResponse(texto)
        elif funcion == "geoimage":
            location = request.POST["location"]

            print("FROM HERE POST")

            url = urlopen(
                "https://maps.googleapis.com/maps/api/streetview?size=400x400&location=" + location +
                          "&fov=90&heading=150&pitch=10&key=AIzaSyA73XI98g4X_eyF3G5b8chj-E37bVgrBPY"
            )
            imagen = url.read()

            response = HttpResponse(imagen, content_type="image/jpeg")
            response["Content-Disposition"] = "attachment; filename=\"imagen.jpg\""

            return response
        elif funcion == "cliente_propietario":
            id = request.POST["id"]
            cp = Personas.objects.filter(identificacion=id)

            data = serializers.serialize("json", cp)

            return HttpResponse(data)
        elif funcion == "cliente_arrendatario":
            id = request.POST["id"]
            cp = Personas.objects.filter(identificacion=id)

            data = serializers.serialize("json", cp)

            return HttpResponse(data)
        elif funcion == "inmuebles":
            tipo_inmueble = request.POST["tipo_inmueble"]
            ubicacion = request.POST["ubicacion"]

            data = Inmuebles.objects.all()
            data = serializers.serialize("json", data)

            return HttpResponse(data)
        elif funcion == "inmuebles_propietario":
            id = request.POST["id"]
            data = Inmuebles.objects.filter(cliente_propietario=id)
            data = serializers.serialize("json", data)

            return HttpResponse(data)
    elif request.method == "GET":
        funcion = request.GET["funcion"]

        if funcion == "geoimage":
            location = request.GET["location"]

            url = urlopen("https://maps.googleapis.com/maps/api/streetview?size=400x400&location=" + location +
                          "&fov=90&heading=150&pitch=10&key=AIzaSyA73XI98g4X_eyF3G5b8chj-E37bVgrBPY")
            imagen = url.read()

            response = HttpResponse(imagen, content_type="image/jpeg")
            response["Content-Disposition"] = "attachment; filename=\"imagen.jpg\""

            return response
        elif funcion == "paises":
            paises = Paises.objects.all().order_by('nombre')

            return HttpResponse(
                serializers.serialize('json', paises),
                content_type="application/json"
            )
        elif funcion == "departamentos":
            pais = request.GET["pais"]
            departamentos = Departamentos.objects.filter(pais=Paises.objects.get(pk=pais)).order_by('nombre')

            return HttpResponse(
                serializers.serialize('json', departamentos),
                content_type="application/json"
            )
        elif funcion == "ciudades":
            departamento = request.GET["departamento"]
            ciudades = Ciudades.objects.filter(departamento=Departamentos.objects.get(pk=departamento)).order_by('nombre')

            return HttpResponse(
                serializers.serialize('json', ciudades),
                content_type="application/json"
            )


def si(request):
    context = {

    }

    return render(request, "inmueble.html", context)


def ctpdf(request):
    id = request.GET["id"]
    contrato = Contratos.objects.get(pk=id)
    im = contrato.inmueble
    cp = contrato.cliente_propietario
    ca = contrato.cliente_arrendatario
    ar = cp.asesor
    cd1 = contrato.codeudor1
    cd2 = contrato.codeudor2
    cd3 = contrato.codeudor3

    fecha_inicio = contrato.fecha_inicio
    fecha_vigencia = contrato.fecha_vigencia

    locale.setlocale(locale.LC_ALL, '')

    parte_arrendadora = ar.nombre + ", " + ar.tipo_identificacion + " " + ar.identificacion
    parte_arrendadora = parte_arrendadora + "<br />"

    if ar.telefono_movil and ar.telefono_movil != "0":
        parte_arrendadora = parte_arrendadora + "TELEFONO MOVIL: " + ar.telefono_movil + "<br />"
    if ar.telefono_fijo and ar.telefono_fijo != "0":
        parte_arrendadora = parte_arrendadora + "TELEFONO FIJO: " + ar.telefono_fijo + "<br />"

    parte_arrendataria = ca.nombre + ", " + ca.tipo_identificacion + " " + ca.identificacion
    parte_arrendataria = parte_arrendataria + "<br />"

    if ca.telefono_movil and ca.telefono_movil != "0":
        parte_arrendataria = parte_arrendataria + "TELEFONO MOVIL: " + ca.telefono_movil + "<br />"
    if ca.telefono_fijo and ca.telefono_fijo != "0":
        parte_arrendataria = parte_arrendataria + "TELEFONO FIJO: " + ca.telefono_fijo + "<br />"

    sar = "" + contrato.servicios_arrendador

    sar = sar.replace("'", "")
    sar = sar.replace("[", "")
    sar = sar.replace("]", "")

    sa = "" + contrato.servicios_arrendatario

    sa = sa.replace("'", "")
    sa = sa.replace("[", "")
    sa = sa.replace("]", "")

    codeudor1 = None
    codeudor2 = None
    codeudor3 = None

    if cd1:
        codeudor1 = "{}, {} {}".format(cd1.nombre, cd1.tipo_identificacion, cd1.identificacion)
    if cd2:
        codeudor2 = "{}, {} {}".format(cd2.nombre, cd2.tipo_identificacion, cd2.identificacion)
    if cd3:
        codeudor3 = "{}, {} {}".format(cd3.nombre, cd3.tipo_identificacion, cd3.identificacion)

    context = {
        'ar': ar,
        'ca': ca,
        'arrendador': ar.nombre + ", " + ar.tipo_identificacion + " " + ar.identificacion,
        'arrendatario': ca.nombre + ", " + ca.tipo_identificacion + " " + ca.identificacion,
        'inmueble': im,
        'direccion_inmueble': im.direccion + ", " + im.ciudad + ", " + im.departamento + ", " + im.pais,
        'precio_canon': '{} ({})'.format(
            numero_a_moneda(contrato.precio_canon).upper(),
            locale.currency(contrato.precio_canon, grouping=True).replace('+', ' '),
        ),
        'termino_contrato': int(round((fecha_vigencia - fecha_inicio).days / 30, 0)),
        'fecha_inicio': str(fecha_inicio),
        'fecha_vencimiento': str(fecha_vigencia),
        'servicios_arrendador': sar,
        'servicios_arrendatario': sa,
        'parte_arrendadora': parte_arrendadora,
        'parte_arrendataria': parte_arrendataria,
        'cd1': cd1,
        'cd2': cd2,
        'cd3': cd3,
        'codeudor1': codeudor1,
        'codeudor2': codeudor2,
        'codeudor3': codeudor3
    }

    rp = render_to_string("contrato/contrato2.html", context)

    file = os.path.join(tempfile.gettempdir(), "contrato{}.pdf".format(im.id))

    tipo_vivienda = 'VIVIENDA URBANA'

    if im.tipo_inmueble == 'LOCAL':
        tipo_vivienda = 'LOCAL COMERCIAL'

    id_im = str(im.id).zfill(4)

    pdfkit.from_string(rp, file, {
        'title': 'CONTRATO DE ARRENDAMIENTO DE {} N° {}-2'.format(tipo_vivienda, id_im),
        '--header-html': 'http://127.0.0.1:{}/lsb/header.php'.format(80),
        '--header-spacing': '10',
        '--footer-html': 'http://127.0.0.1:{}/lsb/footer.php'.format(80),
        '--footer-spacing': '5'
    })

    return FileResponse(
        open(file, "rb"),
        as_attachment=True,
        filename="contrato - {}.pdf".format(id_im),
        content_type="application/pdf"
    )


def importar_paises(request):
    pais = Paises(nombre='COLOMBIA')
    pais.save()

    csv = open(os.path.expanduser('~/Desktop/BD/ciudades.csv'), 'rb')

    line = csv.readline()

    keys = {}

    while line:
        line = str(line.decode('utf-8'))
        line = line.replace('"', '')
        line = line.replace('\n', '')
        parts = line.split(";")

        if parts[0] not in keys:
            dp = Departamentos(nombre=parts[1], pais=pais)

            dp.save()
            keys[parts[0]] = True

        line = csv.readline()

    csv.seek(0)

    line = csv.readline()

    while line:
        line = str(line.decode('utf-8'))
        line = line.replace('"', '')
        line = line.replace('\n', '')
        parts = line.split(";")

        dp = Ciudades(
            nombre=parts[3],
            departamento=Departamentos.objects.filter(nombre=parts[1]).first()
        )

        dp.save()

        line = csv.readline()

    csv.close()
