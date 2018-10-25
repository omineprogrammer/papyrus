from django.core.exceptions import ValidationError


def noEqual0(value):
    if value == 0:
        raise ValidationError('no debe ser 0')

# def quantityInStock(value):
#     if value == 0:
#         raise ValidationError('no debe ser 0')