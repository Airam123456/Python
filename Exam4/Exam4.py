from pyexistdb import db, patch

patch.request_patching(patch.XMLRpcLibPatch)

# Coneccion con la base de datos
db = db.ExistDB("http://admin:dm2@localhost:8080/exist/")


def creaBase():

    # Comprobamos si la base existe y si no la creamos
    if db.hasCollection("ColeccionVentas"):
        print("Ya existe")
    else:
        db.createCollection("ColeccionVentas")

    # Subimos los datos de los xml
    fic = open("clientes.xml")
    xml = fic.read()
    db.load(xml, "ColeccionVentas/clientes.xml")

    fic = open("detallefacturas.xml")
    xml = fic.read()
    db.load(xml, "ColeccionVentas/detallefacturas.xml")

    fic = open("facturas.xml")
    xml = fic.read()
    db.load(xml, "ColeccionVentas/facturas.xml")

    fic = open("productos.xml")
    xml = fic.read()
    db.load(xml, "ColeccionVentas/productos.xml")

def insertarFacturas():

    numFactura = input("Numero de factura")
    fecha = input("Fecha")
    importe = input("importe")
    numCliente = input("Numero cliente")

    existeCli = "for $existeCliente in /clientes/clien return $existeCliente[@numero="+numCliente+"]"
    cli = db.executeQuery(existeCli)

    update1 = "update insert <factura numero=" + numFactura + "> <fecha> " + fecha + " </fecha> <importe>" + importe + "</importe> " \
    "<numcliente> " + numCliente + "</numcliente> </factura> into /facturas"

    if db.getHits(cli) == 0:
        print("No existe el cliente")
    else:
        db.executeQuery(update1)


    codigo = input("introduce codigo de la factura. Introduce 0 para continuar")

    existeCod ="for $existeProducto in /productos/product return $existeProducto[codigo="+codigo+"]"
    cod= db.executeQuery(existeCod)
    if db.getHits(cod) == 0:
        print("No existe el producto")
    else:
        print("No me ha dado tiempo a seguir")





def verFactura():

    query = """
    for $facturaCliente in /facturas/factura
    let $numCli := data($facturaCliente/numcliente)
    let $numFac := data($facturaCliente/@numero)
    let $nomCli := /clientes/clien[@numero=$numCli]/nombre/text()

    return
        <facturasclientes>
            <nombre>{$nomCli}</nombre>
            <nufact>{$numFac}</nufact>
        </facturasclientes>
    """
    xml = "<definitivo>"
    res = db.executeQuery(query)
    for i in range(db.getHits(res)):
        xml += db.retrieve_text(res, i) + "\n"
    xml += "<definitivo>"
    print(xml)


# creaBase()
insertarFacturas()
# verFactura()