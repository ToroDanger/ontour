from flask import jsonify
import math

def valor_paquete(conexion, paqueteTuristico, cantAlumnos):
    cursor=conexion.connection.cursor()
    sql = "SELECT totalPaquete FROM paqueteturistico where id = '{0}'".format(paqueteTuristico)
    cursor.execute(sql)
    dato = cursor.fetchone()
    valorPaquete = dato[0]
    valorCuotaAlumno = math.ceil((valorPaquete / cantAlumnos) / 8)

    return valorCuotaAlumno