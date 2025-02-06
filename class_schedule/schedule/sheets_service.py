import json
import google.auth
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1yoY3KDOB1RRTbesi6UUjE3q7EFPjc9rTHJtVKuRfucQ"


def get_service():
    """Autenticar con Google Sheets API"""
    creds = Credentials.from_service_account_file("baristamed-6c80d046e9bf.json", scopes=SCOPES)
    return build("sheets", "v4", credentials=creds)


def read_schedule():
    """Leer todas las clases almacenadas en la hoja y convertir profesores y alumnos a listas"""
    service = get_service()
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="A1:Z100").execute()
    values = result.get("values", [])

    clases = []
    for row_idx, row in enumerate(values, start=1):
        for col_idx, cell in enumerate(row, start=1):
            try:
                clase = json.loads(cell)  # Convertir el contenido de la celda a JSON
                clase["row"] = row_idx
                clase["col"] = col_idx

                # Convertir profesores y alumnos a listas
                clase["profesores"] = json.loads(clase["profesores"]) if isinstance(clase["profesores"], str) else clase["profesores"]
                clase["alumnos"] = json.loads(clase["alumnos"]) if isinstance(clase["alumnos"], str) else clase["alumnos"]

                clases.append(clase)
            except (json.JSONDecodeError, KeyError):
                continue  # Ignorar celdas vacías o con datos inválidos

    return clases


def check_existing_class(fecha, hora):
    """Verificar si ya hay una clase en el mismo horario"""
    clases = read_schedule()
    for clase in clases:
        if clase["fecha"] == fecha and clase["hora"] == hora:
            return True
    return False

def find_next_available_row(service, spreadsheet_id, col):
    """Encuentra la primera fila vacía en la columna seleccionada"""
    sheet = service.spreadsheets()
    col_letter = chr(64 + col)  # Convierte el número de columna en letra (Ej: 2 -> 'B')
    range_col = f"{col_letter}:{col_letter}"  # Rango de toda la columna (Ej: 'B:B')

    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_col).execute()
    values = result.get("values", [])

    # Si la columna está vacía, devuelve la fila 1
    if not values:
        return 1

    return len(values) + 1  # La siguiente fila vacía

def write_class(col, clase):
    """Escribir o actualizar una clase en una celda específica"""
    if check_existing_class(clase.fecha, clase.hora):
        raise ValueError("Ya existe una clase en este horario")

    service = get_service()
    sheet = service.spreadsheets()

    
    row = find_next_available_row(service, SPREADSHEET_ID, col)
    print(f"Fila calculada: {row}")  # Imprime el valor de row para verificar

    cell = f"{chr(64 + col)}{row}"

    values = [[json.dumps({
        "fecha": clase.fecha,
        "hora": clase.hora,
        "profesores": clase.profesores,
        "alumnos": clase.alumnos
    })]]

    body = {"values": values}

    sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=cell,
        valueInputOption="RAW",
        body=body
    ).execute()


def delete_class(row, col):
    """Borrar el contenido de una celda específica"""
    service = get_service()
    sheet = service.spreadsheets()
    cell = f"{chr(64 + col)}{row}"

    body = {"values": [[""]]}
    sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=cell, valueInputOption="RAW", body=body).execute()