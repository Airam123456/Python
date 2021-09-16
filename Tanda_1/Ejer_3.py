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
        cont = cont +1

print(lista)
print(sumatorio)
print(sumatorio / cont)