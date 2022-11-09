from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3

import Agente


def creandoReporte(agente: Agente):

    try:
        c = canvas.Canvas("reporte"+agente.ip+".pdf", pagesize=A3)
        text = c.beginText(100, 1150)
        text.setFont("Times-Roman", 18)
        text.textLine("Administracion de servicios en Red")
        text.textLine("Practica 1")
        text.textLine("Reporte del algente")

        text.setFont("Times-Roman", 14)
        text.textLine("Zacarias Pineda Esmeralda")
        text.textLine("Informacion del agente")

        text.setFont("Times-Roman", 12)
        c.drawImage("img/"+str(agente.sistemaOperativo)+".jpg", 400,1000, width = 100, height = 100)
        text.textLine("Sistema Operativo: " + str(agente.sistemaOperativo))
        text.textLine("Version: " + str(agente.versionSO))
        text.textLine("Nombre del dispositivo: " + str(agente.nombreAgente))
        text.textLine("Informacion de contacto: " + str(agente.contacto))
        text.textLine("Ubicacion: " + str(agente.ubicacion))
        text.textLine("Numero de interfaces: " + str(agente.numeroInterfaces))
        text.textLine("1 .- up")
        text.textLine("2.- down")
        text.textLine("6.- notPresent")
        i = 1
        while( i <= int(agente.numeroInterfaces)):
            text.textLine("Interfaz " + str(i) + " estado: " + str(agente.interfaces[i]))
            i += 1

        c.drawText(text)
        c.save()

    except Exception as e:
        print("Error al crear el PDF: " + str(e))
