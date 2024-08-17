from projeto import api

from ..views.login import Login
from ..views.beneficiarios import GetCpf
from ..views.carteirinha import GetCarteirinha



api.add_resource(Login, '/api/v1/authenticate')
api.add_resource(GetCpf, '/api/v1/beneficiario/<string:cpf>')
api.add_resource(GetCarteirinha, '/api/v1/carteirinha/<string:cpf>')