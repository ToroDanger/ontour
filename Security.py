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
            'mail': authenticated_user.mail,
            'rol': authenticated_user.rol
           
        }
        return jwt.encode(payload, cls.secret, algorithm="HS256")