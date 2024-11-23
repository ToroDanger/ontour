from flask import jsonify

def total_a_pagar_por_curso(conexion, curso_id):  # Recibe conexion y curso_id
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
                c.id = %s;"""
    cursor.execute(sql, (curso_id,))
    datos = cursor.fetchall()

    return {'total_a_pagar': datos[0][0] if datos else '0', 'mensaje': 'Total a pagar por curso obtenido con éxito'}


def total_a_pagar_por_alumno(conexion, curso_id):  # Recibe conexion y curso_id
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
                c.id = %s;"""
    cursor.execute(sql, (curso_id,))
    datos = cursor.fetchall()

    return {'total_a_pagar_alumno': datos[0][0] if datos else '0', 'mensaje': 'Total a pagar por alumno obtenido con éxito'}


def total_pagado_por_alumno(conexion, alumno_id):  # Recibe conexion y alumno_id
    cursor = conexion.connection.cursor()
    sql = """SELECT 
                SUM(c.valorCuota) AS 'Total Pagado'
            FROM 
                cuota c
            WHERE 
                c.alumnoCuota = %s
                AND c.pagado = TRUE;"""
    cursor.execute(sql, (alumno_id,))
    datos = cursor.fetchall()

    return {'total_pagado': datos[0][0] if datos else '0', 'mensaje': 'Total pagado por alumno obtenido con éxito'}


def saldo_por_pagar(conexion, alumno_id):  # Recibe conexion y alumno_id
    cursor = conexion.connection.cursor()
    sql = """SELECT 
                CONCAT('$', FORMAT(SUM(valorCuota), 0)) AS 'Saldo por Pagar'
            FROM 
                cuota
            WHERE 
                alumnoCuota = %s 
                AND pagado = FALSE 
                AND fechaVenc < NOW();"""
    cursor.execute(sql, (alumno_id,))
    datos = cursor.fetchall()

    return {'saldo_por_pagar': datos[0][0] if datos else '$0', 'mensaje': 'Saldo por pagar obtenido con éxito'}
