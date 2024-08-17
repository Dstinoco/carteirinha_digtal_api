from flask_restx import Resource
from flask import jsonify, send_file
from flask_jwt_extended import jwt_required

from PIL import Image, ImageDraw, ImageFont
import io
import base64


from projeto import api
from ..connection import ConnectBanco




class GetCarteirinha(Resource):

    @api.doc(security='Bearer')
    @jwt_required()
    @api.doc(params={'cpf': {'in': 'path', 'description': 'CPF do beneficiário', 'type': 'string'}})
    def get(self, cpf):

        try:
            cpf = cpf.replace(".", "")
            cpf = cpf.replace("-", "")

            with ConnectBanco() as db:
                beneficiario = db.get_carteirinha(cpf)

                if not beneficiario:
                    return {"error": "Beneficiario não encontrado"}, 404
                
            beneficiario = beneficiario[0]
            data_nasc = str(beneficiario['DT_NASC']).split('-')
            data_nasc = data_nasc[2] + '/' + data_nasc[1] + '/' + data_nasc[0]
            data_incl = str(beneficiario['DT_INCL']).split('-')
            data_incl = data_incl[2] + '/' + data_incl[1] + '/' + data_incl[0]
            
            
            dados = {
                "carteira": "Carteirinha Digital",
                "nome": beneficiario['NOME'],
                "dt_nascimento": data_nasc,
                "matricula": beneficiario['MATRICULA'],
                "plano": beneficiario['PLANO'],
                "ans": "335614",
                "adesao": data_incl
            }
            if "BLACK" in beneficiario['PLANO']:
                imagem_base = Image.open("projeto/views/templates/carteirinha_black.png")
            else:
                imagem_base = Image.open("projeto/views/templates/Carteirinha.png")

            draw = ImageDraw.Draw(imagem_base)
            fonte1 = ImageFont.truetype("projeto/views/templates/arialbd.ttf", 85)
            fonte2 = ImageFont.truetype("projeto/views/templates/arialbd.ttf", 65)
            fonte3 = ImageFont.truetype("projeto/views/templates/arialbd.ttf", 56)
            fonte4 = ImageFont.truetype("projeto/views/templates/arialbd.ttf", 43)
            

            draw.text((100, 350), f"Carteirinha Digital", font=fonte1, fill="white")
            if len(beneficiario['NOME']) > 25 and len(beneficiario['NOME']) < 35:
                draw.text((100, 900), f"{dados['nome']}", font=fonte3, fill="white")
            elif len(beneficiario['NOME']) > 36:
                draw.text((100, 900), f"{dados['nome']}", font=fonte4, fill="white")
            else:
                draw.text((100, 900), f"{dados['nome']}", font=fonte2, fill="white")
            draw.text((100, 1010), f"{dados['matricula']}", font=fonte1, fill="white")
            draw.text((100, 1130), f"{dados['plano']}", font=fonte2, fill="white")

            draw.text((850, 1770), f"Nasc.", font=fonte2, fill="white")
            draw.text((850, 1850), f"{dados['dt_nascimento']}", font=fonte2, fill="white")

            draw.text((450, 1770), f"Adesão", font=fonte2, fill="white")
            draw.text((450, 1850), f"{dados['adesao']}", font=fonte2, fill="white")

            draw.text((100, 1770), f"ANS", font=fonte2, fill="white")
            draw.text((100, 1850), f"{dados['ans']}", font=fonte2, fill="white")

            # Reduzir o tamanho da imagem para uma largura e altura específicas
            nova_largura = 300
            nova_altura = 400
            imagem_base = imagem_base.resize((nova_largura, nova_altura))

            # Salvar a imagem em um objeto Bytes
            img_io = io.BytesIO()
            imagem_base.save(img_io, 'PNG')
            img_io.seek(0)

            # Converter a imagem para base64
            img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

            resposta = {
                    "value": "minha-carteirinha.png",
                    "key": f"data:image/png;base64,{img_base64}"
                        }

            return jsonify(resposta)
            #return send_file(img_io, mimetype='image/png')

        except Exception as e:
            return {"error": str(e)}, 500

