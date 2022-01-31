from pyexistdb import db, patch

patch.request_patching(patch.XMLRpcLibPatch)

# Coneccion con la base de datos
db = db.ExistDB("http://admin:dm2@localhost:8080/exist/")
# db.ExistDB("http://admin:dm2@localhost:8080/exist/AIRAM")

# Comprobamos si la base existe y si no la creamos
if db.hasCollection("GIMNASIO"):
    print("Ya existe")
else:
    db.createCollection("GIMNASIO")

# Subimos los datos de los xml
fic = open("socios_gim.xml")
xml = fic.read()
db.load(xml, "GIMNASIO/socios_gim.xml")

fic = open("actividades_gim.xml")
xml = fic.read()
db.load(xml, "GIMNASIO/actividades_gim.xml")

fic = open("uso_gimnasio.xml")
xml = fic.read()
db.load(xml, "GIMNASIO/uso_gimnasio.xml")

# Consulta para crear el xml temporal
query ="""
for $uso in /USO_GIMNASIO/fila_uso
let $nomsocio := /SOCIOS_GIM/fila_socios[COD=$uso/CODSOCIO]/NOMBRE/text()
let $nomactiv := /ACTIVIDADES_GIM/fila_actividades[@cod=$uso/CODACTIV]/NOMBRE/text()
let $tipoactiv := data(/ACTIVIDADES_GIM/fila_actividades[@cod=$uso/CODACTIV]/@tipo)
let $horas := $uso/HORAFINAL/text()-$uso/HORAINICIO/text()
return 
    <datos>
        <COD>{$uso/CODSOCIO/text()}</COD>
        <NOMBRESOCIO>{$nomsocio}</NOMBRESOCIO>
        <CODACTIV>{$uso/CODACTIV/text()}</CODACTIV>
        <NOMBREACTIVIDAD>{$nomactiv}</NOMBREACTIVIDAD>
        <horas>{$horas}</horas>
        <tipoact>{$tipoactiv}</tipoact>
        {
            if($tipoactiv = 1) then
                <cuota_adicional>0</cuota_adicional>
            else if ($tipoactiv = 2) then
                <cuota_adicional>{$horas *2}</cuota_adicional>
            else
                <cuota_adicional>{$horas *4}</cuota_adicional>  
        }
    </datos>
"""

# Creamos el xml temporal
xml = "<temp>"
res = db.executeQuery(query)
print(res, db.getHits(res))
for i in range(db.getHits(res)):
    xml += db.retrieve_text(res, i)
xml += "</temp>"
# Subimos el xml temporal
db.load(xml, "GIMNASIO/temp.xml")

# Consulta para crear el xml definitivo
query ="""
for $final in /SOCIOS_GIM/fila_socios
let $adic := sum(/temp/datos[COD=$final/COD]/cuota_adicional)
let $tot := $final/CUOTA_FIJA/text() + $adic
return 
    <datos>
        <COD>{$final/COD/text()}</COD>
        <NOMBRESOCIO>{$final/NOMBRE/text()}</NOMBRESOCIO>
        <CUOTA_FIJA>{$final/CUOTA_FIJA/text()}</CUOTA_FIJA>
        <suma_couto_adic>{$adic}</suma_couto_adic>
        <cuota_total>{$tot}</cuota_total>
    </datos>
"""

# Creamos el xml definitivo
xml = "<definitivo>"
res = db.executeQuery(query)
print(res, db.getHits(res))
for i in range(db.getHits(res)):
    xml += db.retrieve_text(res, i)
xml += "</definitivo>"

# Subimos el xml definitivo
db.load(xml, "GIMNASIO/definitivo.xml")
# Borramos el xml temporal
db.removeDocument("GIMNASIO/temp.xml")
