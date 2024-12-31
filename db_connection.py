import os
import json
from pymongo import MongoClient

class DBConnection:

    _instance = None

    def __init__(self):
        self.db_config = 'db_config.json'  
        self.client = None
        self.check_config()
        
    def check_config(self):
        print('Iniciando verificação da configuração do banco de dados...')
        # Caso o Documento de configuração não exista, ele irá entrar nesse 'if'
        if not os.path.exists(self.db_config):
            with open(self.db_config, 'w') as json_file:
                print("Banco de dados não configurado !")
                data = input("Digite o link do MongoDB (SEM AS ASPAS)")
                json.dump({"mongo_url": data}, json_file, indent=4)
                print("Arquivo de Configuração Salvo !")
        else:
            print("Verificação concluída!")

    def connect(self):
        print("Iniciando conexão com o MongoDB")
        if self.client is None:
            with open(self.db_config, 'r') as json_file:
                config = json.load(json_file)
                mongo_url = config.get("mongo_url")

                if mongo_url:
                    try:
                        self.client = MongoClient(mongo_url)
                        self.client.admin.command('ismaster')
                        print("Conexão com MongoDB realizada com sucesso!")
                    except ConnectionError as e:
                        print(f"Erro ao conectar ao MongoDB {e}")

conexao = DBConnection()
conexao.connect()