import mysql.connector
import csv


def crearBBDD():
    dicOlimpiadas = {}
    dicEventos = {}
    dicParticipacion = {}
    dicDeportes = {}
    dicDeportistas = {}
    dicEquipo = {}

    with open('recortada.csv') as entrada:
        reader = csv.reader(entrada, delimiter=',')
        idOlimpiada = 1
        idEvento = 1
        idParticipacion = 1
        idDeporte = 1
        idDeportista = 1
        idEquipo = 1
        firstRow = 0

        for row in reader:
            if firstRow == 0:
                firstRow += 1
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
                    if(olimpiadaEvento == olimpiada):
                        break
                    else:
                        numOlimpiada += 1

                numDeporte = 1
                for deporteEvento in dicDeportes.values():
                    if(deporteEvento == deporte):
                        break
                    else:
                        numDeporte += 1

                evento = [row[13], numDeporte, numOlimpiada]
                if evento is not dicEventos.values():
                    dicEventos[idEvento] = evento
                    idEvento += 1

                numDeportista = 1
                for deportistaParticipacion in dicParticipacion.values():
                    if(deportistaParticipacion == deportista):
                        break
                    else:
                        numDeportista += 1

                numEvento = 1
                for eventoParticipacion in dicEventos.values():
                    if (eventoParticipacion == evento):
                        break
                    else:
                        numEvento += 1

                numEquipo = 1
                for equipoParticipacion in dicEquipo():
                    if(equipoParticipacion == equipo):
                        break
                    else:
                        numEquipo += 1

                participacion = [numDeportista, numEvento, numEquipo, row[3], row[14]]
                if participacion is not dicParticipacion.values():
                    dicParticipacion[idParticipacion] = participacion
                    idParticipacion += 1

    print(dicDeportes)

crearBBDD()