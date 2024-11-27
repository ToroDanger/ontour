from decouple import config
import datetime
import jwt
import pytz


class Security():

    secret = config('JWT_KEY')
    tz = pytz.timezone("America/Santiago")

    @classmethod
    def generate_token(cls, authenticated_user):
        payload = {
            'iat': datetime.datetime.now(tz=cls.tz),
            'exp': datetime.datetime.now(tz=cls.tz) + datetime.timedelta(minutes=10),
            'mail': authenticated_user.mail
        }
        return jwt.encode(payload, cls.secret, algorithm="HS256")
    

    
    @classmethod
    def verify_token(cls, headers):
        if 'Authorization' in headers.keys():
            authorization = headers['Authorization']
            try:
                encoded_token = authorization.split(" ")[1]
                
                if len(encoded_token) > 0:
                    decoded_token = jwt.decode(encoded_token, cls.secret, algorithms=['HS256'])
                    # el contenido del token decodificado
                    print(decoded_token)  

                    return True
            except jwt.ExpiredSignatureError:
                print("Token ha expirado.")
            except jwt.InvalidSignatureError:
                print("Firma del token no válida.")
            except jwt.DecodeError:
                print("Error al decodificar el token.")
            except Exception as e:
                print(f"Error inesperado: {e}")
        
        return False
    

    