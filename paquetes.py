from flask import jsonify
import math

def valor_paquete(conexion, paqueteTuristico, cantAlumnos):
    cursor = conexion.connection.cursor()
    sql = "SELECT totalPaquete FROM paqueteturistico where id = '{0}'".format(paqueteTuristico)
    cursor.execute(sql)
    dato = cursor.fetchone()
    valorPaquete = dato[0]
    valorCuotaAlumno = math.ceil((valorPaquete / cantAlumnos) / 8)

    return valorCuotaAlumno

def get_paquetes(conexion):
    cursor = conexion.connection.cursor()
    sql = "SELECT * FROM paqueteturistico"
    cursor.execute(sql)
    datos = cursor.fetchall()
    paquetes = []
    for fila in datos:
        paquete = {'id':fila[0],
                   'nomPaquete':fila[1],
                   'totalPaquete':fila[2],
                   'hospedaje':fila[3],
                   'transporte':fila[4],
                   'ciudad':fila[5]}
        paquetes.append(paquete)
    return jsonify({'paquetes':paquetes,'Mensaje':'Carga Ok'})