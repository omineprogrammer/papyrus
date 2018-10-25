from django import forms
from apps.inventario.models import ModeloImpresora


class ModeloImpresoraForm(forms.ModelForm):

    class Meta:
        model = ModeloImpresora
        fields = [
            'fabricante',
            'modelo',
            'tipo',
            'conexion_local',
            'conexion_red_cableada',
            'conexion_red_inalambrica'
        ]

        labels = {
            'fabricante': 'Fabricante de impresora',
            'modelo': 'Modelo',
            'tipo': 'Tipo de Impresion',
            'conexion_local': 'Conexion Local',
            'conexion_red_cableada': 'Conexion LAN',
            'conexion_red_inalambrica': 'Conexion por WiFi',
        }

        widgets = {
            'fabricante': forms.Select(attrs={
                'class': 'form-control'
            }),
            'modelo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese modelo de impresora'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese tipo de impresora'
            }),
            'conexion_local': forms.CheckboxInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter quantity in Hz'
            }),
            'conexion_red_cableada': forms.CheckboxInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter quantity in Bytes'
            }),
            'conexion_red_inalambrica': forms.CheckboxInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter quantity in Bytes'
            })
        }