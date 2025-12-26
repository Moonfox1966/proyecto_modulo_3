# Archivo: main.py
# Sistema de Registro de Pasajeros en un Hotel
# Este archivo orquesta el menú principal y conecta con los módulos del sistema

from modulos.entradas import (
    pedir_texto,
    pedir_habitacion,
    pedir_fecha,
    pedir_estado,
    pedir_documento,
)
from modulos.operaciones import (
    crear_estructura,
    registrar_pasajero,
    listar_pasajeros,
    sincronizar_desde_csv,
    buscar_por_documento,
    actualizar_pasajero,
    eliminar_pasajero,
    buscar_pasajero_por_habitacion,
)


def mostrar_menu() -> None:
    # Muestra el menú principal del sistema
    print("\n--- Sistema de Registro de Pasajeros ---")
    print("1. Registrar pasajero (check-in)")
    print("2. Listar pasajeros")
    print("3. Buscar pasajero por documento")
    print("4. Actualizar datos de pasajero")
    print("5. Eliminar pasajero")
    print("6. Buscar pasajero por habitación (recursivo)")
    print("7. Salir")


def accion_registrar(sistema: dict) -> None:
    # Captura los datos del pasajero y lo registra en el sistema
    if sincronizar_desde_csv(sistema):
        print("Datos sincronizados desde datos_prueba.csv.")
    pasajero = {
        "nombre": pedir_texto("Nombre: "),
        "documento": pedir_documento("Documento (RUT o ID/Pasaporte): "),

        "nacionalidad": pedir_texto("Nacionalidad: "),
        "habitacion": pedir_habitacion("Número de habitación: "),
        "fecha_ingreso": pedir_fecha("Fecha de ingreso (DD-MM-YYYY): "),
        "fecha_salida": pedir_fecha("Fecha de salida (DD-MM-YYYY): "),
        "estado": pedir_estado("Estado"),
    }

    if registrar_pasajero(sistema, pasajero):
        print("Pasajero registrado correctamente.")
    else:
        print("Error: documento duplicado o habitación ocupada.")


def accion_listar(sistema: dict) -> None:
    # Muestra todos los pasajeros registrados
    if sincronizar_desde_csv(sistema):
        print("Datos sincronizados desde datos_prueba.csv.")
    pasajeros = listar_pasajeros(sistema)

    if not pasajeros:
        print("No hay pasajeros registrados.")
        return

    print("\n--- Lista de Pasajeros ---")
    for p in pasajeros:
        print(
            f"{p['documento']} | {p['nombre']} | "
            f"{p['nacionalidad']} | Hab {p['habitacion']} | {p['estado']}"
        )


def accion_buscar_documento(sistema: dict) -> None:
    # Busca un pasajero por documento
    if sincronizar_desde_csv(sistema):
        print("Datos sincronizados desde datos_prueba.csv.")
    documento = pedir_documento("Documento a buscar: ")
    pasajero = buscar_por_documento(sistema, documento)

    if pasajero is None:
        print("Pasajero no encontrado.")
    else:
        print(
            f"{pasajero['documento']} | {pasajero['nombre']} | "
            f"Hab {pasajero['habitacion']} | {pasajero['estado']}"
        )


def accion_actualizar(sistema: dict) -> None:
    # Actualiza los datos de un pasajero existente
    if sincronizar_desde_csv(sistema):
        print("Datos sincronizados desde datos_prueba.csv.")
    documento = pedir_documento("Documento del pasajero a actualizar: ")

    cambios = {
        "nombre": pedir_texto("Nuevo nombre: "),
        "nacionalidad": pedir_texto("Nueva nacionalidad: "),
        "habitacion": pedir_habitacion("Nueva habitación: "),
        "fecha_ingreso": pedir_fecha("Nueva fecha ingreso (DD-MM-YYYY): "),
        "fecha_salida": pedir_fecha("Nueva fecha salida (DD-MM-YYYY): "),
        "estado": pedir_estado("Nuevo estado"),
    }

    if actualizar_pasajero(sistema, documento, cambios):
        print("Pasajero actualizado correctamente.")
    else:
        print("Error: pasajero no existe o habitación ocupada.")


def accion_eliminar(sistema: dict) -> None:
    # Elimina un pasajero del sistema
    if sincronizar_desde_csv(sistema):
        print("Datos sincronizados desde datos_prueba.csv.")
    documento = pedir_documento("Documento del pasajero a eliminar: ")

    if eliminar_pasajero(sistema, documento):
        print("Pasajero eliminado correctamente.")
    else:
        print("Error: pasajero no encontrado.")


def accion_buscar_habitacion(sistema: dict) -> None:
    # Busca un pasajero usando función recursiva
    if sincronizar_desde_csv(sistema):
        print("Datos sincronizados desde datos_prueba.csv.")
    habitacion = pedir_habitacion("Número de habitación a buscar: ")
    pasajero = buscar_pasajero_por_habitacion(sistema, habitacion)

    if pasajero is None:
        print("No hay pasajero asignado a esa habitación.")
    else:
        print(
            f"{pasajero['documento']} | {pasajero['nombre']} | "
            f"Hab {pasajero['habitacion']} | {pasajero['estado']}"
        )


def main() -> None:
    # Punto de entrada principal del sistema
    sistema = crear_estructura()
    opcion = ""

    while opcion != "7":
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            accion_registrar(sistema)
        elif opcion == "2":
            accion_listar(sistema)
        elif opcion == "3":
            accion_buscar_documento(sistema)
        elif opcion == "4":
            accion_actualizar(sistema)
        elif opcion == "5":
            accion_eliminar(sistema)
        elif opcion == "6":
            accion_buscar_habitacion(sistema)
        elif opcion == "7":
            print("Saliendo del sistema...")
        else:
            print("Opción no válida. Intente nuevamente.")


# Ejecución directa del programa
if __name__ == "__main__":
    main()
