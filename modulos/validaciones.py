# modulos/validaciones.py
# Funciones de validación para asegurar datos correctos.

def texto_no_vacio(texto: str) -> bool:
    # Valida que el texto no esté vacío (luego de quitar espacios).
    return texto.strip() != ""


def es_entero_positivo(valor: str) -> bool:
    # Valida que el string represente un entero positivo (1, 2, 3, ...).
    return valor.isdigit() and int(valor) > 0


def es_fecha_dd_mm_yyyy(valor: str) -> bool:
    # Valida una fecha con formato dd-mm-yyyy.
    if not valor:
        return False

    partes = valor.split("-")
    if len(partes) != 3:
        return False

    dia, mes, anio = partes
    if not (dia.isdigit() and mes.isdigit() and anio.isdigit()):
        return False

    dia_i = int(dia)
    mes_i = int(mes)
    anio_i = int(anio)

    if anio_i < 1900 or mes_i < 1 or mes_i > 12 or dia_i < 1:
        return False

    dias_por_mes = {
        1: 31,
        2: 29 if _es_bisiesto(anio_i) else 28,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31,
    }

    return dia_i <= dias_por_mes[mes_i]


def _es_bisiesto(anio: int) -> bool:
    return anio % 400 == 0 or (anio % 4 == 0 and anio % 100 != 0)
