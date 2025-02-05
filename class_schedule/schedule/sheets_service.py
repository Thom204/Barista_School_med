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
    """Leer todas las clases almacenadas en la hoja"""
    service = get_service()
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="A1:Z100").execute()
    values = result.get("values", [])

    clases = []
    for row_idx, row in enumerate(values, start=1):
        for col_idx, cell in enumerate(row, start=1):
            try:
                clase = json.loads(cell)
                clase["row"] = row_idx
                clase["col"] = col_idx
                clases.append(clase)
            except json.JSONDecodeError:
                continue  # Ignorar celdas vacías o con datos no válidos

    return clases


def check_existing_class(fecha, hora):
    """Verificar si ya hay una clase en el mismo horario"""
    clases = read_schedule()
    for clase in clases:
        if clase["fecha"] == fecha and clase["hora"] == hora:
            return True
    return False


def write_class(row, col, clase):
    """Escribir o actualizar una clase en una celda específica"""
    if check_existing_class(clase.fecha, clase.hora):
        raise ValueError("Ya existe una clase en este horario")

    service = get_service()
    sheet = service.spreadsheets()
    cell = f"{chr(64 + col)}{row}"

    values = [[json.dumps({
        "fecha": clase.fecha,
        "hora": clase.hora,
        "profesores": clase.profesores,
        "alumnos": clase.alumnos
    })]]

    body = {"values": values}
    sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=cell, valueInputOption="RAW", body=body).execute()


def delete_class(row, col):
    """Borrar el contenido de una celda específica"""
    service = get_service()
    sheet = service.spreadsheets()
    cell = f"{chr(64 + col)}{row}"

    body = {"values": [[""]]}
    sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=cell, valueInputOption="RAW", body=body).execute()