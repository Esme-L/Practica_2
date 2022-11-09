import getSNMP as snmp
import getSNMP2 as snmp2
from Reporte import creandoReporte
from hilo import hiloUpdate
import threading 
from time import sleep
from time import time
import rrdtool 
from ReporteContabilidad import creandoReporteContabilidad


class Agente():
    comunidad = ''
    ip = ''
    nombreAgente = ''
    sistemaOperativo = ''
    versionSO = ''
    contacto = ''
    ubicacion = ''
    numeroInterfaces = ''
    interfaces = {}
    estado = ''
    snmpVersion = ''
    puerto = ''
    enlace = False
    time = ''
    actualizar = 0
    horario = ''

    def __init__(self):
        self.comunidad = ''
        self.ip = ''
        self.nombreAgente = ''
        self.sistemaOperativo = ''
        self.versionSO = ''
        self.contacto = ''
        self.ubicacion = ''
        self.numeroInterfaces = ''
        self.interfaces = {}
        self.estado = ''
        self.snmpVersion = ''
        self.puerto = ''
        self.enlace = False
        self.time = ''
        self.actualizar = 1
        self.horario = ''
    

    def obtenerSO(self):
        aux = snmp.consultaSNMP(self.comunidad, self.ip, '1.3.6.1.2.1.1.1.0')
        if aux.find("#") > 0:
            if (aux.find("Ubuntu") > 0):  # En caso de ser Ubuntu
                soaux = aux.split()[5]
                ''.join(soaux)
                self.sistemaOperativo = soaux[soaux.find('-') + 1:]
        else:
            self.sistemaOperativo = aux.split()[14]
            self.versionSO = aux.split()[16]

    def obtenerUbicacion(self):
        aux = snmp.consultaSNMP(self.comunidad, self.ip, '1.3.6.1.2.1.1.6.0')
        aux = aux.split('=')
        self.ubicacion = aux[-1]

    def obtenerNombre(self):
        aux = snmp.consultaSNMP(self.comunidad, self.ip, '1.3.6.1.2.1.1.5.0')
        aux = aux.split('=')
        self.nombreAgente = aux[-1]


    def obtenerContacto(self):
        aux = snmp.consultaSNMP(self.comunidad, self.ip, '1.3.6.1.2.1.1.4.0')
        aux = aux.split('=')
        self.contacto = aux[-1]

    def obtenerInterfaces(self):
        aux = snmp.consultaSNMP(self.comunidad, self.ip, '1.3.6.1.2.1.2.1.0')
        aux = aux.split('=')
        self.numeroInterfaces = aux[-1]
        i = 1
        while (i <= int(self.numeroInterfaces)):
            aux = snmp.consultaSNMP(self.comunidad, self.ip, '1.3.6.1.2.1.2.2.1.8.' + str(i))
            aux = aux.split('=')
            self.interfaces[i] = aux[-1]
            i += 1

    def obtenerHorario(self):
        aux = snmp2.consultaSNMP2(self.comunidad, self.ip, '1.3.6.1.2.1.1.1.0')
        self.horario = aux

    def actualizarHilo(self):
        hilo1 = threading.Thread(args = (self,), target = hiloUpdate)
        hilo1.start()

    """ 
    def inOctects(self):
        aux = consultaSNMP(self.comunidad, self.ip, '1.3.6.1.2.1.2.2.1.11.1')
        octetosin = aux.split(":")[-1]
    """    
    """
    def obtenerEstados(self):
        self.numeroInterfaces = snmp.consultaSNMP(self.comunidad, self.ip, '1.3.6.1.2.1.2.1.0')
        intEst = []
        for i in range(1, int(self.numeroInterfaces).split('=')):
            aux = snmp.consultaSNMP(self.comunidad, self.ip, '1.3.6.1.2.1.2.2.1.8.' + str(i))
            intEst[i] = aux.split()[4]
            self.estado = intEst[i]
    """
    def crearReporte(self):
        self.obtenerSO()
        self.obtenerContacto()
        self.obtenerUbicacion()
        self.obtenerInterfaces()
        self.obtenerNombre()
        creandoReporte(self)

    def createRRD(self):
        try:
            rrdtool.create(self.ip + '.rrd',
                "--start",'N',
                "--step",'30',
                "DS:unicast:COUNTER:200:U:U",
                "DS:ip:COUNTER:201:U:U",
                "DS:icmp:COUNTER:202:U:U",
                "DS:segmentos:COUNTER:203:U:U",
                "DS:udp:COUNTER:204:U:U",
                "RRA:AVERAGE:0.5:5:300",
                "RRA:AVERAGE:0.5:5:300",
                "RRA:AVERAGE:0.5:5:300",
                "RRA:AVERAGE:0.5:5:300",
                "RRA:AVERAGE:0.5:5:300"
            )
        except Exception as e:
            print("Error al crear el RRD", e)

    def graphRRD(self, tini : int, tfin :  int):
        try :
            i = 0
            for j in ['unicast', 'ip', 'icmp', 'segmentos', 'udp']:
                rrdtool.graph(self.ip + str(i) + ".png",
                             "--start",str(tini),
                             "--end",str(tfin),
                             "--vertical-label="+j,
                            "DEF:"+j+"="+self.ip+".rrd:"+j+":AVERAGE",
                            "AREA:"+j+"#557996:Tramas "+j)                
                i += 1
        except Exception as e :
            print("Error al graficar", e)

    def crearReporteContabilidad(self, tinicio : int, tfinal : int ):
        self.obtenerNombre()
        self.obtenerHorario()
        self.obtenerContacto()
        #inOctects(self
        self.graphRRD(tinicio, tfinal)
        creandoReporteContabilidad(self)

