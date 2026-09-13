import os
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

GMAIL_USER = os.environ["GMAIL_USER"]
GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]
DESTINATARIO = os.environ["DESTINATARIO"]

def obtener_precio(simbolo):
    url = f"https://api.gold-api.com/price/{simbolo}"
    respuesta = requests.get(url, timeout=10)
    respuesta.raise_for_status()
    datos = respuesta.json()
    return float(datos["price"])

def construir_mensaje(precio_oro, precio_plata, razon):
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    cuerpo = f"""Reporte de metales preciosos — {fecha}

Oro (XAU):   ${precio_oro:,.2f} USD por onza
Plata (XAG): ${precio_plata:,.2f} USD por onza

Razón oro/plata: {razon:.2f}
(cuántas onzas de plata equivalen a una onza de oro)
"""
    return cuerpo

def enviar_correo(cuerpo):
    mensaje = MIMEText(cuerpo)
    mensaje["Subject"] = "Reporte diario: Oro, Plata y Razón Oro/Plata"
    mensaje["From"] = GMAIL_USER
    mensaje["To"] = DESTINATARIO

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
        servidor.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        servidor.send_message(mensaje)

if __name__ == "__main__":
    precio_oro = obtener_precio("XAU")
    precio_plata = obtener_precio("XAG")
    razon = precio_oro / precio_plata

    cuerpo = construir_mensaje(precio_oro, precio_plata, razon)
    enviar_correo(cuerpo)
    print("Correo enviado correctamente.")
    print(cuerpo)
