from flask_restx import Resource
from flask import jsonify
from flask_jwt_extended import jwt_required

from projeto import api
from ..connection import ConnectBanco


class GetCpf(Resource):

    @api.doc(security='Bearer')
    @jwt_required()
    @api.doc(params={'cpf': {'in': 'path', 'description': 'CPF do beneficiário', 'type': 'string'}})
    def get(self, cpf):

        try:

            cpf = cpf.replace(".", "")
            cpf = cpf.replace("-", "")

            with ConnectBanco() as db:
                result = db.get_cpf(cpf)

            data_json = {
                'nome': result
            }    

            return data_json, 200
        
        except Exception as e:
            return {"error": str(e)}, 500