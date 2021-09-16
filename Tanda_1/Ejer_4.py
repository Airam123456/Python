lista = []
sumatorio = 0
cont = 0

while cont < 5:
    num = int(input("introduce un numero:"))
    if num % 2 == 0:
        print("Introducir numeros impares")
    else:
        lista.append(num)
        sumatorio = sumatorio + num
        cont = cont + 1

print("¿Que desea hacer con la lista? \n \t "
      "1.Sumatorio \n \t 2.Media \n \t 3.Maximo \n \t 4.Minimo \n \t 0.Salir")

resp = int(input())
if resp == 1:
    print(sumatorio)
elif resp == 2:
    print(sumatorio / cont)
elif resp == 3:
    print(max(lista))
elif resp == 4:
    print(min(lista))
else:
    print("Gracias")

