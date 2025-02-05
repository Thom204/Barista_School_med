from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
import gspread
import django
import pickle
import os


dc_dias= {'lunes': 'B', 
          'martes': 'C', 
          'miercoles': 'D',
          'jueves': 'E',
          'viernes': 'F',
          'sabado': 'G',
          'domingo': 'H'}
 
class dia():
    def __init__(self, nombre):
        codigo= dc_dias[nombre]
        clasesDia= {}

    def setClases(dc):
        clasesDia= dc

SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file"]


# Usamos el archivo de credenciales para el cliente OAuth2
def Usr_Authenticate():
    creds = None
    # El archivo de credenciales de usuario final es un archivo JSON descargado desde Google Cloud Console.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # Si no hay credenciales válidas, ejecutamos el flujo de autenticación
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("Desktop_Client_Open.json", SCOPES)
            creds = flow.run_local_server(port=0)  # Abre una ventana para autenticarte
        # Guardamos las credenciales para la próxima vez
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return creds


def authenticate():
    creds = None
    if os.path.exists('baristamed-6c80d046e9bf.json'):
        creds = Credentials.from_service_account_file('baristamed-6c80d046e9bf.json', scopes=SCOPES)
    else:
        print("El archivo de clave de la cuenta de servicio no se encontró.")
        return None
    return creds

def connect_to_gspread():
    creds = authenticate()
    client = gspread.authorize(creds)
    return client

# Función principal del bucle
def main():
    client = None
    # Bucle de comandos

    if client is None:
        client = connect_to_gspread()

        # Extraemos el ID de la hoja de cálculo del enlace
        try:
            # El ID de la hoja está entre "/d/" y "/edit"
            spreadsheet_id = '1yoY3KDOB1RRTbesi6UUjE3q7EFPjc9rTHJtVKuRfucQ'

            # Intentamos acceder a la hoja de cálculo por ID
            sheet = client.open_by_key(spreadsheet_id).sheet1
                
            # Obtener y mostrar datos
            data = sheet.get_all_records()

        except Exception as e:
            print(f"Ocurrió un error: {e}")

# Ejecutamos el script
if __name__ == "__main__":
    main()