from flask_restx import fields
from projeto import api


login_payload = api.model('Login', {
    'Username': fields.String(required=True, description='Nome de usuário'),
    'Password': fields.String(required=True, description='Senha de acesso')
})