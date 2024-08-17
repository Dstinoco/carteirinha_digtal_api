from projeto import api
from flask import jsonify, request
from flask_jwt_extended import create_access_token
from projeto.model import Users
from flask_restx import Resource
from projeto.fields import login_payload
from projeto.connection import ConnectBanco
from datetime import datetime
import pytz
import json
from projeto.geo_location.geo import dados_ip

fuso = pytz.timezone('America/Sao_Paulo')




class Login(Resource):

    @api.expect(login_payload)
    @api.doc(responses={200: 'Sucesso', 401: 'Credenciais inválidas'})
    def post(self):

        try: 
            ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
            #ip_address = '177.137.232.38' 
            data = request.get_json()
            user_agent = request.user_agent.string
            data_hora = datetime.now(fuso)
            metodo=request.method
            rota = request.path
            payload = request.json
            payload_json = json.dumps(payload)
            endereco, empresa = dados_ip(ip_address)
            api_nome = 'Beneficiarios_bemoby'
           
            with ConnectBanco() as db:
                db.insert_log(ip=ip_address, data=data_hora, payload=payload_json, user_agent=user_agent, pais=endereco['country_name'],
                                uf=endereco['region_code'], cidade=endereco['city'], empresa=empresa, latitude=endereco['latitude'], longitude=endereco['longitude'],
                                rota=rota, metodo=metodo, api_nome=api_nome)

            user = Users.query.filter_by(Username = data.get('Username')).first()

            if user and user.check_password(data.get('Password')):
                access_token = create_access_token(identity=user.Id)
                
                return {'access_token': access_token}, 200
            else:
                return {'mensagem': 'Credenciais inválidas'}, 401
        

        except Exception as e:
            return {"error": str(e)}, 500