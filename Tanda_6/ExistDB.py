from pyexistdb import db, patch

patch.request_patching(patch.XMLRpcLibPatch)
db.ExistDB("http://admin:dm2@localhost:8080/exist/")
# db.ExistDB("http://admin:dm2@localhost:8080/exist/" + coleccion)
