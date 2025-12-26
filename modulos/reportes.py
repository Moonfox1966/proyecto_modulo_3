# modulos/reportes.py
# Funciones relacionadas con reportes y visualización de información

def mostrar_historial(sistema: dict) -> None:
    # Muestra el historial de acciones del sistema
    historial = sistema.get("historial", [])

    if not historial:
        print("No hay acciones registradas.")
        return

    print("\n--- Historial de acciones ---")
    for accion in historial:
        print(accion)