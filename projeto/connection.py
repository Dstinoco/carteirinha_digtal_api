import pymssql
import os
#from projeto.query import Query



class ConnectBanco:

    def __init__(self):

        self.username_db = os.getenv('DB_USER')
        self.password_db = os.getenv('DB_PASSWORD1') + '#' + os.getenv('DB_PASSWORD2')
        self.host_db = os.getenv('DB_HOST')
        self.database_db = os.getenv('DB_DATABASE')

        self.mydb = pymssql.connect(user=self.username_db, password=self.password_db, server=self.host_db, database=self.database_db)
        self.cursor = self.mydb.cursor()



    def __enter__(self):

        self.cursor
        return self
    

    def __exit__(self, exc_type, exc_value, traceback):

        self.mydb.close()
        self.cursor.close()


    def get_cpf(self, cpf):

        
        query = f"SELECT NOME FROM integracao_python.dw_d_top_beneficiarios WHERE CPF = '{cpf}' "

        self.cursor.execute(query)
        result = self.cursor.fetchall()

        return result[0][0]
    

    def get_carteirinha(self, cpf):
        query = f"""SELECT 
                    NOME, 
                    MATRICULA, 
                    CONVERT(VARCHAR(10), DT_NASC, 120) AS DT_NASC,
                    CONVERT(VARCHAR(10), DT_INCL, 120) AS DT_INCL,
                    PLANO 
                    from integracao_python.aux_beneficiarios_tasy WHERE CPF = '{cpf}'
                     AND ATIVO = 'S' """
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        columns = [column[0] for column in self.cursor.description]
        data_dict = [dict(zip(columns, row)) for row in result]

        return data_dict



    """def get_agenda(self, page, page_size, indica_marcacao=None, data_marcacao=None, uf=None):

        offset = (page - 1) * page_size
        filters = []
        query = self.base_query 

        if indica_marcacao is not None and indica_marcacao != '':
            filters.append(f"INDICA_MARCACAO = '{indica_marcacao}'")
            
        if data_marcacao is not None and data_marcacao != '':
            filters.append(f"DATA_MARCACAO_ORIGINAL = '{data_marcacao}'")

        if uf is not None and uf != '':
            filters.append(f"ESTADO_UNIDADE= '{uf}'")   

        if filters:
            query += ' WHERE ' + ' AND '.join(filters)

        query += f" ORDER BY ID_MARCACAO  OFFSET {offset} ROWS FETCH NEXT {page_size} ROWS ONLY"
        
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        columns = [column[0] for column in self.cursor.description]
        data = [dict(zip(columns, row))  for row in results]

        return data """
    

    """def count_get_agenda(self, indica_marcacao=None, data_marcacao=None, uf=None):

        query = "SELECT COUNT(*) FROM [med-dw-interop].integracao_python.aux_agenda_beneficiario"
        filters = []

        if indica_marcacao is not None and indica_marcacao != '':
            filters.append(f"INDICA_MARCACAO = '{indica_marcacao}'")
            
        if data_marcacao is not None and data_marcacao != '':
            filters.append(f"DATA_MARCACAO_ORIGINAL = '{data_marcacao}'")

        if uf is not None and uf != '':
            filters.append(f"ESTADO_UNIDADE= '{uf}'")   

        if filters:
            query += ' WHERE ' + ' AND '.join(filters)
        
        self.cursor.execute(query)
        result = self.cursor.fetchone()[0]
        return result"""


    def insert_log(self, data, payload, ip, user_agent, pais, uf, cidade, empresa, latitude, longitude, rota, metodo, api_nome):
        query = f"INSERT INTO [med-dw-interop].integracao_python.api_log_conexao (DATA_ACESSO, PAYLOAD, IP, USER_AGENT, PAIS, UF, CIDADE, EMPRESA, LATITUDE, LONGITUDE, ROTA, METODO, API_NOME) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.cursor.execute(query, (data, payload, ip, user_agent, pais, uf, cidade, empresa, latitude, longitude, rota, metodo, api_nome))
        self.mydb.commit()