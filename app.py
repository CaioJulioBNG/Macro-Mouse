from pynput import keyboard, mouse
import time
from pymongo import MongoClient
import os
import json


class Macro():

    def __init__(self):
        self.db_config = 'db_config.json'                # Caminho para o arquivo de configuração do MongoDB
        self.check_db_config()                           # Função para criar (caso não exista) o arquivo de configuração MongoDB
        mongo_url = self.get_db_config()                 # Jogando os dados com a função 'get_db_config()' na variável mongo_url
        self.collection = self.conect_db(mongo_url)      # Função para conectar no MongoDB
        self.default_load(self.collection)               # Carregamento da configuração Default
        self.menu()        
        #self.carregar_configuracoes(self.collection)                              # Menu


    def check_db_config(self):

        # Caso o Documento de configuração não exista, ele irá entrar nesse 'if'
        if not os.path.exists(self.db_config):
            with open(self.db_config, 'w') as json_file:
                print("Carregando Configuração do Banco de Dados...")
                data = input("Digite o link do MongoDB (SEM AS ASPAS)")
                json.dump({"mongo_url": data}, json_file, indent=4)
                print("Arquivo de Configuração Salvo !")
        else:
            print("Arquivo de Configuração do Banco de Dados Carregado!")

    def get_db_config(self):

        # Abrindo o Arquivo de configuração para obter os dados
        with open(self.db_config, 'r') as json_file:
            config = json.load(json_file)
            mongo_url = config.get("mongo_url")

            return mongo_url

    def conect_db(self, url):

        # Realizando a Conexão com o MongoDB
        client = MongoClient(url)
        db = client["macro"]
        collection = db["config"]
        
        # Retornando a Collection para outras funções usarem
        return collection
    
    def default_load(self, collection):

        # Documento Inicial
        default = {
            "Nome": "Configuração Inicial",
            "f6": "10",
            "htk2": ["Exemplo", "array"]
        }

        # Insere o documento Default caso não exista
        if collection.count_documents({"Nome": "Configuração Inicial"}) == 0:
            collection.insert_one(default)
    
    def menu_configurar_macro(self):
        print("Trocar Configuração Geral")
        print("Adicionar Macro")
        print("Remover Macro")

    def carregar_configuracoes(self, collection):
        print("Monstrando Configurações Salvas !")
        print('-'*35)
        configuracoes = collection.find({}, {"Nome": 1, "_id":0 })
        for i in configuracoes:
            print(i.get("Nome",""))
        print('-'*35)

    def menu(self):
        print("Menu:")
        print("(0) Carregar Configurações")
        print("(1) Configurar Macro")
        print("(2) Executar Macro")
        option = input("Digite a Opção:")
        self.menu_handler(option)

    def menu_handler(self, option):
        match option:
            case '0':
                self.carregar_configuracoes(self.collection)
            
            case '1':
                pass

            case '2':
                pass






if __name__ == "__main__":
    Macro()