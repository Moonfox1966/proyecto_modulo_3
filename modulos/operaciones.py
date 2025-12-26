# Archivo: modulos/operaciones.py
# Lógica principal del sistema de registro de pasajeros

from __future__ import annotations

import csv
from pathlib import Path

# Tupla con campos fijos del pasajero (datos inmutables)
CAMPOS_PASAJERO = (
    "nombre",
    "documento",
    "nacionalidad",
    "habitacion",
    "fecha_ingreso",
    "fecha_salida",
    "estado",
)

CAMPOS_CSV = (
    "documento",
    "nombre",
    "nacionalidad",
    "habitacion",
    "fecha_ingreso",
    "fecha_salida",
    "estado",
)


def _ruta_csv_por_defecto() -> Path:
    # Ruta del CSV de ejemplo dentro del proyecto
    return Path(__file__).resolve().parents[1] / "data" / "datos_prueba.csv"


def _normalizar_registro(fila: dict) -> dict | None:
    # Limpia y convierte tipos desde el CSV
    try:
        habitacion = int(fila.get("habitacion", "").strip())
    except ValueError:
        return None

    registro = {
        "documento": fila.get("documento", "").strip(),
        "nombre": fila.get("nombre", "").strip(),
        "nacionalidad": fila.get("nacionalidad", "").strip(),
        "habitacion": habitacion,
        "fecha_ingreso": fila.get("fecha_ingreso", "").strip(),
        "fecha_salida": fila.get("fecha_salida", "").strip(),
        "estado": fila.get("estado", "").strip(),
    }

    if not registro["documento"] or not registro["nombre"]:
        return None

    return registro


def cargar_pasajeros_desde_csv(sistema: dict, ruta: Path | None = None) -> int:
    # Carga pasajeros desde un CSV y devuelve cuántos registros se agregaron
    ruta_final = ruta or _ruta_csv_por_defecto()
    if not ruta_final.exists():
        return 0

    agregados = 0
    with ruta_final.open(newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            registro = _normalizar_registro(fila)
            if registro and registrar_pasajero(sistema, registro, persistir=False):
                agregados += 1

    return agregados


def recargar_desde_csv(sistema: dict, ruta: Path | None = None) -> int:
    # Reemplaza los datos en memoria por el contenido del CSV
    sistema["pasajeros"].clear()
    sistema["habitaciones_ocupadas"].clear()
    sistema["historial"].clear()
    return cargar_pasajeros_desde_csv(sistema, ruta)


def sincronizar_desde_csv(
    sistema: dict,
    ruta: Path | None = None
) -> bool:
    # Recarga y devuelve True si hubo cambios reales en memoria.
    antes = (
        dict(sistema["pasajeros"]),
        set(sistema["habitaciones_ocupadas"]),
        list(sistema["historial"]),
    )
    recargar_desde_csv(sistema, ruta)
    despues = (
        sistema["pasajeros"],
        sistema["habitaciones_ocupadas"],
        sistema["historial"],
    )
    return despues != antes


def guardar_pasajeros_a_csv(sistema: dict, ruta: Path | None = None) -> None:
    # Guarda el estado actual en el CSV de ejemplo
    ruta_final = ruta or _ruta_csv_por_defecto()
    pasajeros = list(sistema["pasajeros"].values())
    pasajeros.sort(key=lambda p: p.get("documento", ""))

    with ruta_final.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=CAMPOS_CSV)
        escritor.writeheader()
        for pasajero in pasajeros:
            escritor.writerow(
                {campo: pasajero.get(campo, "") for campo in CAMPOS_CSV}
            )


def crear_estructura(cargar_csv: bool = True) -> dict:
    # Crea la estructura principal del sistema
    sistema = {
        "pasajeros": {},                 # dict: documento -> datos del pasajero
        "historial": [],                 # list: registro de acciones
        "habitaciones_ocupadas": set(),  # set: habitaciones en uso
    }
    if cargar_csv:
        cargar_pasajeros_desde_csv(sistema)
    return sistema


def registrar_pasajero(
    sistema: dict,
    pasajero: dict,
    persistir: bool = True
) -> bool:
    # Registra un pasajero si no existe y la habitación está libre
    documento = pasajero.get("documento")
    habitacion = pasajero.get("habitacion")

    if documento in sistema["pasajeros"]:
        return False

    if habitacion in sistema["habitaciones_ocupadas"]:
        return False

    sistema["pasajeros"][documento] = pasajero
    sistema["habitaciones_ocupadas"].add(habitacion)
    sistema["historial"].append(f"CHECK-IN: {documento}")
    if persistir:
        guardar_pasajeros_a_csv(sistema)
    return True


def listar_pasajeros(sistema: dict) -> list:
    # Devuelve una lista con todos los pasajeros
    return list(sistema["pasajeros"].values())


def buscar_por_documento(sistema: dict, documento: str) -> dict | None:
    # Busca un pasajero por su documento
    return sistema["pasajeros"].get(documento)


def actualizar_pasajero(
    sistema: dict,
    documento: str,
    cambios: dict,
    persistir: bool = True
) -> bool:
    # Actualiza los datos de un pasajero existente
    pasajero = sistema["pasajeros"].get(documento)
    if pasajero is None:
        return False

    # Validar cambio de habitación
    if "habitacion" in cambios:
        nueva = cambios["habitacion"]
        actual = pasajero.get("habitacion")

        if nueva != actual and nueva in sistema["habitaciones_ocupadas"]:
            return False

        sistema["habitaciones_ocupadas"].discard(actual)
        sistema["habitaciones_ocupadas"].add(nueva)

    pasajero.update(cambios)
    sistema["historial"].append(f"UPDATE: {documento}")
    if persistir:
        guardar_pasajeros_a_csv(sistema)
    return True


def eliminar_pasajero(
    sistema: dict,
    documento: str,
    persistir: bool = True
) -> bool:
    # Elimina un pasajero y libera su habitación
    pasajero = sistema["pasajeros"].pop(documento, None)
    if pasajero is None:
        return False

    habitacion = pasajero.get("habitacion")
    sistema["habitaciones_ocupadas"].discard(habitacion)
    sistema["historial"].append(f"DELETE: {documento}")
    if persistir:
        guardar_pasajeros_a_csv(sistema)
    return True


# -------- FUNCIÓN RECURSIVA --------

def buscar_por_habitacion_recursivo(
    pasajeros: list,
    habitacion: int,
    indice: int = 0
) -> dict | None:
    # Búsqueda recursiva de pasajero por habitación
    if indice >= len(pasajeros):
        return None

    if pasajeros[indice].get("habitacion") == habitacion:
        return pasajeros[indice]

    return buscar_por_habitacion_recursivo(
        pasajeros,
        habitacion,
        indice + 1
    )


def buscar_pasajero_por_habitacion(
    sistema: dict,
    habitacion: int
) -> dict | None:
    # Función envolvente para la búsqueda recursiva
    pasajeros = list(sistema["pasajeros"].values())
    return buscar_por_habitacion_recursivo(pasajeros, habitacion)
