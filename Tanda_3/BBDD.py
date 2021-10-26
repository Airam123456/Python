import mysql.connector
import csv
import os


def borrarBBDD(conectordb, cursor):
    queryParticipacion = "DROP TABLE IF EXISTS Participacion"
    queryEvento = "DROP TABLE IF EXISTS Evento"
    queryOlimpiada = "DROP TABLE IF EXISTS Olimpiada"
    queryDeporte = "DROP TABLE IF EXISTS Deporte"
    queryDeportista = "DROP TABLE IF EXISTS Deportista"
    queryEquipo = "DROP TABLE IF EXISTS Equipo"
    try:
        cursor.execute(queryParticipacion)
        cursor.execute(queryEvento)
        cursor.execute(queryOlimpiada)
        cursor.execute(queryDeporte)
        cursor.execute(queryDeportista)
        cursor.execute(queryEquipo)
        conectordb.commit()
    except:
        print("Fallo al borrar las tablas")
    finally:
        print(cursor.rowcount, "record(s) deleted")
        conectordb.close()


def crearTablas(conectordb, cursor):
    with open('olimpiadas.sql', 'r') as olimpFiles:
        readTablas = olimpFiles.read()
        tablas = cursor.execute(readTablas, multi=True)
        for row in tablas:
            if row.with_rows:
                row.fetchall()

    conectordb.commit()

def crearBBDD():
    try:
        conectordb = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="password",
            database="olimpiadas",
            autocommit=False
        )
        cursor = conectordb.cursor()
        print("Coneccion exitosa")
    except:
        print("Fallo en la coneccion")

    try:
        borrarBBDD(conectordb, cursor)
        print("Base de datos vaciada correctamente.")
        try:
            crearTablas(conectordb, cursor)
            print("Estructura de la base de datos creada correctamente.")
        except:
            print("No se ha podido crear la estructura de la base de datos.")
    except:
        print("No se ha podido borrar la base de datos.")

    archivo = input("Introducir la direccion del archivo")

    if not os.path.exists(archivo):
        print("La dirección de archivo especificada no existe.")
    else:
        print("Accediendo al archivo csv...")

        dicOlimpiadas = {}
        dicEventos = {}
        dicParticipacion = {}
        dicDeportes = {}
        dicDeportistas = {}
        dicEquipo = {}

        with open(archivo) as entrada:
            reader = csv.reader(entrada, delimiter=',')
            idOlimpiada = 1
            idEvento = 1
            idParticipacion = 1
            idDeporte = 1
            idDeportista = 1
            idEquipo = 1
            primerRow = 0

            for row in reader:
                if primerRow == 0:
                    primerRow += 1
                else:
                    olimpiada = [row[8], row[9], row[10], row[11]]
                    if olimpiada is not dicOlimpiadas.values():
                        dicOlimpiadas[idOlimpiada] = olimpiada
                        idOlimpiada += 1

                    deporte = [row[12]]
                    if deporte is not dicDeportes.values():
                        dicDeportes[idDeporte] = deporte
                        idDeporte += 1

                    deportista = [row[1], row[2], row[4], row[5]]
                    if deportista is not dicDeportistas.values():
                        dicDeportistas[idDeportista] = deportista
                        idDeportista += 1

                    equipo = [row[6], row[7]]
                    if equipo is not dicEquipo.values():
                        dicEquipo[idEquipo] = equipo
                        idEquipo += 1

                    numOlimpiada = 1
                    for olimpiadaEvento in dicOlimpiadas.values():
                        if olimpiadaEvento == olimpiada:
                            break
                        else:
                            numOlimpiada += 1

                    numDeporte = 1
                    for deporteEvento in dicDeportes.values():
                        if deporteEvento == deporte:
                            break
                        else:
                            numDeporte += 1

                    evento = [row[13], numDeporte, numOlimpiada]
                    if evento is not dicEventos.values():
                        dicEventos[idEvento] = evento
                        idEvento += 1

                    numDeportista = 1
                    for deportistaParticipacion in dicParticipacion.values():
                        if deportistaParticipacion == deportista:
                            break
                        else:
                            numDeportista += 1

                    numEvento = 1
                    for eventoParticipacion in dicEventos.values():
                        if eventoParticipacion == evento:
                            break
                        else:
                            numEvento += 1

                    numEquipo = 1
                    for equipoParticipacion in dicEquipo():
                        if equipoParticipacion == equipo:
                            break
                        else:
                            numEquipo += 1

                    participacion = [numDeportista, numEvento, numEquipo, row[3], row[14]]
                    if participacion is not dicParticipacion.values():
                        dicParticipacion[idParticipacion] = participacion
                        idParticipacion += 1

            listaAux = []
            for datos in dicOlimpiadas:
                listaAux.append(list(dicOlimpiadas.get(datos)))
            query = "insert into Olimpiada (id_olimpiada,nombre,anio,temporada,ciudad) values (%s, %s, %s, %s, %s)"
            cursor.executemany(query, listaAux)


crearBBDD()

