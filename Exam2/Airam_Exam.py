import mysql.connector
import csv
import os
import time

def pregunta1():

    try:
        conectordb = mysql.connector.connect(
            host="172.20.132.100",
            user="ex2",
            password="adat",
            database="examen2")

        cursor = conectordb.cursor()

        print("conexion exitosa")
    except:
        print("fallo")

    query = "select  alumnos.APENOM, notas.NOTA, asignaturas.ABREVIATURA from alumnos, notas, asignaturas where alumnos.DNI = notas.DNI and notas.COD = asignaturas.COD order by alumnos.APENOM desc"
    cursor.execute(query)

    for row in cursor:
        print(str(row[0]))
        print("---------------------------")
        print(str(row[2]) + "\t" + str(row[1])+"\n")

    cursor.close()
    conectordb.close()


def predunta2():
    #Coneccion
    try:
        conectordb = mysql.connector.connect(
            host="172.20.132.100",
            user="ex2",
            password="adat",
            database="examen2")

        cursor = conectordb.cursor()

        print("conexion exitosa")
    except:
        print("fallo")

     #pedimos el dni
    dni = (input("Escribe el DNI del alumno que deseas modificar\n"))
    query = "select APENOM from alumnos where DNI = " + dni + ";"
    cursor.execute(query)

    for row in cursor:
        print(str(row[0]))

    #pedimos nombre
    nuevoNombre = input("Escribe el nuevo nombre para el alumno\n")
    if (nuevoNombre == ""):
        print("Nombre no cambiado")
    else:
        #hacemos el update de datos
        query = "update alumnos set APENOM = '" + nuevoNombre + "' where DNI =" + dni + ";"
        cursor.execute(query)

    #visualizamos el nuevo nombre
    query = "select APENOM from alumnos where DNI = " + dni + ";"
    cursor.execute(query)

    for row in cursor:
        print(str(row[0]))

    conectordb.commit()
    cursor.close()
    conectordb.close()

def pregunta3():

    try:
        conectordb = mysql.connector.connect(
            host="172.20.132.100",
            user="ex2",
            password="adat",
            database="examen2")

        cursor = conectordb.cursor()

        print("conexion exitosa")
    except:
        print("fallo")

    #pedimos dni
    dni = (input("Escribe el DNI del alumno que deseas calificar\n"))
    query = "select APENOM from alumnos where DNI = " + dni + ";"
    cursor.execute(query)

    for row in cursor:
        print(str(row[0]))

    #listamos asignaturas
    print("Listado de asignaturas disponibles: ")
    query = "select NOMBRE, ABREVIATURA, COD from asignaturas"
    cursor.execute(query)

    asignaturas = {}
    contAsig = 1
    for row in cursor:
        asignaturas[contAsig] = (row[0], row[1], row[2])
        print(str(contAsig) + "-. " + str(row[0])+" ("+str(row[1]) + ")")
        contAsig += 1

    #preguntamos que asignatura y que nota queremos cambiar
    codAsig = int(input("Escribe el codigo de la asignatura a evaluar:\n"))
    while(codAsig < 1 or codAsig > contAsig -1):
        codAsig = int(input("Codigo fuera de rango, escriba el correcto\n"))

    nota = int(input("Escribe la nota del alumno\n"))
    while(nota < 0 or nota > 10):
        nota = int(input("La nota es entre 1 y 10\n"))

    asignaturaSelec = asignaturas[codAsig]

    #hacemos el cambio
    query = "update notas set NOTA = '" + str(nota) + "' where DNI = '" + str(dni) + "' and COD = '" + str(asignaturaSelec[2]) + "';"
    cursor.execute(query)

    print("La nota se ha modificado")

    conectordb.commit()
    cursor.close()
    conectordb.close()



pregunta1()












