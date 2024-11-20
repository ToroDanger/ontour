from flask import Flask, jsonify, request, send_file
from flask_mysqldb import MySQL
import pagos, alumnos, seguros, cursos, paquetes, login
import pandas as pd
import os
from config import config



app = Flask(__name__)
app.config.from_object(config['development'])

conexion = MySQL(app)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/login', methods=['POST'])
def login_get():
    return login.login(conexion)

@app.route('/home')
def home():
    return jsonify({"message":"Bienvenido a mi BackEnd"})

@app.route('/pagos', methods=['GET'])
def listar_pagos():
    return pagos.get_pagos(conexion)
    
@app.route('/alumnos', methods=['GET'])
def lista_alumnos():
    return alumnos.get_alumnos(conexion)

@app.route('/seguros', methods=['GET'])
def listar_seguro():
    return seguros.get_seguros(conexion)

@app.route('/cursos', methods=['GET'])
def listar_cursos():
    return cursos.get_curso(conexion)

@app.route('/cursos', methods=['POST'])
def agregar_curso():
    try:
        conexion.connection.begin()

        if 'Planilla' not in request.files:
            return jsonify({'error': 'No se ha enviado un archivo'}), 400
        if 'contrato' not in request.files:
            return jsonify({'error': 'No se ha enviado un archivo'}), 400 

        Planilla = request.files['Planilla']
        contrato = request.files['contrato']
        xlsx_df = pd.read_excel(Planilla, sheet_name='Alumnos')
        nomCurso = request.form.get('nomCurso')
        nomColegio = request.form.get('nomColegio')
        paqueteTuristico = request.form.get('paqueteTuristico')
        seguro = request.form.get('seguro')
        cantAlumnos = len(xlsx_df)
        fechaViaje = request.form.get('fechaViaje')

        cursoId = cursos.post_curso(conexion, contrato, nomCurso ,nomColegio ,paqueteTuristico ,seguro ,cantAlumnos, app, fechaViaje)
        valorCuotaAlumno = paquetes.valor_paquete(conexion, paqueteTuristico, cantAlumnos)
        listaAlumnos = alumnos.cargar_alumnos(conexion=conexion, cursoId=cursoId, xlsx_df=xlsx_df, valorCuotaAlumno=valorCuotaAlumno)

        conexion.connection.commit()

        return f'Se ha creado el curso {nomCurso}, se han cargado {len(listaAlumnos)} alumnos'
    except Exception as e:
        conexion.connection.rollback()
        print(e)
        return 'Error en la carga de Datos, favor validar datos a cargar o archivo Excel'
        

@app.route('/archivos', methods=['GET'])
def lista_doc():
    cursor=conexion.connection.cursor()
    sql = "SELECT * FROM archivo"
    cursor.execute(sql)
    datos = cursor.fetchall()
    archivos = []
    for fila in datos:
        fila = {'id':fila[0],
                'curso':fila[1],
                'nombre':fila[2]}
        archivos.append(fila)
    return jsonify({'archivos':archivos})

@app.route('/get_pdf/<filename>', methods=['GET'])
def get_pdf(filename):
    file_path = os.path.join('uploads', filename)
    try:
        return send_file(file_path, as_attachment=True)
    except FileNotFoundError:
        return jsonify({'error': 'Archivo no encontrado'}), 404
    
@app.route('/pagos', methods=['POST'])
def agregar_pago():
    cursor = conexion.connection.cursor()
    datos = request.get_json()

    nroTarjeta = datos.get('nroTarjeta')
    fecVen = datos.get('fecVec')
    cvv = datos.get('cvv')

    cuotas = datos.get('cuotas', [])
    cuotaStr = str(tuple(cuotas))
    sql = "UPDATE cuota SET pagado = 1 WHERE id in {0}".format(cuotaStr)
    cursor.execute(sql)

    sql = "INSERT INTO pago (montoPago, nroTarjeta, fecVen, cvv) VALUES ((SELECT sum(valorCuota) FROM cuota where id in {0}), '{1}', '{2}', '{3}')".format(cuotaStr, nroTarjeta, fecVen, cvv)
    cursor.execute(sql)

    pagoId = cursor.lastrowid

    for cuota in cuotas:
        sql = "INSERT INTO pagocuota (cuota, pago) VALUES ('{0}','{1}')".format(cuota, pagoId)
        cursor.execute(sql)
    
    conexion.connection.commit()
    return jsonify({"Mensaje":"Pago Ingresado Ok"})
    
@app.route('/alumnos/apoderado', methods=['GET'])
def alumnos_apoderado():

    apoderado = request.args.get('apoderado')

    cursor = conexion.connection.cursor()
    sql = """SELECT 	a.id,
                        c.nomCurso,
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
        alumno = {  "alumno":fila[0],
                    "nomCurso":fila[1], 
                    "nomColegio":fila[2], 
                    "ciudad":fila[3], 
                    "rut":fila[4]}
        alumnos.append(alumno)
    return jsonify({'alumnos':alumnos, 'mensaje':'Hola Karlita'})
    

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()