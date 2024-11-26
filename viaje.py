from flask import jsonify, request

def verInfoViaje(conexion):
    alumno = request.args.get('alumno')

    cursor = conexion.connection.cursor()
    sql = """SELECT a.nom AS nomAlumno,
                CONCAT(a.appat,' ',a.appat) AS Alumno,
                c.nomCurso,
                c.nomColegio,
                p.ciudad AS destino
        FROM alumno a
        INNER JOIN curso c ON (a.curso = c.id)
        INNER JOIN paqueteTuristico p ON (c.PaqueteTuristico = p.id)
        WHERE a.id = '{0}';""".format(alumno)
    
    cursor.execute(sql)
    datos = cursor.fetchone()

    viaje = {
        "nomAlumno": datos[0],        
        "appatAlumno": datos[1],    
        "nomCurso": datos[2],        
        "nomColegio": datos[3],       
        "destino": datos[4]
    }

    return jsonify({'viaje': viaje, 'mensaje': 'Info del viaje obtenida con éxito'})