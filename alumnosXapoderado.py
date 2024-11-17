from flask import jsonify, request

def alumnos_apoderado(conexion):
    apoderado = request.args.get('apoderado')

    cursor = conexion.connection.cursor()
    sql = """SELECT 	c.nomCurso,
                        c.nomColegio,
                        p.ciudad,
                        a.rut
                FROM alumno a
                INNER JOIN curso c
                    ON (a.curso = c.id)
                INNER JOIN paqueteturistico p
                    ON (c.paqueteTuristico = p.id)
                WHERE a.apoderado = '{0}';""".format(apoderado)
    cursor.execute(sql)
    datos = cursor.fetchall()
    alumnos = []
    for fila in datos:
        alumno = {  "nomCurso":fila[0], 
                    "nomColegio":fila[1], 
                    "ciudad":fila[2], 
                    "rut":fila[3]}
        alumnos.append(alumno)
    return jsonify({'alumnos':alumnos, 'mensaje':'Alumnos del apoderado obtenidos con éxito'})