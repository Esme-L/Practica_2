from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3
from getSNMP import consultaSNMP

import Agente


def creandoReporteContabilidad(agente: Agente):

    try:
        c = canvas.Canvas("reporteContabilidad"+agente.ip+".pdf", pagesize=A3)
        text = c.beginText(100, 1150)
        text.setFont("Times-Roman", 18)
        text.textLine("Administracion de servicios en Red")
        text.textLine("Practica 1")
        text.textLine("Reporte del algente")

        text.setFont("Times-Roman", 14)
        text.textLine("Zacarias Pineda Esmeralda")
        text.textLine("Grupo: 4CM13")

        text.textLine("version: " + agente.snmpVersion)
        text.textLine("device: " + agente.nombreAgente)
        text.textLine("description" ) #no entiendo que va aqui
        text.textLine("date: " + agente.horario)


        text.textLine("rdate" + agente.horario)
        text.textLine("#NAS-IP-Adress")
        text.textLine("4: " + agente.ip)
        text.textLine("#NAS-Port")
        text.textLine("5: " + agente.puerto)
        text.textLine("#NAS-Port-Type") #No se de donde sale
        text.textLine("61: 2")
        text.textLine("#User-Name")
        text.textLine("1:" + agente.contacto)
        text.textLine("#Acct-Status-Type") # no se 
        text.textLine("40: 2")
        text.textLine("#Acct-Delay-Time") # no se
        text.textLine("41: 14")
        in_octed = consultaSNMP(agente.comunidad, agente.ip, '1.3.6.1.2.1.2.2.1.10.1')
        text.textLine("#Acct-Input-Octets") #
        text.textLine("42: " + in_octed)
        out_octed = consultaSNMP(agente.comunidad, agente.ip, '1.3.6.1.2.1.2.2.1.16.1')
        text.textLine("#Acct-Output-Octets")
        text.textLine("43: " + out_octed)
        text.textLine("#Acct-Session-Id")
        text.textLine("44: 185")
        text.textLine("#Acct-Authentic")
        text.textLine("45: 1")
        text.textLine("#Acct-Session-Time")
        text.textLine("46: 1238")
        in_packet = consultaSNMP(agente.comunidad, agente.ip, '1.3.6.1.2.1.4.3.0')
        text.textLine("#Acct-Input-Packets")
        text.textLine("47: " + in_packet)
        out_packet = consultaSNMP(agente.comunidad, agente.ip, '1.3.6.1.2.1.4.10.0')
        text.textLine("#Acct-Output-Packets")
        text.textLine("48 :" + out_packet)
        text.textLine("#Acct-Terminate-Cause")
        text.textLine("49: 11")
        text.textLine("#Acct-Multi-Session-Id")
        text.textLine("50: 73")
        text.textLine("#Acct-Link-Coun")
        text.textLine("51: 2")
        

        tamx = 250
        tamy = 100
        b = 100
        c.drawImage(agente.ip+"0.png", 20, 400-b, width=tamx, height=tamy)
        c.drawImage(agente.ip+"1.png", 300, 400-b, width=tamx, height=tamy)
        c.drawImage(agente.ip+"2.png", 20, 270-b, width=tamx, height=tamy)
        c.drawImage(agente.ip+"3.png", 300, 270-b, width=tamx, height=tamy)
        c.drawImage(agente.ip+"4.png", 20, 140-b, width=tamx, height=tamy)
        

        c.drawText(text)
        c.save()
    except Exception as e:
        print('Error al crear el PDF: '+ str(e))



