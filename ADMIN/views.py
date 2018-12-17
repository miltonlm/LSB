import json
import locale
from datetime import datetime
from urllib.parse import quote_plus
from urllib.request import urlopen

import pdfkit
from django.core import serializers
from django.http import HttpResponse, FileResponse
from django.shortcuts import render

from ADMIN.numero_letras import numero_a_moneda, numero_a_letras
from .forms import FI, FP, FC
from .models import Personas, Inmuebles, Contratos


def index(request):
    context = {
    }

    return render(request, 'index.html', context)


def p(request):
    if request.method == 'POST':
        form = FP(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponse(content=json.dumps({'ok': True}), content_type="application/json")
        else:
            return HttpResponse(content=json.dumps({'ok': True}), content_type="application/json")
    else:
        data = Personas.objects.all()
        context = {
            'form': FP(),
            'data': serializers.serialize("python", data),
            'data2': data,
            'nombre_programa': "Personas"
        }
        return render(request, 'crud.html', context)


def inm(request):
    if request.method == 'POST':
        form = FI(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponse(json.dumps({'ok': True}))
        else:
            return HttpResponse(json.dumps({'ok': False}))
    else:
        data = Inmuebles.objects.all()
        form = FI()

        if 'id' in request.GET:
            dataf = Inmuebles.objects.filter(id=request.GET["id"])

            return HttpResponse(serializers.serialize("json", dataf))

        context = {
            'form': form,
            'data': serializers.serialize("python", data),
            'data2': data,
            'nombre_programa': "Inmuebles"
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
                "https://maps.googleapis.com/maps/api/geocode/json?address=" + address + "&key=AIzaSyA73XI98g4X_eyF3G5b8chj-E37bVgrBPY")
            texto = url.read()

            return HttpResponse(texto)
        elif funcion == "geoimage":
            location = request.POST["location"]

            url = urlopen("https://maps.googleapis.com/maps/api/streetview?size=400x400&location=" + location +
                          "&fov=90&heading=235&pitch=10&key=AIzaSyA73XI98g4X_eyF3G5b8chj-E37bVgrBPY")
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
                          "&fov=90&heading=235&pitch=10&key=AIzaSyA73XI98g4X_eyF3G5b8chj-E37bVgrBPY")
            imagen = url.read()

            response = HttpResponse(imagen, content_type="image/jpeg")
            response["Content-Disposition"] = "attachment; filename=\"imagen.jpg\""

            return response


def ct(request):
    if request.method == 'POST':
        form = FC(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponse(json.dumps({'ok': True}))
        else:
            return HttpResponse(json.dumps({'ok': False}))
    else:
        data = Contratos.objects.all()
        form = FC

        if 'id' in request.GET:
            dataf = Contratos.objects.filter(id=request.GET["id"])

            return HttpResponse(serializers.serialize("json", dataf))

        context = {
            'form': form,
            'data': serializers.serialize("python", data),
            'data2': data,
            'nombre_programa': "Contratos"
        }

        return render(request, 'crud.html', context)


def si(request):
    context = {

    }

    return render(request, "inmueble.html", context)


def ctpdf(request):
    id = request.GET["id"]
    contrato = Contratos.objects.filter(id=id).first()
    im = Inmuebles.objects.filter(id=contrato.inmueble).first()
    cp = Personas.objects.filter(identificacion=contrato.cliente_propietario).first()
    ca = Personas.objects.filter(identificacion=contrato.cliente_arrendatario).first()
    ar = Personas.objects.filter(id=cp.asesor).first()

    fecha_inicio = datetime.strptime(contrato.fecha_inicio, "%Y-%m-%d")
    fecha_vigencia = datetime.strptime(contrato.fecha_vigencia, "%Y-%m-%d")

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

    sa = "" + contrato.servicios_arrendatario

    sa = sa.replace("'", "")
    sa = sa.replace("[", "")
    sa = sa.replace("]", "")

    context = {
        'arrendador': ar.nombre + ", " + ar.tipo_identificacion + " " + ar.identificacion,
        'arrendatario': ca.nombre + ", " + ca.tipo_identificacion + " " + ca.identificacion,
        'direccion_inmueble': im.direccion + ", " + im.ciudad + ", " + im.departamento + ", " + im.pais,
        'precio_canon': '{} {}'.format(locale.currency(contrato.precio_canon, grouping=True),
                                       numero_a_moneda(contrato.precio_canon).upper()),
        'termino_contrato': round((fecha_vigencia - fecha_inicio).days / 30, 0),
        'fecha_inicio': fecha_inicio,
        'fecha_vencimiento': fecha_vigencia,
        'servicios_arrendatario': sa,
        'parte_arrendadora': parte_arrendadora,
        'parte_arrendataria': parte_arrendataria
    }

    rp = render(request, "contrato1.html", context)

    f = open("contrato123.html", "wb")

    f.write(rp.content)
    f.flush()
    f.close()

    pdfkit.from_file("contrato123.html", "contrato.pdf")
    rp = FileResponse(open("contrato.pdf", "rb"), as_attachment=True, filename="contrato.pdf",
                      content_type="application/pdf")

    return rp
