from modulos.operaciones import (
    crear_estructura,
    registrar_pasajero,
    buscar_por_documento,
    actualizar_pasajero,
    eliminar_pasajero,
    buscar_pasajero_por_habitacion,
)


def test_registrar_pasajero_ok():
    sistema = crear_estructura(cargar_csv=False)
    pasajero = {
        "nombre": "Juan",
        "documento": "123",
        "nacionalidad": "CL",
        "habitacion": 101,
        "fecha_ingreso": "10-01-2025",
        "fecha_salida": "15-01-2025",
        "estado": "Alojado",
    }
    assert registrar_pasajero(sistema, pasajero) is True
    assert "123" in sistema["pasajeros"]
    assert 101 in sistema["habitaciones_ocupadas"]


def test_registrar_documento_duplicado_falla():
    sistema = crear_estructura(cargar_csv=False)
    p1 = {"documento": "123", "habitacion": 101}
    p2 = {"documento": "123", "habitacion": 102}
    assert registrar_pasajero(sistema, p1) is True
    assert registrar_pasajero(sistema, p2) is False


def test_registrar_habitacion_ocupada_falla():
    sistema = crear_estructura(cargar_csv=False)
    p1 = {"documento": "111", "habitacion": 101}
    p2 = {"documento": "222", "habitacion": 101}
    assert registrar_pasajero(sistema, p1) is True
    assert registrar_pasajero(sistema, p2) is False


def test_buscar_por_documento():
    sistema = crear_estructura(cargar_csv=False)
    p = {"documento": "123", "habitacion": 101, "nombre": "Juan"}
    registrar_pasajero(sistema, p)
    encontrado = buscar_por_documento(sistema, "123")
    assert encontrado is not None
    assert encontrado["nombre"] == "Juan"


def test_actualizar_pasajero_cambia_habitacion_ok():
    sistema = crear_estructura(cargar_csv=False)
    p = {"documento": "123", "habitacion": 101, "nombre": "Juan"}
    registrar_pasajero(sistema, p)

    ok = actualizar_pasajero(sistema, "123", {"habitacion": 103, "nombre": "Juan P"})
    assert ok is True
    assert sistema["pasajeros"]["123"]["habitacion"] == 103
    assert 101 not in sistema["habitaciones_ocupadas"]
    assert 103 in sistema["habitaciones_ocupadas"]


def test_actualizar_a_habitacion_ocupada_falla():
    sistema = crear_estructura(cargar_csv=False)
    registrar_pasajero(sistema, {"documento": "111", "habitacion": 200})
    registrar_pasajero(sistema, {"documento": "123", "habitacion": 101})

    ok = actualizar_pasajero(sistema, "123", {"habitacion": 200})
    assert ok is False


def test_eliminar_pasajero_libera_habitacion():
    sistema = crear_estructura(cargar_csv=False)
    registrar_pasajero(sistema, {"documento": "123", "habitacion": 101})
    assert eliminar_pasajero(sistema, "123") is True
    assert "123" not in sistema["pasajeros"]
    assert 101 not in sistema["habitaciones_ocupadas"]


def test_buscar_recursivo_por_habitacion():
    sistema = crear_estructura()
    registrar_pasajero(sistema, {"documento": "123", "habitacion": 101, "nombre": "Juan"})
    encontrado = buscar_pasajero_por_habitacion(sistema, 101)
    assert encontrado is not None
    assert encontrado["documento"] == "123"

    no_encontrado = buscar_pasajero_por_habitacion(sistema, 999)
    assert no_encontrado is None
