# Archivo: modulos/entradas.py
# Funciones para solicitar y validar datos ingresados por el usuario

from modulos.documentos import normalizar_documento, parece_rut_chileno

from modulos.validaciones import (
    texto_no_vacio,
    es_entero_positivo,
    es_fecha_dd_mm_yyyy,
)


def pedir_texto(mensaje: str) -> str:
    # Solicita un texto no vacío al usuario
    texto = input(mensaje).strip()

    while not texto_no_vacio(texto):
        print("Error: este campo no puede estar vacío.")
        texto = input(mensaje).strip()

    return texto


def pedir_habitacion(mensaje: str) -> int:
    # Solicita un número de habitación válido (entero positivo)
    valor = input(mensaje).strip()

    while not es_entero_positivo(valor):
        print("Error: la habitación debe ser un número entero positivo.")
        valor = input(mensaje).strip()

    return int(valor)


def pedir_fecha(mensaje: str) -> str:
    # Solicita una fecha con formato dd-mm-yyyy
    valor = input(mensaje).strip()

    while not es_fecha_dd_mm_yyyy(valor):
        print("Error: formato inválido. Use dd-mm-yyyy.")
        valor = input(mensaje).strip()

    return valor


def pedir_estado(mensaje: str) -> str:
    # Solicita el estado de la estadía con opciones controladas
    opciones = {
        "1": "Alojado",
        "2": "Check-out",
    }

    opcion = input(f"{mensaje} (1 = Alojado, 2 = Check-out): ").strip()

    while opcion not in opciones:
        print("Error: opción inválida.")
        opcion = input(f"{mensaje} (1 = Alojado, 2 = Check-out): ").strip()

    return opciones[opcion]

def pedir_documento(mensaje: str) -> str:
    # Pide un documento. Si parece RUT, lo valida como RUT; si no, lo acepta como internacional.
    doc = input(mensaje).strip()
    doc_ok = normalizar_documento(doc)

    while doc_ok is None:
        if parece_rut_chileno(doc):
            print("Error: RUT chileno inválido. Ejemplo: 22222222-2 o 22222222-K")
        else:
            print("Error: documento inválido (mínimo 5 caracteres).")

        doc = input(mensaje).strip()
        doc_ok = normalizar_documento(doc)

    return doc_ok