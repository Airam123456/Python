
import  csv
import pandas as pd

class GestorCSV:

    num = 0
    while num != 5:
        datos = pd.read_csv("solo50.csv")
        print("Seleccione una opción escribiendo el número")
        print("1: Generar fichero csv de olimpiadas")
        print("2: Buscar deportista")
        print("3: Buscar deportistas por deporte y olimpiada")
        print("4: Añadir deportista")
        print("5: Salir del programa")
        num = int(input())

        if num == 1:
            olimpiadas = datos[['Year', 'Games', 'Season', 'City']].drop_duplicates()
            print(list(olimpiadas))
            olimpiadas.to_csv('Olimpiadas.csv', index = False)

        if num == 2:
            print("Introduzca el nombre a buscar: ")
            nombre = input()
            if [datos.Name == nombre]:
                print(datos[datos.Name == nombre])
            else:
                print("hey")

        if num == 3:
            print("Introduzca el deporte a buscar:")
            deporte = input()
            print("Introduzca el año:")
            anio = input()
            print("Introduzca temporada Summer/Winter:")
            temporada = input()

            if [datos.Sport == deporte] and [datos.Year == anio] and [datos.Season == temporada]:
                print(datos[['Sport', 'Year', 'Season']].drop_duplicates())
                print(datos[['Name', 'Event', 'Medal']])








