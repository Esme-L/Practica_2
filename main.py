import sys

import Agente
from pickle import load, dump
from typing import Generic
from hilo import hiloUpdate

agentes = [ ]


def menu():

    while (True):
        if agentes == []:
            print('No hay agentes en la lista ')
        else:
            #Checar que los agentes funcionen y empezarlos a monitorizar, sí que sí.
            for agente in agentes:
                agente.enlace = True
                agente.actualizarHilo()

        print("\tSistema de Administracion de Red\n"
              "\tPráctica 1 - Adquisición de Informacion\n"
              "\tEsmerada Zacarias Pineda \t4CM13 \t2020630526\n"
              "1) Agregar un agente \n"
              "2) Cambiar informacion de dispositivo\n"
              "3) Eliminar dispositivo\n"
              "4) Mostrar Agentes\n"
              "5) Generar un reporte\n"
              "6) Generar reporte de contabilidad")

        opcion = int(input("> "))

        if opcion == 1:
            agregarAgente()

        elif opcion == 2:
            mostrarAgentes()
            print("Ingrese el numero de agente a modificar")
            aux = input()
            modificarAgente(aux)

        elif opcion == 3:
            mostrarAgentes()
            print("Ingrese el agente a eliminar")
            aux = input()
            eliminarAgente(int(aux))

        elif opcion == 4:
            mostrarAgentes()

        elif opcion == 5:
            mostrarAgentes()
            print("Ingresa el numero del agente a hacer reporte")
            op = input()
            agentes[int(op)].crearReporte()

        elif opcion == 6:
            mostrarAgentes()
            print("Ingresa el numero del agente a hacer reporte")
            aux = input()
            print("Timepo de incio para graficar")
            init = input()
            print("Tiempo final para graficar")
            fin = input()
            agentes[int(aux)].crearReporteContabilidad(int(init), int(fin))

def agregarAgente():
    print("\t\tAgregar un agente")
    agente = Agente.Agente()
    print("Ingrese la comunidad: ")
    agente.comunidad = input()
    print("Ingrese la version SNMP")
    agente.snmpVersion = input()
    print("Ingrese el puerto")
    agente.puerto = input()
    print("Ingrese la IP")
    agente.ip = input()
    agente.createRRD()
    agentes.append(agente)
    guardarArchivo(agentes, 'agentes')

def eliminarAgente(indi : int):
    mostrarAgentes()
    agentes.pop(indi)
    guardarArchivo(agentes, 'agentes')

def mostrarAgentes():
    i = 0
    for a in agentes:
        print(str(i) + " .- " + a.ip)
        i+=1
    print("")

def cargarArchivo(name):
    arch = name+'.plk'
    f = open(arch, 'rb')
    aux = load(f)
    f.close()
    return aux

def guardarArchivo(aux: Generic, name: str):
    arch = name + ".plk"
    f = open(arch, 'wb')
    dump(aux, f, -1)
    f.close()

def modificarAgente(indi: int):
    print("Que aspecto desea modificar: \n"
          "1) Comunidad \n"
          "2) Version SNMP \n"
          "3) Puerto \n"
          "4) IP")
    opcion = int(input())
    ag = Agente.Agente
    ag = agentes[int(indi)]
    if opcion == 1:
        print("Ingrese la nueva comunidad")
        ag.comunidad = input()
    elif opcion == 2:
        print("Ingrese la nueva version SNMP")
        ag.snmpVersion = input()
    elif opcion == 3:
        print("Ingrese el nuevo puerto")
        ag.puerto = input()
    elif opcion == 4:
        print("Ingrese la nueva IP")
        ag.ip = input()

try:
    agentes = cargarArchivo('agentes')
except FileNotFoundError:
    print("ERROR")
#hiloUpdate(agentes[0])
menu()


