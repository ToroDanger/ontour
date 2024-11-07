1) Iniciar Virtual Enviromente

        -pip install virtualenv
        -virtualenv -p python venv 

2) Instalar dependencias del proyecto

        -pip install -r requirements.txt
        
3) configurar Base de datos

        -crear archivo .env 
        -ingresar los siguientes datos:

            MYSQL_HOST=localhost
            MYSQL_USER=root
            MYSQL_PASSWORD= TU CONTRASEÑA
            MYSQL_DB= EL NOMBRE DEL ESQUEMA

4) Para ejecutar el servidor usar 

        python app.py                   