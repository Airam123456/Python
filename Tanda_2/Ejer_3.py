import pandas as pd
import csv
import xml.sax
import xml.etree.ElementTree as ET
from xml.dom import minidom


class XMLHandler(xml.sax.ContentHandler):

    def __init__(self):
        self.Datos = False

    def startElement(self, name, attrs):
        if attrs.getNames() == ['year']:
            print("Año: " + attrs['year'])
        if name == "juegos":
            self.Datos = True

    def characters(self, cha):
        if self.Datos:
            print("Juegos: " + cha)

    def endElement(self, name):
        if name == "juegos":
            self.Datos = False

num = 0
while num != 4:
    print("Seleccione una opción escribiendo el número")
    print("1: Crear XML de olimpiadas")
    print("2: Crear XML de deportistas")
    print("3: Listado de olimpiadas")
    print("4: Salir del programa")
    num = int(input())

    if num == 1:
        olimpicList = []  # La idea de hacerlo de esta forma con  una lista me la dio Raul porque
                            # yo estaba usando pandas y estaba atascado

        with open('olimpiadas.csv') as entrada:
            reader = csv.reader(entrada, delimiter = ',')
            finalizado = False
            for row in reader:
                if not finalizado:
                    finalizado = True
                else:
                    olimpicList.append([row[2], row[1], row[3], row[4]])

        root = ET.Element('olimpiadas')  # Root del xml
        for row in olimpicList:  # Por cada olimpiada, le pone el atributo y crea los hijos
            olimpiada = ET.SubElement(root, 'olimpiada')
            olimpiada.set('year', row[0])
            juegos = ET.SubElement(olimpiada, 'juegos')
            juegos.text = row[1]
            temporada = ET.SubElement(olimpiada, 'temporada')
            temporada.text = row[2]
            ciudad = ET.SubElement(olimpiada, 'ciduad')
            ciudad.text = row[3]

        xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
        with open("olimpiadas.xml", "w") as f:
            f.write(xmlstr)

    if num == 2:
        root = ET.Element('deportistas')
        with open('athlete_events.csv') as entrada:
            reader = csv.reader(entrada, delimiter = ',')
            finalizado = False
            for row in reader:
                if not finalizado:
                    finalizado = True
                else:
                    id = row[0]
                    deportista = ET.SubElement(root, 'deportista')
                    deportista.set('id', row[0])
                    nombre = ET.SubElement(deportista, 'nombre')
                    nombre.text = row[1]
                    sexo = ET.SubElement(deportista, 'sexo')
                    sexo.text = row[2]
                    altura = ET.SubElement(deportista, 'altura')
                    altura.text = row[4]
                    peso = ET.SubElement(deportista, 'peso')
                    peso.text = row[5]
                    participaciones = ET.SubElement(deportista, 'participaciones')
                    deporte = ET.SubElement(participaciones, 'deporte')
                    deporte.set('nombre', row[12])
                    participacion = ET.SubElement(deporte, 'participacion')
                    participacion.set('edad', row[3])
                    equipo = ET.SubElement(participacion, 'equipo')
                    equipo.text = row[11]
                    juegos = ET.SubElement(participacion, 'juegos')
                    juegos.text = row[8]
                    evento = ET.SubElement(participacion, 'evento')
                    evento.text = row[13]
                    if (row[14] != 'NA'):
                        medalla = ET.SubElement(participacion, 'medalla')
                        medalla.text = row[14]

        xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
        with open("deportistas.xml", "w") as f:
            f.write(xmlstr)

    if num == 3:
        handler = XMLHandler()
        parser = xml.sax.make_parser()
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        parser.setContentHandler(handler)
        parser.parse("olimpiadas.xml")