import os
import shutil


class Archivo:

    num = 0
    while num != 6:
        print("Seleccione una opción escribiendo el número")
        print("1: Crear directorio")
        print("2: Listar directorio")
        print("3: Copiar archivo")
        print("4: Mover archivo")
        print("5: Eliminar directorio/archivo")
        print("6: Salir del programa")
        num = int(input())

        if num == 1:
            print("Escriba la ruta donde se creara el directorio")
            ruta = input()
            print("Escriba el nombre del archivo a crear")
            nombre = input()
            directorio = ruta + "/" + nombre

            try:
                os.mkdir(directorio)
            except OSError:
                print("La creación del directorio %s falló" % directorio)
            else:
                print("Se ha creado el directorio: %s " % directorio)

        if num == 2:
            print("Escriba la ruta del directorio que desea listar")
            ruta = input()
            with os.scandir(ruta) as directorios:
                for dir in directorios:
                    print(dir)

        if num == 3:
            print("Escriba la ruta de origen del archivo")
            rutaOrigen = input()
            print("Escriba el nombre del archivo a copiar")
            nombre = input()
            print("Escriba la ruta del directorio destino ")
            rutaDestino = input()

            try:
                shutil.copy(rutaOrigen + "/" + nombre, rutaDestino + "/" + nombre)
            except OSError:
                print("La copia del archivo %s falló" % nombre)
            else:
                print("Se ha copiado el archivo %s correctamente" % nombre)

        if num == 4:
            print("Escriba la ruta de origen del archivo")
            rutaOrigen = input()
            print("Escriba el nombre del archivo a mover")
            nombre = input()
            print("Escriba la ruta del directorio destino ")
            rutaDestino = input()

            try:
                shutil.move(rutaOrigen + "/" + nombre, rutaDestino + "/" + nombre)
            except OSError:
                print("No se pudo mover el archivo %s" % nombre)
            else:
                print("Se ha movido el archivo %s correctamente al directorio %s" % (nombre, rutaDestino))

        if num == 5:
            print("Escriba la ruta del archivo que desea eliminar")
            ruta = input()
            if os.path.exists(ruta):
                try:
                    os.remove(ruta)
                    print("Archivo borrado")
                except OSError as IsADirectoryError:
                    try:
                        os.rmdir(ruta)
                        print("Carpeta borrada")
                    except OSError:
                        print("No se puede borrar carpetas con contenido dentro")

            else:
                print("La ruta no existe")

    print("Que tenga un buen dia")


