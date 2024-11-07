from flask import Flask, jsonify
from flask_mysqldb import MySQL 

from config import config

app = Flask(__name__)

conexion = MySQL(app)

@app.route('/home')
def home():
    return jsonify({"message":"Bienvenido a mi BackEnd"})

@app.route('/pagos', methods=['GET'])
def lista_pago():
    try:
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
        print('Error')
        return 'Error'

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()