import pandas as pd
import csv
import xml.etree.ElementTree as ET
from xml.dom import minidom
import pickle

class Batalla:
    def __init__(self,id, nombre,anio, region,localizacion,reyA,reyD,gana):
        self.id = id
        self.nombre = nombre
        self.anio = anio
        self.region = region
        self.localizacion = localizacion
        self.reyA = reyA
        self.reyD = reyD
        self.gana = gana

    def __str__(self):
        return "The " + self.nombre + " took place in " + self.localizacion + " (" + self.region +  ") in the year " + self.anio + " The King(s) " + self.reyA + " fougth against " + self.reyD + " and he/htey " + self.gana


num = -1
while num != 0:  #
    print("Seleccione una opción escribiendo el número")
    print("1: Buscar Batalla por Region")
    print("2: Crear XML de batallas")
    print("3: Crear fichero binario objetos")
    print("4: Eliminar Batalla fich Binario objetos")
    print(("0: Salir"))
    num = int(input())

    if num == 1:
        print("Escriba el nombre de una region")
        region = input()

        try:
            datos = pd.read_csv("battles.csv")
            batallas = datos.loc[(datos['region'] == region)]
            print(batallas[['region', 'location', 'name', 'year', 'attacker_king', 'defender_king', 'attacker_outcome']])
        except IndexError:
            print("No encontrtado")

    if num == 2:
        root = ET.Element('juego_tronos')
        with open('battles.csv') as entrada:
            reader = csv.reader(entrada, delimiter=',')
            finalizado = False
            for row in reader:
                if not finalizado:
                    finalizado = True
                else:
                    id = row[2]
                    batalla = ET.SubElement(root, 'batalla id')
                    batalla.set('id', row[2])
                    nombre = ET.SubElement(batalla, 'nombre')
                    nombre.text = row[0]
                    anio = ET.SubElement(batalla, 'anio')
                    anio.text = row[1]
                    region = ET.SubElement(batalla, 'region')
                    region.text = row[23]
                    localizacion = ET.SubElement(batalla, 'localizacion')
                    localizacion.text = row[22]
                    ataque = ET.SubElement(batalla, 'ataque')
                    ataque.set('tamanio = ', row[17])
                    ataque.set('gana =', row[13])
                    reyA = ET.SubElement(ataque, 'rey')
                    reyA.text = row[3]
                    comandanteA = ET.SubElement(ataque, 'comandante')
                    comandanteA.text = row[19]
                    familia_1 = ET.SubElement(ataque, 'familia')
                    familia_1.text = row[5]
                    if(row[6] != ''):
                        familia_2 = ET.SubElement(ataque, 'familia')
                        familia_2.text = row[6]
                    if (row[7] != ''):
                        familia_3 = ET.SubElement(ataque, 'familia')
                        familia_3.text = row[7]
                    if (row[8] != ''):
                        familia_4 = ET.SubElement(ataque, 'familia')
                        familia_4.text = row[8]
                    defensa = ET.SubElement(batalla, 'defensa')
                    defensa.set('tamanio = ', row[18])
                    defensa.set('gana =', row[13])
                    reyD = ET.SubElement(defensa, 'rey')
                    reyD.text = row[4]
                    comandanteD = ET.SubElement(defensa, 'comandante')
                    comandanteD.text = row[20]
                    familia_5 = ET.SubElement(defensa, 'familia')
                    familia_5.text = row[9]
                    if (row[10] != ''):
                        familia_6 = ET.SubElement(defensa, 'familia')
                        familia_6.text = row[10]
                    if (row[11] != ''):
                        familia_7 = ET.SubElement(defensa, 'familia')
                        familia_7.text = row[11]
                    if (row[12] != ''):
                        familia_8 = ET.SubElement(defensa, 'familia')
                        familia_8.text = row[12]

        xmlstr = minidom.String(ET.tostring(root)).toprettyxml(indent="   ")
        with open("battles.xml", "w") as f:
            f.write(xmlstr)


    if num == 3:
        parse = ET.parse('battles.xml')
        root  = parse.getroot()
        with open('battles.pickle', 'wb') as f:
            for padre in root:
                battlesList = []
                battlesList.append(padre.attrib['id'])
                for hijo in padre:
                    battlesList.append(hijo.text)
                battle = Batalla(battlesList[0], battlesList[1], battlesList[2], battlesList[3], battlesList[4], battlesList[5], battlesList[6], battlesList[7])
                pickle.dump(battle, f)

    if num == 4:
        print("Introduzca el id de la batalla")
        id = input()
        eliminada = False
        with open('battles.pickle', 'rb') as f:
            try:
                batalla = pickle.load(f)
                if (batalla.id == id):
                    print(batalla.__str__())
            except:
                print("No encontrada")



