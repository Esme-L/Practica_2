import Agente 
from getSNMP import consultaSNMP
import time
import rrdtool 

OID = {
	#Paquetes unicast que ha recibido una interfaz de red de un agente
	"paquestes_unicast" : '1.3.6.1.2.1.2.2.1.11.1',
	#Paquetes recibidos a protocolos IP, incluyendo los que tienen errores
	"paquetes_recibidos" : '1.3.6.1.2.1.4.3.0',
	#Mensajes ICMP echo que ha enviado el agente
	"mensajes_icmp" : '1.3.6.1.2.1.5.21.0',
	#Segmentos recibidos, incluyendo los que se han recibido con errores 
	"segmentos_recibidos" : '1.3.6.1.2.1.6.10.0',
	#Datagramas entregados a usuarios UDP
	"datagramas_entregados" : '1.3.6.1.2.1.7.1.0'
	}

def hiloUpdate (agente : Agente):
	global OID
	try:
		while agente.enlace:
			unicast = int(consultaSNMP(agente.comunidad, agente.ip, OID["paquestes_unicast"]))
			ip = int(consultaSNMP(agente.comunidad, agente.ip, OID["paquetes_recibidos"]))
			icmp = int(consultaSNMP(agente.comunidad, agente.ip, OID["mensajes_icmp"]))
			segmentos = int(consultaSNMP(agente.comunidad, agente.ip, OID["segmentos_recibidos"]))
			udp = int(consultaSNMP(agente.comunidad, agente.ip, OID["datagramas_entregados"]))

			valor = "N:" + str(unicast) + ':' + str(ip) + ':' + str(icmp) + ':' + str(segmentos) + ':' + str(udp)
			rrdtool.update(agente.ip + ".rrd", valor)
			#print(valor)
			rrdtool.dump(agente.ip + ".rrd", agente.ip +".xml")

			time.sleep(agente.actualizar) 

	except Exception as e:
		print("El hilo no esta vivo")
		print(str(e))

