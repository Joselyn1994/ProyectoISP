
# Importamos ValidationError para mostrar errores de validación en Django.
from django.core.exceptions import ValidationError


# Creamos una función para validar las cédulas ecuatorianas.
def validar_cedula_ecuatoriana(cedula):

    # Comprobamos que el valor recibido sea una cadena de texto.
    if not isinstance(cedula, str):
        raise ValidationError(
            'La cédula debe ser ingresada como texto.'
        )

    # Verificamos que contenga exactamente 10 dígitos numéricos.
    if not cedula.isdigit() or len(cedula) != 10:
        raise ValidationError(
            'La cédula debe contener exactamente 10 números.'
        )

    # Convertimos cada carácter de la cédula en un número entero.
    digitos = [int(numero) for numero in cedula]

    # Obtenemos el tercer dígito de la cédula.
    tercer_digito = digitos[2]

    # Comprobamos que corresponda a una persona natural.
    if tercer_digito < 0 or tercer_digito > 5:
        raise ValidationError(
            'La cédula no corresponde a una persona natural.'
        )

    # Inicializamos una variable para acumular los resultados.
    suma = 0

    # Recorremos los primeros nueve dígitos de la cédula.
    for posicion in range(9):

        # Obtenemos el número de la posición actual.
        valor = digitos[posicion]

        # Multiplicamos por 2 las posiciones pares.
        if posicion % 2 == 0:
            valor *= 2

        # Restamos 9 cuando el resultado es mayor o igual a 10.
        if valor >= 10:
            valor -= 9

        # Acumulamos el resultado de cada operación.
        suma += valor

    # Calculamos el residuo de la suma al dividirla para 10.
    residuo = suma % 10

    # Calculamos el dígito verificador correspondiente.
    verificador = 0 if residuo == 0 else 10 - residuo

    # Comparamos el verificador calculado con el último dígito.
    if verificador != digitos[9]:
        raise ValidationError(
            'La cédula ecuatoriana no es válida.'
        )

    # Devolvemos True cuando todas las comprobaciones son correctas.
    return True
