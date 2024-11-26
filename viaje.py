from flask import jsonify, request

def verInfoViaje(conexion):
    alumno = request.args.get('alumno')

    cursor = conexion.connection.cursor()
    sql = """SELECT CONCAT(a.nom,' ',a.appat) AS Alumno,
                c.nomCurso,
                c.nomColegio,
                p.ciudad AS destino
        FROM alumno a
        INNER JOIN curso c ON (a.curso = c.id)
        INNER JOIN paqueteTuristico p ON (c.PaqueteTuristico = p.id)
        WHERE a.id = '{0}';""".format(alumno)
    
    cursor.execute(sql)
    datos = cursor.fetchone()

    if datos:
        viaje = {
            "nomAlumno": datos[0],        
            "nomCurso": datos[1],        
            "nomColegio": datos[2],       
            "destino": datos[3]
        }
        
        return jsonify({'viaje': viaje, 'mensaje': 'Info del viaje obtenida con éxito'})
    else:
        return jsonify({'mensaje': 'No se encontró información para el alumno especificado'}), 404
