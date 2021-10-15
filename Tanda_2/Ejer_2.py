import  csv
import pandas as pd

class GestorCSV:

    num = 0
    while num != 5:
        print("Seleccione una opción escribiendo el número")
        print("1: Generar fichero csv de olimpiadas")
        print("2: Buscar deportista")
        print("3: Buscar deportistas por deporte y olimpiada")
        print("4: Añadir deportista")
        print("5: Salir del programa")
        num = int(input())

        if num == 1:
            datos = pd.read_csv("athlete_events.csv")
            olimpiadas = datos[['Games', 'Year', 'Season', 'City']].drop_duplicates()
            olimpiadas.to_csv('olimpiadas.csv', index = False)
            print("Archivo creado")

        if num == 2:
            print("Introduzca el nombre a buscar: ")
            nombre = input()
            datos = pd.read_csv("athlete_events.csv")
            print(datos.loc[datos['Name'] == nombre])

        if num == 3:
            try:
                print("Introduzca el deporte a buscar:")
                deporte = input()
                print("Introduzca el año:")
                anio = int(input())
                print("Introduzca temporada Summer/Winter:")
                temporada = input()

                datos = pd.read_csv("athlete_events.csv")

                olimpiadas = datos.loc[(datos['Sport'] == deporte) & (datos['Year'] == anio) & (datos['Season'] == temporada)]
                print(olimpiadas[['Games', 'City', 'Sport']].iloc[0])
                print(olimpiadas[['Name', 'Event', 'Medal']])
            except IndexError:
                print("No encontrtado")

        if num == 4:








