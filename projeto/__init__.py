from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

import os

username_db = os.getenv('DB_USER')
password_db = os.getenv('DB_PASSWORD1') + '#' + os.getenv('DB_PASSWORD2')
host_db = os.getenv('DB_HOST')
database_db = os.getenv('DB_DATABASE')



authorization = {
    'Bearer': {
        'description':'No campo Value digite: "Bearer <access_token>"',
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}


api = Api(default="Rotas", default_label="Rotas disponíveis", title='Bemoby Beneficiarios', 
          description='API de integração com o Bemoby, retornando o Nome do beneficiario e tambem a carteirinha', prefix='', authorizations=authorization)



app = Flask(__name__)
database = SQLAlchemy()
JWTManager(app)

#drive = 'SQL+Server' #local ativar essa
drive = 'ODBC+Driver+17+for+SQL+Server'

app.config['JWT_SECRET_KEY'] = "" # key removida
app.config['SQLALCHEMY_DATABASE_URI'] = f'mssql+pyodbc://{username_db}:{password_db}@{host_db}:1433/{database_db}?driver={drive}' #trocar em prod: driver=SQL+Server
app.config.SWAGGER_UI_DOC_EXPANSION = 'list'




api.init_app(app)
database.init_app(app)


from projeto import exception
from projeto.routes import routes