lista = []
suma = 0
cont = 0

while cont < 5:
    num = int(input("introduce un numero:"))
    if num % 2 == 0:
        print("Introducir numeros impares")
    else:
        lista.append(num)
        suma = suma + num
        cont = cont + 1

def sumatorio():
    print(suma)
def media():
    print(suma / cont)
def maximo():
    print(max(lista))
def minimo():
    print(min(lista))


print("¿Que desea hacer con la lista? \n \t "
      "1.Sumatorio \n \t 2.Media \n \t 3.Maximo \n \t 4.Minimo \n \t 0.Salir")

resp = int(input())
if resp == 1:
    sumatorio()
elif resp == 2:
    media()
elif resp == 3:
    maximo()
elif resp == 4:
    minimo()
else:
    print("Gracias")

