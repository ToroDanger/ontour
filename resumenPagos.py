from flask import jsonify, request

def total_a_pagar_por_curso(conexion):
    curso_id = request.args.get('curso_id')  # Recibe el ID del curso como parámetro

    cursor = conexion.connection.cursor()
    sql = """SELECT 
                CONCAT('$', FORMAT((p.totalPaquete + s.valorSeguro), 0)) AS 'Total a Pagar por Curso'
            FROM 
                curso c
            INNER JOIN 
                paqueteTuristico p ON c.PaqueteTuristico = p.id
            INNER JOIN 
                seguro s ON c.seguro = s.id
            WHERE 
                c.id = {0};""".format(curso_id)

    cursor.execute(sql)
    datos = cursor.fetchall()

    return jsonify({'total_a_pagar': datos[0][0] if datos else '0', 'mensaje': 'Total a pagar por curso obtenido con éxito'})


def total_a_pagar_por_alumno(conexion):
    curso_id = request.args.get('curso_id')  # Recibe el ID del curso como parámetro

    cursor = conexion.connection.cursor()
    sql = """SELECT 
                CONCAT('$', FORMAT((p.totalPaquete + s.valorSeguro) / c.cantAlumnos, 0)) AS 'Total a Pagar por Alumno'
            FROM 
                curso c
            INNER JOIN 
                paqueteTuristico p ON c.PaqueteTuristico = p.id
            INNER JOIN 
                seguro s ON c.seguro = s.id
            WHERE 
                c.id = {0};""".format(curso_id) 

    cursor.execute(sql)
    datos = cursor.fetchall()

    return jsonify({'total_a_pagar_alumno': datos[0][0] if datos else '0', 'mensaje': 'Total a pagar por alumno obtenido con éxito'})

def total_pagado_por_alumno(conexion):
    alumno_id = request.args.get('alumno_id')  # Recibe el ID del alumno como parámetro

    cursor = conexion.connection.cursor()
    sql = """SELECT 
                SUM(c.valorCuota) AS 'Total Pagado'
            FROM 
                cuota c
            WHERE 
                c.alumnoCuota = {0}
                AND c.pagado = TRUE;""".format(alumno_id)  

    cursor.execute(sql)
    datos = cursor.fetchall()

    return jsonify({'total_pagado': datos[0][0] if datos else '0', 'mensaje': 'Total pagado por alumno obtenido con éxito'})

from flask import jsonify, request

def saldo_por_pagar(conexion):
    alumno_id = request.args.get('alumno_id')  # Recibe el ID del alumno como parámetro

    # Usamos un cursor para ejecutar la consulta
    cursor = conexion.connection.cursor()

    # Es importante usar placeholders (en lugar de formato de cadena) para evitar SQL injection
    sql = """SELECT 
                CONCAT('$', FORMAT(SUM(valorCuota), 0)) AS 'Saldo por Pagar'
            FROM 
                cuota
            WHERE 
                alumnoCuota = %s 
                AND pagado = FALSE 
                AND fechaVenc < NOW();"""

    # Ejecutamos la consulta con el alumno_id como parámetro
    cursor.execute(sql, (alumno_id,))

    # Obtenemos los resultados
    datos = cursor.fetchall()

    # Si la consulta devuelve un resultado, lo retornamos, de lo contrario retornamos '0'
    return jsonify({'saldo_por_pagar': datos[0][0] if datos else '$0', 'mensaje': 'Saldo por pagar obtenido con éxito'})
