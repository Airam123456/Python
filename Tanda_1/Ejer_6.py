class Criptografo:

    def encriptar(texto):
        txt = ""
        for letra in texto:
            txt = txt + (chr(ord(letra)+1))
        print(txt)

    def desencriptar(texto):
        txt = ""
        for letra in texto:
            txt = txt + (chr(ord(letra)-1))
        print(txt)

    encriptar("Airam")
    desencriptar("Cocodrilo")