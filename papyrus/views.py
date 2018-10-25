from django.shortcuts import render
from django.apps import apps


def base(request):
    print(apps.get_app_config('inventario').name)
    return render(request, 'base/base.html')