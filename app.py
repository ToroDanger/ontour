from flask import Flask, jsonify, request
from flask_mysqldb import MySQL 
import pagos, alumnos, seguros, cursos, paquetes
import pandas as pd
import math
import os
from config import config

app = Flask(__name__)
app.config.from_object(config['development'])

conexion = MySQL(app)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

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

    cursoId = cursos.post_curso(conexion, contrato, nomCurso ,nomColegio ,paqueteTuristico ,seguro ,cantAlumnos, app)
    valorCuotaAlumno = paquetes.valor_paquete(conexion, paqueteTuristico, cantAlumnos)
    lista_alumnos = alumnos.cargar_alumnos(conexion=conexion, cursoId=cursoId, xlsx_df=xlsx_df, valorCuotaAlumno=valorCuotaAlumno)

    return f'Se ha creado el curso {nomCurso}, se han cargado {len(lista_alumnos)} alumnos'

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()