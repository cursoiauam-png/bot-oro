import os
import csv
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

GMAIL_USER = os.environ["GMAIL_USER"]
GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]
DESTINATARIO = os.environ["DESTINATARIO"]

ARCHIVO_HISTORIAL = "historial.csv"
ARCHIVO_GRAFICA = "grafica.png"

def obtener_precio(simbolo):
    url = f"https://api.gold-api.com/price/{simbolo}"
    respuesta = requests.get(url, timeout=10)
    respuesta.raise_for_status()
    datos = respuesta.json()
    return float(datos["price"])

def interpretar_razon(razon):
    if razon < 40:
        return "La plata está relativamente cara frente al oro (razón baja para estándares históricos)."
    elif razon > 80:
        return "El oro está relativamente caro frente a la plata (razón alta para estándares históricos)."
    else:
        return "La razón se encuentra en un rango intermedio, sin una señal extrema en ningún sentido."

def guardar_en_historial(fecha, precio_oro, precio_plata, razon):
    archivo_existe = os.path.isfile(ARCHIVO_HISTORIAL)
    with open(ARCHIVO_HISTORIAL, "a", newline="") as f:
        escritor = csv.writer(f)
        if not archivo_existe:
            escritor.writerow(["fecha", "precio_oro", "precio_plata", "razon"])
        escritor.writerow([fecha, precio_oro, precio_plata, round(razon, 2)])

def generar_grafica():
    fechas = []
    razones = []
    with open(ARCHIVO_HISTORIAL, "r") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            fechas.append(fila["fecha"])
            razones.append(float(fila["razon"]))

    plt.figure(figsize=(8, 4))
    plt.plot(fechas, razones, marker="o")
    plt.title("Razón oro/plata a lo largo del tiempo")
    plt.xlabel("Fecha")
    plt.ylabel("Razón oro/plata")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(ARCHIVO_GRAFICA)
    plt.close()

def construir_mensaje(precio_oro, precio_plata, razon):
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    interpretacion = interpretar_razon(razon)
    cuerpo = f"""Reporte de metales preciosos — {fecha}

Oro (XAU):   ${precio_oro:,.2f} USD por onza
Plata (XAG): ${precio_plata:,.2f} USD por onza

Razón oro/plata: {razon:.2f}
(cuántas onzas de plata equivalen a una onza de oro)

Lectura del día: {interpretacion}

Se adjunta la gráfica con el historial acumulado hasta hoy.
"""
    return cuerpo

def enviar_correo(cuerpo):
    mensaje = MIMEMultipart()
    mensaje["Subject"] = "Reporte diario: Oro, Plata y Razón Oro/Plata"
    mensaje["From"] = GMAIL_USER
    mensaje["To"] = DESTINATARIO
    mensaje.attach(MIMEText(cuerpo))

    with open(ARCHIVO_GRAFICA, "rb") as f:
        imagen = MIMEImage(f.read())
        imagen.add_header("Content-Disposition", "attachment", filename=ARCHIVO_GRAFICA)
        mensaje.attach(imagen)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
        servidor.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        servidor.send_message(mensaje)

if __name__ == "__main__":
    precio_oro = obtener_precio("XAU")
    precio_plata = obtener_precio("XAG")
    razon = precio_oro / precio_plata
    fecha_hoy = datetime.now().strftime("%Y-%m-%d %H:%M")

    guardar_en_historial(fecha_hoy, precio_oro, precio_plata, razon)
    generar_grafica()

    cuerpo = construir_mensaje(precio_oro, precio_plata, razon)
    enviar_correo(cuerpo)
    print("Correo enviado correctamente.")
    print(cuerpo)
