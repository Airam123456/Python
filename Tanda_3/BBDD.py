import mysql.connector
import csv
import os
import time


def borrarBBDD(conectordb, cursor):
    queryParticipacion = "DROP TABLE IF EXISTS Participacion"
    queryEvento = "DROP TABLE IF EXISTS Evento"
    queryOlimpiada = "DROP TABLE IF EXISTS Olimpiada"
    queryDeporte = "DROP TABLE IF EXISTS Deporte"
    queryDeportista = "DROP TABLE IF EXISTS Deportista"
    queryEquipo = "DROP TABLE IF EXISTS Equipo"

    cursor.execute(queryParticipacion)
    cursor.execute(queryEvento)
    cursor.execute(queryOlimpiada)
    cursor.execute(queryDeporte)
    cursor.execute(queryDeportista)
    cursor.execute(queryEquipo)
    conectordb.commit()

def borrarDatos(conectordb, cursor):
    queryParticipacion = "delete from Participacion"
    queryEvento = "delete from Evento"
    queryOlimpiada = "delete from Olimpiada"
    queryDeporte = "delete from Deporte"
    queryDeportista = "delete from Deportista"
    queryEquipo = "delete from Equipo"

    cursor.execute(queryParticipacion)
    cursor.execute(queryEvento)
    cursor.execute(queryOlimpiada)
    cursor.execute(queryDeporte)
    cursor.execute(queryDeportista)
    cursor.execute(queryEquipo)
    conectordb.commit()

'''
def crearConexion():
    conectordb = mysql.connector.connect(
        host="127.0.0.1",
        user="admin",
        password="password",
        database="olimpiadas")

    cursor = conectordb.cursor()
'''

def crearTablasSQL(conectordb, cursor):
    with open('olimpiadas.sql', 'r') as olimpFiles:
        readTablas = olimpFiles.read().split(';')
        for row in readTablas:
            cursor.execute(row)
    conectordb.commit()

def crearTablasSQLite(conectordb, cursor):
    with open('olimpiadas.db.sql', 'r') as olimpFiles:
        readTablas = olimpFiles.read().split(';')
        for row in readTablas:
            cursor.execute(row)
    conectordb.commit()


dicOlimpiadas = {}
dicEventos = {}
dicParticipacion = {}
dicDeportes = {}
dicDeportistas = {}
dicEquipo = {}


def cargarDatosCSV():

    archivo = input("Introducir la direccion del archivo \n")

    if not os.path.exists(archivo):
        print("La dirección de archivo especificada no existe.")
    else:
        print("Accediendo al archivo csv...")

        with open(archivo) as entrada:
            reader = csv.reader(entrada, delimiter=',')
            entrada.readline()
            idOlimpiada = 1
            idEvento = 1
            idDeporte = 1
            idEquipo = 1

            for row in reader:
                if row[8] not in dicOlimpiadas:
                    idOlimAct = idOlimpiada
                    olimpiada = [idOlimAct, row[8], row[9], row[10], row[11]]
                    dicOlimpiadas[row[8]] = olimpiada
                    idOlimpiada = idOlimpiada + 1
                else:
                    idOlimAct = dicOlimpiadas[row[8]][0]

                if row[0] not in dicDeportistas:
                    deportista = [row[0], row[1], row[2], row[4], row[5]]
                    dicDeportistas[row[0]] = deportista
                    idDeportistaAct = row[0]
                    if row[4] == "NA":
                        dicDeportistas[row[0]][3] = None
                    if row[5] == "NA":
                        dicDeportistas[row[0]][4] = None
                else:
                    idDeportistaAct = dicDeportistas[row[0]][0]

                if row[6] not in dicEquipo:
                    idEquipoAct = idEquipo
                    equipo = [idEquipoAct, row[6], row[7]]
                    dicEquipo[row[6]] = equipo
                    idEquipo += 1
                else:
                    idEquipoAct = dicEquipo[row[6]][0]

                if row[12] not in dicDeportes:
                    idDeporteAct = idDeporte
                    deporte = [idDeporteAct, row[12]]
                    dicDeportes[row[12]] = deporte
                    idDeporte += 1
                else:
                    idDeporteAct = dicDeportes[row[12]][0]

                claveEvento = str(idOlimAct) + "" + row[13]
                if claveEvento not in dicEventos:
                    idEventoAct = idEvento
                    evento = [idEventoAct, row[13], idOlimAct, idDeporteAct]
                    dicEventos[claveEvento] = evento
                    idEvento += 1
                else:
                    idEventoAct = dicEventos[claveEvento][0]

                claveParticipacion = str(idDeportistaAct) + "" + str(idEventoAct) + "" + str(idEquipoAct)
                if claveParticipacion not in dicParticipacion:
                    participacion = [idDeportistaAct, idEventoAct, idEquipoAct, row[3], row[14]]
                    dicParticipacion[claveParticipacion] = participacion
                    if row[3] == "NA":
                        dicParticipacion[claveParticipacion][3] = None

        print("Diccionarios cargados")

def crearBBDD():
    cargarDatosCSV()
    try:
        conectordb = mysql.connector.connect(
            host="127.0.0.1",
            user="admin",
            password="password",
            database="olimpiadas")

        cursor = conectordb.cursor()
        print("Coneccion exitosa")
        try:
            borrarDatos(conectordb, cursor)
            print("Base de datos vaciada correctamente.")
            conectordb.commit()

            try:
                crearTablasSQL(conectordb, cursor)
                print("Estructura de la base de datos creada correctamente.")
                conectordb.commit()
            except:
                print("No se ha podido crear la estructura de la base de datos.")
            try:
                queryInsertOlimpiada = "INSERT INTO olimpiadas.Olimpiada (id_olimpiada, nombre, anio, temporada, ciudad) VALUES (%s, %s, %s, %s, %s)"
                list_olimpiadas = list(dicOlimpiadas.values())
                cursor.executemany(queryInsertOlimpiada, list_olimpiadas)
                print("olimpiadas cargadas")
                conectordb.commit()

                queryInsertEquipo = "Insert into Equipo (id_equipo, nombre, iniciales) values (%s, %s, %s)"
                list_equipos = list(dicEquipo.values())
                cursor.executemany(queryInsertEquipo, list_equipos)
                print("equipos cargados")
                conectordb.commit()


                queryInsertDeportista = "Insert into Deportista (id_deportista, nombre, sexo, peso, altura) values (%s, %s, %s, %s, %s)"
                cursor.executemany(queryInsertDeportista, list(dicDeportistas.values()))
                print("deportistas cargados")
                conectordb.commit()


                queryInsertDeporte = "Insert into Deporte (id_deporte, nombre) values (%s,%s)"
                cursor.executemany(queryInsertDeporte, list(dicDeportes.values()))
                print("deportes cargados")
                conectordb.commit()


                queryInsertEvento = "insert into Evento (id_evento, nombre, id_olimpiada, id_deporte) values (%s,%s,%s,%s)"
                cursor.executemany(queryInsertEvento, list(dicEventos.values()))
                print("eventos cargados")

                queryInsertParticipacion = "insert into Participacion (id_deportista, id_evento, id_equipo, edad, medalla) values (%s,%s,%s,%s,%s)"
                cursor.executemany(queryInsertParticipacion, list(dicParticipacion.values()))
                print("Participaciones cargadas")
                conectordb.commit()
                conectordb.close()

            except:
                print("Fallo en los inserts")
                borrarDatos(conectordb, cursor)
        except:
            print("No se ha podido borrar la base de datos.")
    except:
        print("Fallo en la coneccion")

tic = time.perf_counter()
print("La carga de la información se ha realizado correctamente")
#crearBBDD()
toc = time.perf_counter()
print(f"Build finished in {(toc - tic) / 60:0.0f} minutes {(toc - tic) % 60:0.0f} seconds")


def listarDeportistasParticipantes():
    conectordb = mysql.connector.connect(
        host="127.0.0.1",
        user="admin",
        password="password",
        database="olimpiadas")

    cursor = conectordb.cursor()

    temporada = input("Introduce temporada Winter o Summer (W/S)\n")
    while (temporada.upper() != "W" and temporada.upper() != "S"):
        temporada = input("Valor introducido no permitido.\nIntroduce temporada Winter o Summer (W/S)\n")
    if (temporada.upper() == "W"):
        temporada = "Winter"
    else:
        temporada = "Summer"


    query = "select nombre, id_olimpiada from Olimpiada where Olimpiada.temporada = '" + temporada  +"' order by nombre;"
    cursor.execute(query)

    ediciones = {}
    contEdicion = 0
    for row in cursor:
        print("\nEscribe " + str(contEdicion) + " para seleccionar:\n\t-Edición Olímpica:" + str(row[0]))
        ediciones[contEdicion] = (row[0], row[1])
        contEdicion += 1

    numEdicion = int(input("\nNúmero de la edición deseada:"))
    while (numEdicion < 0 or numEdicion > contEdicion - 1):
        numEdicion = int(input("\nNúmero de la edición erroneo, introduzca uno correcto:"))

    edicionSeleccionada = ediciones[numEdicion]
    print("##################################################")

    query = "select Deporte.nombre, Deporte.id_deporte from Evento, Deporte where Evento.id_deporte = Deporte.id_deporte and '" + str(edicionSeleccionada[1]) + "' = id_olimpiada group by Deporte.id_deporte;"
    cursor.execute(query)

    deportes = {}
    contDeporte = 0
    for row in cursor:
        print("\nEscribe " + str(contDeporte) + " para seleccionar:\n\t-Deporte:" + str(row[0]))
        deportes[contDeporte] = (row[0], row[1])
        contDeporte += 1

    numDeporte = int(input("\nNumero del deporte deseado:"))
    while(numDeporte < 0 or numDeporte > contDeporte -1):
        numDeporte = int(input("\nNúmero del deporte erroneo, introduzca uno correcto:"))

    deporteSelecionado = deportes[numDeporte]
    print("##################################################")

    query = "select nombre, id_evento from Evento where '" + str(deporteSelecionado[1]) + "' = id_deporte and '" + str(edicionSeleccionada[1]) + "' = id_olimpiada;"
    cursor.execute(query)

    id_evento = ""
    for row in cursor:
        id_evento = row[1]
    print("-- Resumen --")
    print("Temporada: " + temporada + "\nEdición Olímpica: " + edicionSeleccionada[0] + "\nDeporte: " + deporteSelecionado[0] + "\nEvento: " + str(row[0]))

    print("Deportistas participantes: \n")
    query = "select Deportista.nombre, altura, peso, edad, Equipo.nombre, medalla from Participacion, Deportista, Equipo where '" + str(id_evento) + "' = id_evento "
    query += "and Participacion.id_deportista = Deportista.id_deportista and Participacion.id_equipo = Equipo.id_equipo order by Deportista.nombre;"

    cursor.execute(query)

    contResultDep = 1
    for row in cursor:
        print(str(contResultDep) + ". " + str(row[0]) + "\n\t-Altura:" + str(row[1]) + "\n\t-Peso:" + str(
            row[2]) + "\n\t-Edad:" + str(row[3]) + "\n\t-Equipo:" + str(row[4]) + "\n\t-Medalla:" + str(row[5]) + "\n")
        contResultDep += 1

    cursor.close()
    conectordb.close()

def modificarMedalla():
    conectordb = mysql.connector.connect(
        host="127.0.0.1",
        user="admin",
        password="password",
        database="olimpiadas")

    cursor = conectordb.cursor()

    deportista = input("Introduce nombre del deportista a buscar:\n")
    query = "select nombre, id_deportista from Deportista"
    cursor.execute(query)

    deportistas = {}
    contDeportista = 0
    for row in cursor:
        #El uso del contains lo vi buscando por internet, y lo uso para buscar buscar el nombre seleccionado
        if(row[0].upper().__contains__(deportista.upper())):
            deportistas[contDeportista] = (row[0], row[1])
            print("\nEscribe " + str(contDeportista) + " para seleccionar: \n\t-Deportista: " + str(row[0]))
            contDeportista += 1

    numDeportista = int(input("\nNúmero del deportista deseado/a:"))
    while (numDeportista < 0 or numDeportista > contDeportista - 1):
        numDeportista = int(input("\nNúmero del deportista erroneo, introduzca uno correcto:"))

    deportistaSelecionado = deportistas[numDeportista]
    print("##################################################")


    query = "select Evento.nombre, Evento.id_evento from Evento, Participacion where Evento.id_evento = Participacion.id_evento and '" + str(deportistaSelecionado[1]) + "' = id_deportista;"
    cursor.execute(query)

    eventos = {}
    contEvento = 0
    for row in cursor:
        eventos[contEvento] = (row[0], row[1])
        print("\nEscribe " + str(contEvento) + " para seleccionar:\n\t-Evento: " + str(row[0]))
        contEvento += 1

    numEvento = int(input("\nNúmero del evento deseado:"))
    while (numEvento < 0 or numEvento > contEvento - 1):
        numEvento = int(input("\nNúmero del deportista erroneo, introduzca uno correcto:"))

    eventoSelecionado = eventos[numEvento]
    print("##################################################")


    medalla = input("\nEscribe que tipo de medalla quieres asignarle Bronze, Silver, Gold o NA: \n")

    query = "update Participacion set medalla = '" + str(medalla) + "' where '" + str(deportistaSelecionado[1]) + "' = id_deportista and '" + str(eventoSelecionado[1]) + "' = id_evento;"
    cursor.execute(query)

    query = "select medalla from Participacion where '" + str(deportistaSelecionado[1]) + "' = id_deportista and '" + str(eventoSelecionado[1]) + "' = id_evento;"
    cursor.execute(query)

    medallas = {}
    contMedallas = 0
    for row in cursor:
        medallas[contMedallas] = (row[0])
        print("\nMedalla asignada : " + str(row[0]))

    conectordb.commit()
    cursor.close()
    conectordb.close()

def aniadirDeporParti():

    conectordb = mysql.connector.connect(
        host="127.0.0.1",
        user="admin",
        password="password",
        database="olimpiadas")

    cursor = conectordb.cursor()

    deportista = input("Introduce nombre del deportista a buscar:\n")
    query = "select nombre, id_deportista from Deportista"
    cursor.execute(query)

    deportistas = {}
    contDeportista = 0
    for row in cursor:
        #El uso del contains lo vi buscando por internet, y lo uso para buscar buscar el nombre seleccionado
        if(row[0].upper().__contains__(deportista.upper())):
            deportistas[contDeportista] = (row[0], row[1])
            print("\nEscribe " + str(contDeportista) + " para seleccionar: \n\t-Deportista: " + str(row[0]))
            contDeportista += 1

    if contDeportista == 0:
        print("Deportista no encontrado. \n Añadiendolo a la base de datos.")

        sexo = input("Introduce sexo del nuevo deportista: ")
        while (sexo.upper() != "M" and sexo.upper() != "F"):
            sexo = input("Sexo no permitido.\nValores aceptados: M, F \n")

        peso = int(input("Introduce peso del nuevo deportista: "))
        while (peso < 0 or peso > 500):
            peso = int(input("\nEl peso no puede ser menor de 0 ni mayor de 500.\nIntroduce peso del nuevo deportista: "))



    temporada = input("Introduce temporada Winter o Summer (W/S)\n")
    while (temporada.upper() != "W" and temporada.upper() != "S"):
        temporada = input("Valor introducido no permitido.\nIntroduce temporada Winter o Summer (W/S)\n")
    if (temporada.upper() == "W"):
        temporada = "Winter"
    else:
        temporada = "Summer"


aniadirDeporParti()
#crearBBDD()
#listarDeportistasParticipantes()
#modificarMedalla()
