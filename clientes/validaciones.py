# Importamos ValidationError para mostrar errores de validación en Django.
from django.core.exceptions import ValidationError


# Creamos una función que recibe una cédula ecuatoriana.
def validar_cedula_ecuatoriana(cedula):

    # Comprobamos que la cédula contenga exactamente 10 dígitos.
    if not cedula.isdigit() or len(cedula) != 10:
        raise ValidationError(
            'La cédula debe contener exactamente 10 números.'
        )

    # Convertimos la cédula en una lista de números enteros.
    digitos = [int(numero) for numero in cedula]

    # Obtenemos el tercer dígito, que identifica el tipo de persona.
    tercer_digito = digitos[2]

    # Verificamos que corresponda a una cédula de persona natural.
    if tercer_digito < 0 or tercer_digito > 5:
        raise ValidationError(
            'La cédula no corresponde a una persona natural.'
        )

    # Inicializamos la variable que acumulará los resultados.
    suma = 0

    # Recorremos los primeros nueve dígitos de la cédula.
    for posicion in range(9):

        # Obtenemos el dígito de la posición actual.
        valor = digitos[posicion]

        # Multiplicamos por 2 las posiciones pares y por 1 las impares.
        if posicion % 2 == 0:
            valor *= 2

        # Si el resultado es mayor o igual a 10, restamos 9.
        if valor >= 10:
            valor -= 9

        # Sumamos el resultado al acumulador.
        suma += valor

    # Calculamos el residuo de la suma al dividirla para 10.
    residuo = suma % 10

    # Calculamos el dígito verificador esperado.
    verificador = 0 if residuo == 0 else 10 - residuo

    # Comparamos el dígito calculado con el décimo dígito de la cédula.
    if verificador != digitos[9]:
        raise ValidationError(
            'La cédula ecuatoriana no es válida.'
        )

    # Si supera todas las comprobaciones, la cédula es válida.
    return True