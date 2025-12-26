# modulos/rut.py
# Validación de RUT chileno (cálculo y verificación del dígito verificador)


def limpiar_rut(rut: str) -> str:
    # Elimina puntos, guion y espacios; deja solo números + K si existe.
    return rut.strip().replace(".", "").replace("-", "").upper()


def calcular_dv(cuerpo_rut: str) -> str:
    # Calcula el dígito verificador (DV) del RUT a partir del cuerpo (sin DV).
    suma = 0
    multiplicador = 2

    for digito in reversed(cuerpo_rut):
        suma += int(digito) * multiplicador
        multiplicador += 1

        if multiplicador > 7:
            multiplicador = 2

    resto = 11 - (suma % 11)

    if resto == 11:
        return "0"
    if resto == 10:
        return "K"
    return str(resto)


def validar_rut(rut: str) -> bool:
    # Verifica que el DV ingresado coincida con el DV calculado.
    rut_limpio = limpiar_rut(rut)

    if len(rut_limpio) < 2:
        return False

    cuerpo = rut_limpio[:-1]
    dv_ingresado = rut_limpio[-1]

    if not cuerpo.isdigit():
        return False

    if dv_ingresado not in "0123456789K":
        return False

    return dv_ingresado == calcular_dv(cuerpo)


def formatear_rut(rut: str) -> str | None:
    # Devuelve el RUT normalizado como "12345678-9" o None si no es válido.
    if not validar_rut(rut):
        return None

    rut_limpio = limpiar_rut(rut)
    return f"{rut_limpio[:-1]}-{rut_limpio[-1]}"