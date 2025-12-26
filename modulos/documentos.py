# Archivo: modulos/documentos.py
# Validación flexible de documentos: RUT chileno (si corresponde) o documento internacional

from modulos.rut import formatear_rut


def parece_rut_chileno(documento: str) -> bool:
    # Heurística: detecta si el texto "parece" un RUT.
    doc = documento.strip().upper()

    if doc == "":
        return False

    # Indicadores típicos de RUT: guion/puntos o DV K.
    if "-" in doc or "." in doc:
        return True

    # Si termina en K o dígito, y lo demás son dígitos, también puede ser RUT.
    if doc[-1] in "0123456789K":
        cuerpo = doc[:-1]
        return cuerpo.isdigit()

    return False


def normalizar_documento(documento: str) -> str | None:
    # Si parece RUT, lo valida y devuelve formateado. Si no, devuelve normalizado simple.
    doc = documento.strip()

    if doc == "":
        return None

    if parece_rut_chileno(doc):
        return formatear_rut(doc)  # None si es inválido

    # Documento internacional: normalización simple (sin imponer formato país-específico)
    # Puedes ajustar el mínimo de largo si quieres.
    doc_norm = doc.upper()
    if len(doc_norm) < 5:
        return None

    return doc_norm