from flask import jsonify, request
import math
import os
import pandas as pd

def get_curso(conexion):
    cursor=conexion.connection.cursor()
    sql = "SELECT * FROM curso"
    cursor.execute(sql)
    datos = cursor.fetchall()
    cursos = []
    for fila in datos:
        fila = {'id':fila[0],
                'nomCurso':fila[1],
                'nomColegio':fila[2],
                'paqueteTuristico':fila[3],
                'seguro':fila[4],
                'cantAlumnos':fila[5]}
        cursos.append(fila)
    return jsonify({'mensajes':'Consulta Ok', 'Cursos':cursos})


def post_curso(conexion, contrato, nomCurso ,nomColegio ,paqueteTuristico ,seguro ,cantAlumnos, app):
    cursor=conexion.connection.cursor()
    sql = "INSERT INTO curso (nomCurso, nomColegio, paqueteTuristico, seguro, cantAlumnos) values ('{0}','{1}','{2}','{3}','{4}');".format(nomCurso,
                                                                                                                                           nomColegio,
                                                                                                                                           paqueteTuristico,
                                                                                                                                           seguro,
                                                                                                                                           cantAlumnos) 
    cursor.execute(sql)
    conexion.connection.commit()
    
    cursoId = cursor.lastrowid
    
    sql = "INSERT INTO archivo (curso, ruta) VALUES ('{0}','{1}')".format(cursoId, contrato.filename)
    cursor.execute(sql)
    conexion.connection.commit()

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], contrato.filename)
    contrato.save(file_path)

    return cursoId