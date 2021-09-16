import random


class Persona:
    SEXO = "H"

    def __init__(self, nombre="", edad=0, sexo=SEXO, peso=0, altura=0):
        self.__nombre = nombre
        self.__edad = edad
        self.__dni = self.generaDNI()
        self.__sexo = sexo
        self.__peso = peso
        self.__altura = altura

    def calcularIMC(self):
        IMC = self.__peso / (self.__altura ** 2)

        if IMC < 20:
            return -1
        elif 20 <= IMC <= 25:
            return 0
        else:
            return 1
    def pesoIdeal(self):
        valor = self.calcularIMC()
        if valor == -1:
            print("Peso inferior a los recomendado")
        elif valor == 0:
            print("Peso ideal")
        else:
            print("Sobrepeso")

    def esMayorDeEdad(self):
        if self.__edad < 18:
            return False
        else:
            return True

    def to_String(self):
        return self.__dni, self.__nombre, self.__edad, self.__sexo, self.__peso, self.__altura

    def generaDNI(self):
        dni = random.randint(00000000, 99999999)
        letra ="TRWAGMYFPDXBNJZSQVHLCKE"
        dni = str(dni) + letra[dni%23]
        return dni

    def setNombre(self, nuevoNombre):
        self.__nombre = nuevoNombre

    def setEdad(self, nuevaEdad):
        self.__edad = nuevaEdad

    def setSexo(self, nuevoSexo):
        self.__sexo = nuevoSexo

    def setPeso(self, nuevoPeso):
        self.__peso = nuevoPeso

    def setAltura(self, nuevaAltura):
        self.__altura = nuevaAltura


persona1 = Persona("Airam",29,"H",90,1.90)
persona2 = Persona("Ander",20,"H",54,1.60)
persona3 = Persona("Elena",19,"M",52,1.70)

persona1.pesoIdeal()
persona2.pesoIdeal()
persona3.pesoIdeal()

print(persona1.esMayorDeEdad())
print(persona2.esMayorDeEdad())
print(persona3.esMayorDeEdad())

print(persona1.to_String())
print(persona2.to_String())
print(persona3.to_String())
CAmbbios
