import xml.etree.ElementTree as ET
import pickle

class Olimpiada:
    def __init__(self, anio, juegos, temporada, ciudad):
        self.anio = anio
        self.juegos = juegos
        self.temporada = temporada
        self.ciudad = ciudad

    def __str__(self):
        return "Año: " + self.anio + "\n Juegos: " + self.juegos + "\n Temporada: " + self.temporada + "\n Ciudad: " + self.ciudad

num = 0
while num != 5:
    print("Seleccione una opción escribiendo el número")
    print("1: Crear fichero serializable de olimpiadas")
    print("2: Añadir edición olímpica")
    print("3: Buscar olimpiadas por sede")
    print("4: Eliminar edición olímpica")
    print("5: Salir del programa")
    num = int(input())

    if num == 1: #Aqui nuevamente necesite ayuda de Raul y Ander porque no conseguia serializar de tal manera que los datos
                # fuesen correctos, ellos me dijeron que debia meter un for dentro de otro con el objetivo de sacar a los hijos.
        parse = ET.parse('olimpiadas.xml')
        root = parse.getroot()
        with open('olimpiadas.pickle', 'wb') as f:
            for padre in root:
                olimpicList = []
                olimpicList.append(padre.attrib['year'])
                for hijo in padre:
                    olimpicList.append(hijo.text)
                olimpiada = Olimpiada(olimpicList[0], olimpicList[1], olimpicList[2], olimpicList[3])
                pickle.dump(olimpiada, f)

    if num == 2:
        print("Introduzca datos sobre la olimpiada ")
        anio = input("Año de celebración: ")
        juegos = input("Juegos: ")
        temporada = input("Temporada: ")
        ciudad = input("Ciudad: ")
        olimpiada = Olimpiada(anio, juegos, temporada, ciudad)
        with open('olimpiadas.pickle', 'ab') as f:
            pickle.dump(olimpiada, f)

    if num == 3:
        ciudad = input("Ciudad que desea buscar: ")
        with open('olimpiadas.pickle', 'rb') as f:
            while True:
                try:
                    olimpiada = pickle.load(f)
                    if (olimpiada.ciudad == ciudad):
                        print(olimpiada.__str__())
                except EOFError:
                    break

    if num == 4:
        print("Introduzca datos de la edición olímpica a eliminar")
        anio = input("Año de celebración: ")
        temporada = input("Temporada: ")
        olimpicList = []
        eliminada = False
        with open('olimpiadas.pickle', 'rb') as f:
            try:
                olimpiada = pickle.load(f)
                if olimpiada.year != anio and olimpiada.ciudad != ciudad:
                    olimpicList.append(olimpiada)
                else:
                    eliminada = True
            except EOFError:
                break

            with open('data/objetosOlimpiada.pickle', 'wb') as writeHandler:
                for olimpiada in olimpicList:
                    pickle.dump(olimpiada, f)

        if eliminada:
            print("Eliminacion correcta")
        else:
            print("No se ha encontrado una olimpiada con esos datos")

