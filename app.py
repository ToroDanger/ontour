from flask import Flask, jsonify, request
from flask_mysqldb import MySQL 

from config import config

app = Flask(__name__)

conexion = MySQL(app)

@app.route('/home')
def home():
    return jsonify({"message":"Bienvenido a mi BackEnd"})

@app.route('/pagos', methods=['GET'])
def lista_pagos():
    try:
        id_param = request.args.get('id')

        if(id_param):
            cursor=conexion.connection.cursor()
            sql="SELECT * FROM pago WHERE id = '{0}' ".format(id_param)
            cursor.execute(sql)
            datos=cursor.fetchall()
            pagos=[]
            for fila in datos:
                pago={'id':fila[0],'estadoPago':fila[1], 'montoPago':fila[2], 'nroTarjeta':fila[3], 'fecVen':fila[4], 'cvv':fila[5]}
                pagos.append(pago)
            return jsonify({'pagos': pagos, 'mensaje': 'Pagos listados'})
        else:
            cursor=conexion.connection.cursor()
            sql='SELECT * FROM pago'
            cursor.execute(sql)
            datos=cursor.fetchall()
            pagos=[]
            for fila in datos:
                pago={'id':fila[0],'estadoPago':fila[1], 'montoPago':fila[2], 'nroTarjeta':fila[3], 'fecVen':fila[4], 'cvv':fila[5]}
                pagos.append(pago)
            return jsonify({'pagos': pagos, 'mensaje': 'Pagos listados'})
    except Exception as ex:
        return 'Error ' + ex
    
@app.route('/alumnos', methods=['GET'])
def lista_alumnos():
    id_param = request.args.get('id')
    apoderado_param = request.args.get('apoderado')
    rut_param = request.args.get('rut')
    curso_param = request.args.get('curso')

    if(id_param):
        cursor=conexion.connection.cursor()
        sql = """SELECT al.id, 
                        concat(us.nom,' ',us.appat,' ',us.apmat) as apoderado,
                        al.rut, 
                        al.nom, 
                        al.appat, 
                        al.apmat, 
                        cu.nomCurso
                FROM alumno al
                INNER JOIN user us
                    ON (al.apoderado = us.id)
                INNER JOIN curso cu
                    ON (al.curso = cu.id)
                WHERE al.id = '{0}' """.format(id_param)
        cursor.execute(sql)
        datos=cursor.fetchall()
        alumnos = []
        for fila in datos:
            alumno ={'id': fila[0], 
                   'apoderado': fila[1], 
                   'rut':fila[2], 
                   'nom':fila[3], 
                   'appat':fila[4], 
                   'apmat':fila[5], 
                   'curso': fila[6]}
            alumnos.append(alumno)
        return jsonify({'alumnos': alumnos, 'mensaje': 'Carga Ok', 'codigo': 200})
    elif(apoderado_param):
        return 'hola'
    elif(rut_param):
        return 'hola'
    elif(curso_param):
        return 'hola'
    else:
        cursor=conexion.connection.cursor()
        sql = """SELECT al.id, 
                        concat(us.nom,' ',us.appat,' ',us.apmat) as apoderado,
                        al.rut, 
                        al.nom, 
                        al.appat, 
                        al.apmat, 
                        cu.nomCurso
                FROM alumno al
                INNER JOIN user us
                    ON (al.apoderado = us.id)
                INNER JOIN curso cu
                    ON (al.curso = cu.id)"""
        cursor.execute(sql)
        datos=cursor.fetchall()
        alumnos = []
        for fila in datos:
            alumno ={'id': fila[0], 
                   'apoderado': fila[1], 
                   'rut':fila[2], 
                   'nom':fila[3], 
                   'appat':fila[4], 
                   'apmat':fila[5], 
                   'curso': fila[6]}
            alumnos.append(alumno)
        return jsonify({'alumnos': alumnos, 'mensaje': 'Carga Ok', 'codigo': 200})

@app.route('/seguros', methods=['GET'])
def listar_seguro():
    cursor=conexion.connection.cursor()
    sql = "SELECT * FROM seguro"
    cursor.execute(sql)
    datos = cursor.fetchall()
    seguros = []
    for fila in datos:
        fila = {'id':fila[0], 
                'empresaSeguro':fila[1],
                'nomSeguro': fila[2],
                'valorSeguro':fila[3],
                'coberturaSeguro':fila[4]}
        seguros.append(fila)
    return jsonify({'mensaje':'Consulta Ok', 'Seguros': seguros})

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()