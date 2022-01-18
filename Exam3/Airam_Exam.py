from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class alumnos(Base):
    __tablename__ = 'alumnos'
    DNI = Column(String, primary_key=True)
    APENOM = Column(String)
    POBLA = Column(String)
    TELEF = Column(String)

class asignaturas(Base):
    __tablename__ = 'asignaturas'
    COD = Column(Integer, primary_key=True)
    NOMBRE = Column(String)
    ABREVIATURA = Column(String)

class notas(Base):
    __tablename__ = 'notas'
    DNI = Column(String, ForeignKey('alumnos.DNI'),primary_key=True)
    COD = Column(Integer,ForeignKey('asignaturas.COD'),primary_key=True)
    NOTA = Column(Integer)
    alumno = relationship("alumnos", back_populates="nota")
    asignatura = relationship("asignaturas", back_populates="nota")


alumnos.nota = relationship("notas", back_populates="alumno")
asignaturas.nota = relationship("notas", back_populates="asignatura")


engine = create_engine('mysql+pymysql://ex2:adat@172.20.132.100/examen2')

def listarAlumnos():

    Session = sessionmaker(bind=engine)
    session = Session()

    listado = session.query(notas).all()



    for todos in listado:
        print(str(todos.alumno.APENOM))
        print("------------")
        if(todos.alumno.DNI == todos.DNI and todos.asignatura.COD == todos.COD):
            print(str(todos.asignatura.ABREVIATURA) + "\t" + str(todos.NOTA))

def modificarNombre():

    Session = sessionmaker(bind=engine)
    session = Session()

    nuevoDNI = input("Escribe el DNI del alumno que deseas modificar\n")
    buscarAlumno = session.query(alumnos).filter(alumnos.DNI.like("%" + nuevoDNI + "%"))

    for alu in buscarAlumno:
        print(alu.APENOM)

    nuevoNombre = input("Escribe el nuevo nombre para el alumno\n")
    if(len(nuevoNombre)>0):
        session.query(alumnos).filter(alumnos.DNI.like("%" + nuevoDNI + "%")).update({alumnos.APENOM: nuevoNombre}, synchronize_session = False)
        session.commit()
        print("Alumno modificado correctamente \nFin del programa")
    else:
        print("Ninguna modificacion\nFin del programa")


def modificarNota():

    Session = sessionmaker(bind=engine)
    session = Session()

    buscarDNI = input("Escribe el DNI del alumno al que quieres calificar\n")

    buscarAlumno = session.query(notas).filter(notas.DNI.like("%" + buscarDNI + "%"))

    asignaturas = {}
    contAsig = 1
    for alu in buscarAlumno:
        asignaturas[contAsig] = alu
        print(alu.alumno.APENOM)
        print(str(alu.COD) + "-. " + str(alu.asignatura.NOMBRE) + "  (" + str(alu.asignatura.ABREVIATURA) + ")")
        contAsig += 1

    codAsig = int(input("Escribe el codigo de la asignatura a evaluar:\n"))
    while (codAsig < 1 or codAsig > contAsig - 1):
        codAsig = int(input("Codigo fuera de rango, escriba el correcto\n"))

    notaN = int(input("Escribe la nota del alumno\n"))
    while (notaN < 0 or notaN > 10):
        notaN = int(input("La nota es entre 1 y 10\n"))

    asignaturaSelec = asignaturas[codAsig]

    print(asignaturaSelec.NOTA)

    session.query(notas).filter(notas.DNI.like("%" + buscarDNI + "%"), notas.COD.like(asignaturaSelec.COD)).update({notas.NOTA: notaN}, synchronize_session = False)
    session.commit()
    print("La nota se ha añadido")











# listarAlumnos()
# modificarNombre()
modificarNota()