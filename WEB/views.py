from django.shortcuts import render
from django.core import serializers
from ADMIN import models

# Create your views here.


def index(request):
    context = {

    }

    return render(request, 'index.html', context)


def login(request):
    context = {

    }

    return render(request, 'login.html', context)


def registrar(request):
    context = {

    }

    return render(request, 'registrar.html', context)