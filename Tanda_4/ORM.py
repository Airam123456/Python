import mysql.connector
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Olimpiada(Base):
    __tablename__ = 'Olimpiada'
    id_olimpiada = Column(Integer, primary_key=True)
    nombre = Column(String)
    anio = Column(String)
    temporada = Column(String)
    ciudad = Column(String)


class Deporte(Base):
    __tablename__ = 'Deporte'
    id_deporte = Column(Integer, primary_key=True)
    nombre = Column(String)


class Deportista(Base):
    __tablename__ = 'Deportista'
    id_deportista = Column(Integer, primary_key=True)
    nombre = Column(String)
    sexo = Column(String)
    peso = Column(Integer)
    altura = Column(Integer)


class Equipo(Base):
    __tablename__ = 'Equipo'
    id_equipo = Column(Integer, primary_key=True)
    nombre = Column(String)
    iniciales = Column(String)


class Evento(Base):
    __tablename__ = 'Evento'
    id_evento = Column(Integer, primary_key=True)
    nombre = Column(String)
    id_olimpiada = Column(Integer, ForeignKey('Olimpiada.id_olimpiada'))
    id_deporte = Column(Integer, ForeignKey('Deporte.id_deporte'))
    olimpiada = relationship("Olimpiada", back_populates="eventos")
    deporte = relationship("Deporte", back_populates="eventos")


class Participacion(Base):
    __tablename__ = 'Participacion'
    id_deportista = Column(Integer, ForeignKey('Deportista.id_deportista'), primary_key=True)
    id_evento = Column(Integer, ForeignKey('Evento.id_evento'), primary_key=True)
    id_equipo = Column(Integer, ForeignKey('Equipo.id_equipo'))
    edad = Column(Integer)
    medalla = Column(String)
    deportista = relationship("Deportista", back_populates="participaciones")
    evento = relationship("Evento", back_populates="participaciones")
    equipo = relationship("Equipo", back_populates="participaciones")


Olimpiada.eventos = relationship("Evento", back_populates="olimpiada")
Deporte.eventos = relationship("Evento", back_populates="deporte")

Deportista.participaciones = relationship("Participacion", back_populates="deportista")
Evento.participaciones = relationship("Participacion", back_populates="evento")
Equipo.participaciones = relationship("Participacion", back_populates="equipo")





def menu():
    respuesta = int(input("¿Qué deseas hacer?\n1. Listar deportistas participantes\n2. Modificar medalla"
                          "\n3. Añadir deportista/participación\n4. Eliminar participación\n0. Salir del programa\n"))
    while (respuesta < 0 or respuesta > 4):
        int(input("Respuesta no valida, intentelo de nuevo"))
    if respuesta == 1:
        listarDeportistasParticipantes()
    elif respuesta == 2:
        modificarMedalla()
    elif respuesta == 3:
        aniadirDeporParti()
    elif respuesta == 4:
        eliminarParticipacion()
    else:
        print("Programa Finalizado")



engine = create_engine('mysql+pymysql://admin:password@localhost/olimpiadas', echo=True)
# Base.metadata.create_all(engine)
#Session = sessionmaker(bind=engine)
#session = Session()
#result = session.get(Equipo, 2)
#result = session.query(Evento).filter(Evento.id_evento == 25).one()
#print(result.nombre)



def listarDeportistasParticipantes():

    Session = sessionmaker(bind=engine)
    session = Session()

    temporada = input("Introduce temporada Winter o Summer (W/S)\n")
    while (temporada.upper() != "W" and temporada.upper() != "S"):
        temporada = input("Valor introducido no permitido.\nIntroduce temporada Winter o Summer (W/S)\n")
    if (temporada.upper() == "W"):
        temporada = "Winter"
    else:
        temporada = "Summer"

    cursor = session.query(Olimpiada).filter(Olimpiada.temporada == temporada)

    ediciones = {}
    contEdicion = 0
    for row in cursor:
        print("\nEscribe " + str(contEdicion) + " para seleccionar:\n\t-Edición Olímpica:" + str(row.nombre))
        ediciones[contEdicion] = (row.nombre, row.id_olimpiada)
        contEdicion += 1

    numEdicion = int(input("\nNúmero de la edición deseada:"))
    while (numEdicion < 0 or numEdicion > contEdicion - 1):
        numEdicion = int(input("\nNúmero de la edición erroneo, introduzca uno correcto:"))

    edicionSeleccionada = ediciones[numEdicion]
    print("##################################################")


    query = "select Deporte.nombre, Deporte.id_deporte from Evento, Deporte where Evento.id_deporte = Deporte.id_deporte and '" + str(
        edicionSeleccionada[1]) + "' = id_olimpiada group by Deporte.id_deporte;"
    cursor.execute(query)

    cursor = session.query

    deportes = {}
    contDeporte = 0
    for row in cursor:
        print("\nEscribe " + str(contDeporte) + " para seleccionar:\n\t-Deporte:" + str(row[0]))
        deportes[contDeporte] = (row[0], row[1])
        contDeporte += 1

    numDeporte = int(input("\nNumero del deporte deseado:"))
    while (numDeporte < 0 or numDeporte > contDeporte - 1):
        numDeporte = int(input("\nNúmero del deporte erroneo, introduzca uno correcto:"))

    deporteSelecionado = deportes[numDeporte]
    print("##################################################")
'''
    query = "select nombre, id_evento from Evento where '" + str(deporteSelecionado[1]) + "' = id_deporte and '" + str(
        edicionSeleccionada[1]) + "' = id_olimpiada;"
    cursor.execute(query)

    id_evento = ""
    for row in cursor:
        id_evento = row[1]
    print("-- Resumen --")
    print("Temporada: " + temporada + "\nEdición Olímpica: " + edicionSeleccionada[0] + "\nDeporte: " +
          deporteSelecionado[0] + "\nEvento: " + str(row[0]))

    print("Deportistas participantes: \n")
    query = "select Deportista.nombre, altura, peso, edad, Equipo.nombre, medalla from Participacion, Deportista, Equipo where '" + str(
        id_evento) + "' = id_evento "
    query += "and Participacion.id_deportista = Deportista.id_deportista and Participacion.id_equipo = Equipo.id_equipo order by Deportista.nombre;"

    cursor.execute(query)

    contResultDep = 1
    for row in cursor:
        print(str(contResultDep) + ". " + str(row[0]) + "\n\t-Altura:" + str(row[1]) + "\n\t-Peso:" + str(
            row[2]) + "\n\t-Edad:" + str(row[3]) + "\n\t-Equipo:" + str(row[4]) + "\n\t-Medalla:" + str(row[5]) + "\n")
        contResultDep += 1

    cursor.close()
    conectordb.close()
    menu()

'''
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
        # El uso del contains lo vi buscando por internet, y lo uso para buscar buscar el nombre seleccionado
        if (row[0].upper().__contains__(deportista.upper())):
            deportistas[contDeportista] = (row[0], row[1])
            print("\nEscribe " + str(contDeportista) + " para seleccionar: \n\t-Deportista: " + str(row[0]))
            contDeportista += 1

    numDeportista = int(input("\nNúmero del deportista deseado/a:"))
    while (numDeportista < 0 or numDeportista > contDeportista - 1):
        numDeportista = int(input("\nNúmero del deportista erroneo, introduzca uno correcto:"))

    deportistaSelecionado = deportistas[numDeportista]
    print("##################################################")

    query = "select Evento.nombre, Evento.id_evento from Evento, Participacion where Evento.id_evento = Participacion.id_evento and '" + str(
        deportistaSelecionado[1]) + "' = id_deportista;"
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

    query = "update Participacion set medalla = '" + str(medalla) + "' where '" + str(
        deportistaSelecionado[1]) + "' = id_deportista and '" + str(eventoSelecionado[1]) + "' = id_evento;"
    cursor.execute(query)

    query = "select medalla from Participacion where '" + str(
        deportistaSelecionado[1]) + "' = id_deportista and '" + str(eventoSelecionado[1]) + "' = id_evento;"
    cursor.execute(query)

    medallas = {}
    contMedallas = 0
    for row in cursor:
        medallas[contMedallas] = (row[0])
        print("\nMedalla asignada : " + str(row[0]))

    conectordb.commit()
    cursor.close()
    conectordb.close()
    menu()


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
        # El uso del contains lo vi buscando por internet, y lo uso para buscar buscar el nombre seleccionado
        if (row[0].upper().__contains__(deportista.upper())):
            deportistas[contDeportista] = (row[0], row[1])
            print("\nEscribe " + str(contDeportista) + " para seleccionar: \n\t-Deportista: " + str(row[0]))
            contDeportista += 1

    # ADVERTENCIA!!! A partir de este punto la maquina virtual que usaba para ejecutar la base de datos dejor de funcionar asi que no pude comprobar si lo que hacia era correcto

    if contDeportista == 0:
        # Si el deportista no existe lo creamos
        print("Deportista no encontrado. \n Añadiendolo a la base de datos.")

        sexo = input("Introduce sexo del nuevo deportista: ")
        while (sexo.upper() != "M" and sexo.upper() != "F"):
            sexo = input("\nSexo no permitido.\nValores aceptados: M, F")

        peso = int(input("Introduce peso del nuevo deportista: "))
        while (peso < 0 or peso > 500):
            peso = int(
                input("\nEl peso no puede ser menor de 0 ni mayor de 500.\nIntroduce peso del nuevo deportista: "))

        altura = int(input("Introduce altura del nuevo deportista: "))
        while (altura < 0 or altura > 300):
            altura = int(
                input("\nla altura no puede ser menor de 0 ni mayor de 300.\nIntroduce altura del nuevo deportista: "))

        # creo que aqui no tengo que poner el id del deportista porque eso lo hace el autoincrement
        query = "insert into Deportista (nombre, sexo, peso, altura) values (%s,%s,%s,%s);"
        cursor.execute(query(deportista, sexo, peso, altura))
        conectordb.commit()
        print("Deportista insertado\n")

    else:
        numDeportista = int(input("\nNúmero del deportista deseado/a:"))
        while (numDeportista < 0 or numDeportista > contDeportista - 1):
            numDeportista = int(input("\nNúmero del deportista erroneo, introduzca uno correcto:"))

        deportistaSelecionado = deportistas[numDeportista]

        idDeportista = deportistaSelecionado[1]

    print("##################################################")

    temporada = input("Introduce temporada Winter o Summer (W/S)\n")
    while (temporada.upper() != "W" and temporada.upper() != "S"):
        temporada = input("Valor introducido no permitido.\nIntroduce temporada Winter o Summer (W/S)\n")
    if (temporada.upper() == "W"):
        temporada = "Winter"
    else:
        temporada = "Summer"

    query = "select nombre, id_olimpiada from Olimpiada where Olimpiada.temporada = '" + temporada + "' order by nombre;"
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

    query = "select Deporte.nombre, Deporte.id_deporte from Evento, Deporte where Evento.id_deporte = Deporte.id_deporte and '" + str(
        edicionSeleccionada[1]) + "' = id_olimpiada group by Deporte.id_deporte;"
    cursor.execute(query)

    deportes = {}
    contDeporte = 0
    for row in cursor:
        print("\nEscribe " + str(contDeporte) + " para seleccionar:\n\t-Deporte:" + str(row[0]))
        deportes[contDeporte] = (row[0], row[1])
        contDeporte += 1

    numDeporte = int(input("\nNumero del deporte deseado:"))
    while (numDeporte < 0 or numDeporte > contDeporte - 1):
        numDeporte = int(input("\nNúmero del deporte erroneo, introduzca uno correcto:"))

    deporteSelecionado = deportes[numDeporte]
    print("##################################################")

    query = "select nombre, id_evento from Evento where '" + str(deporteSelecionado[1]) + "' = id_deporte and '" + str(
        edicionSeleccionada[1]) + "' = id_olimpiada;"
    cursor.execute(query)

    eventos = {}
    contEvento = 0
    for row in cursor:
        print("\nEscribe " + str(contEvento) + " para seleccionar:\n\t-Evento: " + str(row[0]))
        eventos[contEvento] = (row[0], row[1])
        contEvento += 1

    numEvento = int(input("\nNumero del evento deseado:"))
    while (numEvento < 0 or numEvento > contEvento - 1):
        numEvento = int(input("\nNúmero del evento erroneo, introduzca uno correcto:"))

    eventoSeleccionado = eventos[numEvento]

    # Aqui dejamos el id del Evento que necesitaremos para la insert
    idEvento = eventoSeleccionado[1]

    medalla = input("Introduce la medalla del deportista, Bronze, Silver, Gold o NA: \n: ")

    edad = int(input("Introduce edad del deportista en la participacion: "))
    while (edad < 0 or edad > 100):
        peso = int(input(
            "\nLa edad no puede ser menor de 0 ni mayor de 100.\nIntroduce edad del deportista en la participacion: "))

    # Informacion del equipo

    query = "select nombre, id_equipo from Equipo;"
    cursor.execute(query)

    equipos = {}
    contEquipo = 0
    for row in cursor:
        print("\nEscribe " + str(contEquipo) + " para seleccionar:\n\t-Evento: " + str(row[0]))
        equipos[contEquipo] = (row[0], row[1])
        contEquipo += 1

    numEquipo = int(input("\nNúmero del equipo deseado: "))
    while (numEquipo < 0 or numEvento > contEquipo - 1):
        numEquipo = int(input("\nNúmero del equipo erroneo, introduzca uno correcto:"))

    equipoSelecionado = equipos[numEquipo]

    idEquipo = equipoSelecionado[1]

    # Insertamos participacion

    query = "insert into Participacion (id_deportista, id_evento, id_equipo, edad, medalla) values (%s,%s,%s,%s,%s);"
    cursor.execute(query(idDeportista, idEvento, idEquipo, edad, medalla))
    conectordb.commit()
    print("Participacion insertada\n")

    cursor.close()
    conectordb.close()
    menu()


def eliminarParticipacion():
    conectordb = mysql.connector.connect(
        host="127.0.0.1",
        user="admin",
        password="password",
        database="olimpiadas")

    cursor = conectordb.cursor()

    deportista = input("Introduce nombre del deportista a buscar:\n")
    query = "select nombre, id_deportista from Deportista"
    cursor.execute(query)

    deportista = input("Introduce nombre del deportista a buscar:\n")
    query = "select nombre, id_deportista from Deportista"
    cursor.execute(query)

    deportistas = {}
    contDeportista = 0
    for row in cursor:
        # El uso del contains lo vi buscando por internet, y lo uso para buscar buscar el nombre seleccionado
        if (row[0].upper().__contains__(deportista.upper())):
            deportistas[contDeportista] = (row[0], row[1])
            print("\nEscribe " + str(contDeportista) + " para seleccionar: \n\t-Deportista: " + str(row[0]))
            contDeportista += 1

    numDeportista = int(input("\nNúmero del deportista deseado/a:"))
    while (numDeportista < 0 or numDeportista > contDeportista - 1):
        numDeportista = int(input("\nNúmero del deportista erroneo, introduzca uno correcto:"))

    deportistaSelecionado = deportistas[numDeportista]

    idDeportista = deportistaSelecionado[1]

    print("##################################################")
    query = "select Evento.nombre, Evento.id_evento from Evento, Participacion where Evento.id_evento = Participacion.id_evento and '" + str(
        idDeportista) + "' = Participacion.id_deportista;"
    cursor.execute(query)

    eventos = {}
    contEvento = 0
    for row in cursor:
        print("\nEscribe " + str(contEvento) + " para seleccionar:\n\t-Evento: " + str(row[0]))
        eventos[contEvento] = (row[0], row[1])
        contEvento += 1

    numEvento = int(input("\nNumero del evento deseado:"))
    while (numEvento < 0 or numEvento > contEvento - 1):
        numEvento = int(input("\nNúmero del evento erroneo, introduzca uno correcto:"))

    eventoSeleccionado = eventos[numEvento]

    # Aqui dejamos el id del Evento que necesitaremos para la insert
    idEvento = eventoSeleccionado[1]

    query = "select Equipo.nombre, Participacion.edad, medalla, id_deportista, id_evento, Participacion.id_equipo from" \
            " Participacion, Equipo where id_evento = '" + idEvento + "' and id_deportista = '" + idDeportista + "' and Participacion.id_equipo = Equipo.id_equipo;"
    cursor.execute(query)

    participaciones = {}
    contParticipacion = 0
    for row in cursor:
        participaciones[contParticipacion] = (row[0], row[1], row[2], row[3], row[4], row[5])
        print("\nEscribe " + str(contParticipacion) + " para seleccionar la participación jugada para el equipo:" + str(
            row[0]) + "\n\t-Ganando la medalla: " + str(row[2]) + "\n\t-Con la edad: " + str(row[1]))
        contParticipacion += 1

    numParticipacion = int(input("\nNúmero de la participacion deseada: "))
    while (numParticipacion < 0 or numParticipacion > contParticipacion - 1):
        numParticipacion = int(input("\nNúmero de participacion erroneo, introduzca uno correcto:"))

    participacionSelecionada = participaciones[numParticipacion]

    idDeportista = participacionSelecionada[3]
    idEvento = participacionSelecionada[4]
    idEquipo = participacionSelecionada[5]

    query = "delete from Participacion where id_deportista = '" + idDeportista + "' and id_evento '" + idEvento + "' and id_equipo '" + idEquipo + "';"
    cursor.execute(query)
    print("Participacion eliminada correctamente")

    if contParticipacion <= 1:
        print("Como esta era la su unica participacion olimpica procederemos a borrarlo de la base")
        query = "delete from Deportista where id_deportista = '" + + idDeportista + "';"
        cursor.execute(query)
        print("Deportista eliminado correctamente")

    conectordb.commit()
    cursor.close()
    conectordb.close()
menu()