# Nombre: Clase main
# Propósito: hacer la conexión a la base de datos mongodb mediante python
# Fecha: 2024/05/07
import pymongo
import datetime

# Conexión con la base de datos
myclient = pymongo.MongoClient("localhost", 27017)
mydb = myclient["sevilla_historica"]
mycol = mydb["lugares"]
# print(db.name)
# print(db.list_collection_names())
salirya = False
while (salirya is False):
    salir1 = False
    print("Bienvenido a la base de datos de Sevilla Histórica, por favor elige tu opción:")
    print("1 para dar de alta documentos en lugares")
    print("2 para actualizar documentos en lugares")
    print("3 para eliminar un cocumento en lugares")
    print("4 para mostrar todos los documentos en lugares")
    print("5 para 3 búsquedas por defecto")
    print("6 para eliminar todos los elementos  en lugares")
    print("7 para eliminar la colección")
    print("8 para salir")
    opcion = input("Elige la opcion que prefieras: ")
    if opcion == "1":
        while salir1 is False:
            print("Has elegido dar de alta documento, ")
            entrada = input(
                "Inserta nombre, descripcion, ubicacion, año de construccion y visitantes anuales (en miles) separados por coma")
            datos = entrada.split(", ")
            print(datos)
            mydb.lugares.insert_one(
                {"nombre": datos[0], "descripcion": datos[1], "ubicacion": datos[2], "anoConstruccion": int(datos[3]),
                 "milesturistasanuales": int(datos[4])})
            salirinsertar = input("Pulse 1 para introducir más documentos")
            if salirinsertar == "1":
                print("A continuación insertará otro documento")
            else:
                salir1 = True
        pausa = input("Introduzca cualquier valor para continuar")
    if opcion == "2":
        print("Has elegido actualizar documento, ")
        opcionupdate = input("Puedes elegir actualizar uno solo (1) o varios (cualquier otro número)")
        if opcionupdate == "1":
            parteactualizar = input("Especifica la consulta que quieres hacer, por ejemplo nombre: Parque Maria Luisa")
            actualizacion = input("Introduce el nuevo valor. Ejemplo anoConstruccion: 1925")
            splitactualizar = parteactualizar.split(": ")
            splitvalores = actualizacion.split(": ")
            if splitvalores[0] == "anoConstruccion" or splitvalores[0] == "milesturistasanuales":
                splitvalores[1] = int(splitvalores[1])
            myquery = {splitactualizar[0]: splitactualizar[1]}
            newvalues = {"$set": {splitvalores[0]: splitvalores[1]}}
            x = mycol.update_one(myquery, newvalues)
            print(x.modified_count, "actualización correcta")
            pausa = input("Introduzca cualquier valor para continuar")
        else:
            parteactualizar = input("Especifica la consulta que quieres hacer, por ejemplo ubicacion: centro")
            actualizacion = input("Introduce el nuevo valor. Ejemplo milesturistasanuales: 2500")
            splitactualizar = parteactualizar.split(": ")
            splitvalores = actualizacion.split(": ")
            if splitvalores[0] == "anoConstruccion" or splitvalores[0] == "milesturistasanuales":
                myquery = {splitactualizar[0]: splitactualizar[1]}
                newvalues = {"$set": {splitvalores[0]: int(splitvalores[1])}}
                x = mycol.update_many(myquery, newvalues)
                print(x.modified_count, "actualización correcta")
                pausa = input("Introduzca cualquier valor para continuar")
            else:
                myquery = {splitactualizar[0]: splitactualizar[1]}
                newvalues = {"$set": {splitvalores[0]: splitvalores[1]}}
                x = mycol.update_many(myquery, newvalues)
                print(x.modified_count, "actualización correcta")
                pausa = input("Introduzca cualquier valor para continuar")
    if opcion == "3":
        print("Has elegido eliminar un documento")
        consulta = input(
            "Introduce la consulta del documento que quieres eliminar, por ejemplo nombre: Parque Maria Luisa ")
        splitconsulta = consulta.split(": ")
        pregunta = input("¿Está seguro que quiere eliminar el documento con " + splitconsulta[0] + " " + splitconsulta[
            1] + "? Si está seguro pulse 1 ")
        if pregunta == "1":
            if splitconsulta[0] == "anoConstruccion" or splitconsulta[0] == "milesturistasanuales":
                myquery = {splitconsulta[0]: int(splitconsulta[1])}
                mycol.delete_one(myquery)
                print("Se eliminó el documento")
                pausa = input("Introduzca cualquier valor para continuar")
            else:
                myquery = {splitconsulta[0]: splitconsulta[1]}
                mycol.delete_one(myquery)
                print("Se eliminó el documento")
                pausa = input("Introduzca cualquier valor para continuar")
        else:
            print("Ha elegido no eliminar documento")
            pausa = input("Introduzca cualquier valor para continuar")
    if opcion == "4":
        print("Has elegido Mostrar todos los documentos de la colección")
        for lugares in mydb.lugares.find():
            print(lugares)
        pausa = input("Introduzca cualquier valor para volver al menú")
    if opcion == "5":
        print("Has elegido búsquedas por defecto")
        print("Lugares con más de 500 años de antigüedad")
        hoy = datetime.date.today()
        currentyear = hoy.year
        for documents in mydb.lugares.find({"anoConstruccion": {"$lt": currentyear - 500}}):
            print(documents)
        pausa = input("Introduzca cualquier valor para continuar")
        print("Lugares que no están en el centro con más de 10000 miles de visitantes anuales")
        for documents in mydb.lugares.find(
                {"ubicacion": {"$not": {"$regex": "centro"}}, "milesturistasanuales": {"$gt": 10000}}):
            print(documents)
        pausa = input("Introduzca cualquier valor para continuar")
        print("Lugares que en el Arenal construidos antes de 1900")
        for documents in mydb.lugares.find({"ubicacion": "Arenal", "anoConstruccion": {"$lt": 1900}}):
            print(documents)
        pausa = input("Introduzca cualquier valor para continuar")
    if opcion == "6":
        print("Has elegido eliminar todos los documentos de la coleccion")
        pregunta = input("¿Está seguro que quiere eliminar TODOS los documentos de la colección? Elige 1 si quieres")
        if pregunta == "1":
            myquery = {}
            mycol.delete_many(myquery)
            print("Se eliminaron todos los documentos")
            pausa = input("Introduzca cualquier valor para continuar")
        else:
            print("No se eliminaron los documentos")
            pausa = input("Introduzca cualquier valor para continuar")
    if opcion == "7":
        print("Has elegido eliminar la colección")
        pregunta = input("¿Está seguro que quiere eliminar la colección? Elige 1 si quieres")
        if pregunta == "1":
            mydb.lugares.drop()
            print("Colección eliminada")
    if opcion == "8":
        salirya = True
print("Ha elegido salir, que tenga un buen día")
