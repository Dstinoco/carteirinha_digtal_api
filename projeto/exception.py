from projeto import app
from flask import jsonify

from flask_jwt_extended.exceptions import NoAuthorizationError
from jwt import DecodeError


@app.errorhandler(404)  
def pagina_nao_encontrada(error):
    return jsonify({'Mensagem': 'URL incorreta consulte a documentação'}), 404


@app.errorhandler(NoAuthorizationError)
def handle_auth_error(e):
    return {"Mensagem":  'Autenticação necessária'}, 401


@app.errorhandler(DecodeError)
def handle_invalid_token_error(e):
    return {"Mensagem":  'Token Inválido!'}, 422