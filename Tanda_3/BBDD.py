import mysql.connector
import csv
import os
import time


def borrarBBDD(conectordb, cursor):
    # queryParticipacion = "DROP TABLE IF EXISTS Participacion"
    # queryEvento = "DROP TABLE IF EXISTS Evento"
    # queryOlimpiada = "DROP TABLE IF EXISTS Olimpiada"
    # queryDeporte = "DROP TABLE IF EXISTS Deporte"
    # queryDeportista = "DROP TABLE IF EXISTS Deportista"
    # queryEquipo = "DROP TABLE IF EXISTS Equipo"

    queryParticipacion = "delete from Participacion"
    queryEvento = "delete from Evento"
    queryOlimpiada = "delete from Olimpiada"
    queryDeporte = "delete from Deporte"
    queryDeportista = "delete from Deportista"
    queryEquipo = "delete from Equipo"

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

    archivo = input("Introducir la direccion del archivo \n")

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

        print("diccionarios cargados")

    try:
        conectordb = mysql.connector.connect(
            host="127.0.0.1",
            user="admin",
            password="password",
            database="olimpiadas",
            autocommit=True
        )
        cursor = conectordb.cursor()
        print("Coneccion exitosa")
    except:
        print("Fallo en la coneccion")

    try:
        borrarBBDD(conectordb, cursor)
        print("Base de datos vaciada correctamente.")
        # try:
        #     crearTablas(conectordb, cursor)
        #     print("Estructura de la base de datos creada correctamente.")
        # except:
        #     print("No se ha podido crear la estructura de la base de datos.")
    except:
        print("No se ha podido borrar la base de datos.")



    try:
        queryInsertOlimpiada = "Insert into Olimpiada (id_olimpiada,nombre,anio,temporada,ciudad) values (%s, %s, %s, %s, %s)"
        list_olimpiadas = dicOlimpiadas.values()
        cursor.executemany(queryInsertOlimpiada, list_olimpiadas)

        print("olimpiadas cargadas")

        queryInsertEquipo = "Insert into Equipo (id_equipo, nombre, iniciales) values (%s, %s, %s)"
        list_equipos = dicEquipo.values()
        cursor.executemany(queryInsertEquipo, list_equipos)

        print("equipos cargados")

        queryInsertDeportista = "Insert into Deportista (id_deportista, nombre, sexo, peso, altura) values (%s, %s, %s, %s, %s)"
        cursor.executemany(queryInsertDeportista, list(dicDeportistas.values()))

        print("deportistas cargados")

        queryInsertDeporte = "Insert into Deporte (id_deporte, nombre) values (%s,%s)"
        cursor.executemany(queryInsertDeporte, list(dicDeportes.values()))

        print("deportes cargados")

        queryInsertEvento = "insert into Evento (id_evento, nombre, id_olimpiada, id_deporte) values (%s,%s,%s,%s)"
        cursor.executemany(queryInsertEvento, list(dicEventos.values()))
        print("eventos cargados")

        queryInsertParticipacion = "insert into Participacion (id_deportista, id_evento, id_equipo, edad, medalla) values (%s,%s,%s,%s,%s)"
        cursor.executemany(queryInsertParticipacion, list(dicParticipacion.values()))
        print("Participaciones cargadas")
    except:
        print("Fallo en los inserts")

tic = time.perf_counter()
print("La carga de la información se ha realizado correctamente")
crearBBDD()
toc = time.perf_counter()
print(f"Build finished in {(toc - tic) / 60:0.0f} minutes {(toc - tic) % 60:0.0f} seconds")


