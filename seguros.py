from flask import jsonify, request

def get_seguros(conexion):
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
    return jsonify({'mensaje':'Consulta Ok', 'Seguros': seguros}), 200
