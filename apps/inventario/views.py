from django.shortcuts import render, redirect
from django.contrib import admin
from django.http import  HttpResponse

from apps.inventario.forms import *


def addImpresora(request):
    if request.method == 'POST':
        form = ModeloImpresoraForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('inventario:addImpresora')
    else:
        form = ModeloImpresoraForm()
    return render(request, 'inventario/addImpresora.html', {'form': form})