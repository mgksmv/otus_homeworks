from django.core.exceptions import ValidationError


def only_int(value):
    if not value.isdigit():
        raise ValidationError('В номере телефона разрешены только цифры!')
