from flask import jsonify, request

def verInfoViaje(conexion):
    apoderado = request.args.get('apoderado')

    cursor = conexion.connection.cursor()
    sql = """SELECT a.nom AS nomAlumno,
                a.appat AS appatAlumno,
                c.nomCurso,
                c.nomColegio,
                p.ciudad AS destino,
                p.fecha_ida,
                p.cant_noches
        FROM alumno a
        INNER JOIN curso c ON (a.curso = c.id)
        INNER JOIN paqueteTuristico p ON (c.PaqueteTuristico = p.id)
        INNER JOIN user u ON (a.apoderado = u.id)
        WHERE u.rut = '{0}';""".format(apoderado)
    
    cursor.execute(sql)
    datos = cursor.fetchall()
    viajes = []
    for fila in datos:
        viaje = {
            "nomAlumno": fila[0],        
            "appatAlumno": fila[1],    
            "nomCurso": fila[2],        
            "nomColegio": fila[3],       
            "destino": fila[4]          
            #"fechaIda": fila[5],        
            #"cantNoches": fila[6]
        }
        viajes.append(viaje)

    return jsonify({'viajes': viajes, 'mensaje': 'Información del viaje obtenida con éxito'})