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



engine = create_engine('mysql+pymysql://admin:password@localhost/olimpiadas')
# Base.metadata.create_all(engine)
#Session = sessionmaker(bind=engine)
#session = Session()
#result = session.get(Equipo, 2)
#result = session.query(Evento).filter(Evento.id_evento == 25).one()
#print(result.nombre)



def listarDeportistasParticipantes():

    Session = sessionmaker(bind=engine)
    session = Session()

    #Seleccionamos temporada
    temporada = input("Introduce temporada Winter o Summer (W/S)\n")
    while (temporada.upper() != "W" and temporada.upper() != "S"):
        temporada = input("Valor introducido no permitido.\nIntroduce temporada Winter o Summer (W/S)\n")
    if (temporada.upper() == "W"):
        temporada = "Winter"
    else:
        temporada = "Summer"

    #Hacemos la consulata con la que obtendremos toda la info
    cursor = session.query(Olimpiada).filter(Olimpiada.temporada == temporada)

    #Mostramos todas las ediciones del tipo de temporada seleccionada
    ediciones = {}
    contEdicion = 0
    for row in cursor:
        print("\nEscribe " + str(contEdicion) + " para seleccionar:\n\t-Edición Olímpica: " + str(row.nombre))
        ediciones[contEdicion] = row
        contEdicion += 1

    #Elegimos edicion
    numEdicion = int(input("\nNúmero de la edición deseada:"))
    while (numEdicion < 0 or numEdicion > contEdicion - 1):
        numEdicion = int(input("\nNúmero de la edición erroneo, introduzca uno correcto:"))

    edicionSeleccionada = ediciones[numEdicion]
    print("##################################################")

    #Seleccionamos deportes distintos
    deportes_dist = {}
    for evento in edicionSeleccionada.eventos:
        if not evento.deporte.id_deporte in deportes_dist:
            deportes_dist[evento.deporte.id_deporte] = evento.deporte

    deportes = {}
    contDeporte = 0
    for row in deportes_dist.values():
        print("\nEscribe " + str(contDeporte) + " para seleccionar:\n\t-Deporte:" + str(row.nombre))
        deportes[contDeporte] = row
        contDeporte += 1

    numDeporte = int(input("\nNumero del deporte deseado: "))
    while (numDeporte < 0 or numDeporte > contDeporte - 1):
        numDeporte = int(input("\nNúmero del deporte erroneo, introduzca uno correcto:"))

    deporteSelecionado = deportes[numDeporte]
    print("##################################################")

    eventos = {}
    contEvento = 0
    for evento in edicionSeleccionada.eventos:
        if evento.deporte.id_deporte  == deporteSelecionado.id_deporte:
            print("\nEscribe " + str(contEvento) + " para seleccionar:\n\t-Evento:" + str(evento.nombre))
            eventos[contEvento] = evento
            contEvento += 1

    numEvento = int(input("\nNumero del evento deseado:"))
    while (numEvento < 0 or numEvento > contEvento - 1):
        numEvento = int(input("\nNúmero del evento erroneo, introduzca uno correcto:"))

    eventoSeleccionado = eventos[numEvento]

    for participacion in eventoSeleccionado.participaciones:
        print("Nombre: " + str(participacion.deportista.nombre) + "\n\tAltura: " + str(participacion.deportista.peso) + "cm" +
              "\n\tPeso: " + str(participacion.deportista.altura) + "kg" + "\n\tEdad: " + str(participacion.edad) + "años" +
              "\n\tEquipo: " + str(participacion.equipo.nombre) + "\n\tMedalla: " + str(participacion.medalla) + "\n")

    menu()

def modificarMedalla():

    Session = sessionmaker(bind=engine)
    session = Session()

    nombre = input("Introduce nombre del deportista a buscar:\n")
    buscar_desportista = session.query(Deportista).filter(Deportista.nombre.like("%" + nombre + "%"))

    deportistas = {}
    contDeportista = 0
    for deportista in buscar_desportista:
        deportistas[contDeportista] = deportista
        print("\nEscribe " + str(contDeportista) + " para seleccionar:\n\t" + deportista.nombre )
        contDeportista += 1

    numDeportista = int(input("\nNúmero del deportista deseado/a:"))
    while (numDeportista < 0 or numDeportista > contDeportista - 1):
        numDeportista = int(input("\nNúmero del deportista erroneo, introduzca uno correcto:"))

    deportistaSelecionado = deportistas[numDeportista]
    print("##################################################")

    participacion = session.query(Participacion).filter(Participacion.id_deportista == deportistaSelecionado.id_deportista)

    eventos = {}
    contEvento = 0
    for par in participacion:
        eventos[contEvento] = par.evento
        print("\nEscribe " + str(contEvento) + " para seleccionar:\n\t" + par.evento.nombre)
        contEvento += 1

    numEvento = int(input("\nNúmero del evento deseado:"))
    while (numEvento < 0 or numEvento > contEvento - 1):
        numEvento = int(input("\nNúmero del deportista erroneo, introduzca uno correcto:"))

    eventoSelecionado = eventos[numEvento]
    print("##################################################")

    medalla = input("\nEscribe que tipo de medalla quieres asignarle Bronze, Silver, Gold o NA: \n")

    session.query(Participacion).filter(Participacion.id_deportista == deportistaSelecionado.id_deportista
    and Participacion.id_evento == eventoSelecionado.id_evento).update({Participacion.medalla: medalla}, synchronize_session = False)


    #Esto esta hecho por el Profesor
    # dep = session.query(Participacion).filter(Participacion.id_deportista == deportistaSelecionado.id_deportista
    #                                     and Participacion.id_evento == eventoSelecionado.id_evento).first()
    # print(dep.id_deportista, dep.medalla)
    # dep.medalla = medalla

    session.commit()
    menu()

def aniadirDeporParti():

    Session = sessionmaker(bind=engine)
    session = Session()

    nombre = input("Introduce nombre del deportista a buscar:\n")
    buscar_desportista = session.query(Deportista).filter(Deportista.nombre.like("%" + nombre + "%"))


    deportistas = {}
    contDeportista = 0
    for deportista in buscar_desportista:
        deportistas[contDeportista] = deportista
        print("\nEscribe " + str(contDeportista) + " para seleccionar:\n\t" + deportista.nombre)
        contDeportista += 1

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
        nuevoDeportista = Deportista(nombre=nombre, sexo=sexo, peso=peso, altura=altura)
        session.add(nuevoDeportista)
        session.commit()

        print("Deportista insertado\n")

    else:
        numDeportista = int(input("\nNúmero del deportista deseado/a:"))
        while (numDeportista < 0 or numDeportista > contDeportista - 1):
            numDeportista = int(input("\nNúmero del deportista erroneo, introduzca uno correcto:"))

        # deportistaSelecionado = deportistas[numDeportista]

        idDeportista = deportista.id_deportista

    print("##################################################")

    #Seleccionamos temporada
    temporada = input("Introduce temporada Winter o Summer (W/S)\n")
    while (temporada.upper() != "W" and temporada.upper() != "S"):
        temporada = input("Valor introducido no permitido.\nIntroduce temporada Winter o Summer (W/S)\n")
    if (temporada.upper() == "W"):
        temporada = "Winter"
    else:
        temporada = "Summer"

    #Hacemos la consulata con la que obtendremos toda la info
    cursor = session.query(Olimpiada).filter(Olimpiada.temporada == temporada)

    #Mostramos todas las ediciones del tipo de temporada seleccionada
    ediciones = {}
    contEdicion = 0
    for row in cursor:
        print("\nEscribe " + str(contEdicion) + " para seleccionar:\n\t-Edición Olímpica: " + str(row.nombre))
        ediciones[contEdicion] = row
        contEdicion += 1

    #Elegimos edicion
    numEdicion = int(input("\nNúmero de la edición deseada:"))
    while (numEdicion < 0 or numEdicion > contEdicion - 1):
        numEdicion = int(input("\nNúmero de la edición erroneo, introduzca uno correcto:"))

    edicionSeleccionada = ediciones[numEdicion]
    print("##################################################")

    # Seleccionamos deportes distintos
    deportes_dist = {}
    for evento in edicionSeleccionada.eventos:
        if not evento.deporte.id_deporte in deportes_dist:
            deportes_dist[evento.deporte.id_deporte] = evento.deporte

    deportes = {}
    contDeporte = 0
    for row in deportes_dist.values():
        print("\nEscribe " + str(contDeporte) + " para seleccionar:\n\t-Deporte:" + str(row.nombre))
        deportes[contDeporte] = row
        contDeporte += 1

    numDeporte = int(input("\nNumero del deporte deseado: "))
    while (numDeporte < 0 or numDeporte > contDeporte - 1):
        numDeporte = int(input("\nNúmero del deporte erroneo, introduzca uno correcto:"))

    deporteSelecionado = deportes[numDeporte]

    print("##################################################")

    eventos = {}
    contEvento = 0
    for evento in edicionSeleccionada.eventos:
        if evento.deporte.id_deporte == deporteSelecionado.id_deporte:
            print("\nEscribe " + str(contEvento) + " para seleccionar:\n\t-Evento:" + str(evento.nombre))
            eventos[contEvento] = evento
            contEvento += 1

    numEvento = int(input("\nNumero del evento deseado:"))
    while (numEvento < 0 or numEvento > contEvento - 1):
        numEvento = int(input("\nNúmero del evento erroneo, introduzca uno correcto:"))

    eventoSeleccionado = eventos[numEvento]

    idEvento = evento.id_evento

    print("##################################################")


    result_equipos = session.query(Equipo).all()

    equipos = {}
    contEquipo = 0
    for equipo in result_equipos:
        equipos[contEquipo] = (equipo)
        print("\nEscribe " + str(contEquipo) + " para seleccionar:\n\t" + str(equipo.nombre))
        contEquipo += 1

    numEquipo = int(input("\nNumero del equipo deseado:"))
    while (numEquipo < 0 or numEquipo > contEquipo - 1):
        numEquipo = int(input("\nNúmero del evento erroneo, introduzca uno correcto:"))

    idEquipo = equipo.id_equipo


    nuevaParticipacion = Participacion(id_deportista=idDeportista, id_evento=idEvento, id_equipo=idEquipo, edad=None,
                                       medalla=None)

    session.add(nuevaParticipacion)
    session.commit()
    session.close()

    print("Insercion correcta")
    print("##################################################\n")
    menu()


def eliminarParticipacion():

    Session = sessionmaker(bind=engine)
    session = Session()

    nombre = input("Introduce nombre del deportista a buscar:\n")
    buscar_desportista = session.query(Deportista).filter(Deportista.nombre.like("%" + nombre + "%"))

    deportistas = {}
    contDeportista = 0
    for deportista in buscar_desportista:
        deportistas[contDeportista] = deportista
        print("\nEscribe " + str(contDeportista) + " para seleccionar:\n\t" + deportista.nombre)
        contDeportista += 1

    while contDeportista == 0:
        print("Deportista no encontrado")

        nombre = input("Introduce nombre del deportista a buscar:\n")
        buscar_desportista = session.query(Deportista).filter(Deportista.nombre.like("%" + nombre + "%"))

        deportistas = {}
        contDeportista = 0
        for deportista in buscar_desportista:
            deportistas[contDeportista] = deportista
            print("\nEscribe " + str(contDeportista) + " para seleccionar:\n\t" + deportista.nombre)
            contDeportista += 1




    numDeportista = int(input("\nNúmero del deportista deseado/a:"))
    while (numDeportista < 0 or numDeportista > contDeportista - 1):
        numDeportista = int(input("\nNúmero del deportista erroneo, introduzca uno correcto:"))

    deportistaSelecionado = deportistas[numDeportista]


    print("##################################################")

    participacion = session.query(Participacion).filter(
        Participacion.id_deportista == deportistaSelecionado.id_deportista)

    eventos = {}
    contEvento = 0
    for par in participacion:
        eventos[contEvento] = par.evento
        print("\nEscribe " + str(contEvento) + " para seleccionar:\n\t" + par.evento.nombre)
        contEvento += 1

    numEvento = int(input("\nNúmero del evento deseado:"))
    while (numEvento < 0 or numEvento > contEvento - 1):
        numEvento = int(input("\nNúmero del deportista erroneo, introduzca uno correcto:"))

    eventoSeleccionado = eventos[numEvento]


    print("##################################################")

    session.query(Participacion).filter(Participacion.id_deportista == deportistaSelecionado.id_deportista,
                                        Participacion.id_evento == eventoSeleccionado.id_evento).delete()

    session.commit()

    print("Participacion borrada")

    contador = session.query(Participacion).filter(Participacion.id_deportista == deportistaSelecionado.id_deportista).count()

    if contador == 0:
        session.query(Deportista).filter(Deportista.id_deportista == deportistaSelecionado.id_deportista).delete()
        print("Deportista borrado")
        session.commit()

    session.close()
    menu()

menu()