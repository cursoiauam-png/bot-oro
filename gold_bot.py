import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

# Credenciales (se leen de los Secrets de GitHub)
GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")
DESTINATARIO = os.environ.get("DESTINATARIO")

def enviar_reporte():
    try:
        # Obtener precio del oro
        response = requests.get("https://api.gold-api.com/price/XAU", timeout=15)
        response.raise_for_status()
        data = response.json()
        
        price = data["price"]
        updated = data.get("updatedAtReadable", "desconocido")
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        # Crear el correo
        asunto = f"Reporte Diario del Oro - {fecha}"
        
        cuerpo = f"""
Reporte Diario del Precio del Oro
================================

Fecha: {fecha}
Precio XAU/USD: ${price:.2f}
Actualizado: {updated}

--------------------------------
Bot autónomo ejecutado con GitHub Actions
"""
        
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = DESTINATARIO
        msg['Subject'] = asunto
        msg.attach(MIMEText(cuerpo, 'plain'))
        
        # Enviar correo
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.send_message(msg)
        
        print(f"[{fecha}] Correo enviado correctamente → ${price:.2f}")
        
    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    enviar_reporte()
