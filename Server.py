# Parte ChatBot

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' ## retirar certos avisos do tensorflow
from tensorflow.keras.models import load_model
import random
import json 
import pickle as pkl
import numpy as np
import spacy ## processamento de linguagem natural
from unidecode import unidecode
from fastapi import FastAPI # API
""" from fastapi.middleware.cors import CORSMiddleware  """
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from Funcoes_extras import *

class Chatbot:
    def __init__(self, modelo_treinado, palavras, classes, banco_respostas) -> None:
        
        self.modelo = modelo_treinado
        self.palavras = palavras
        self.classes = classes
        self.intensoes = banco_respostas
        self.nlp = spacy.load('pt_core_news_sm')
        ## python3.10 -m spacy download pt_core_news_sm

    def limpa_setenca(self, frase):
        frase_palavras = self.nlp(frase)
        frase_limpa = [] 

        for palavra in frase_palavras:
            if palavra.pos_ == 'VERB':
                frase_limpa.append(palavra.lemma_.lower())
            else:
                frase_limpa.append(palavra.text.lower())


        return list(map(unidecode,frase_limpa)) # retirar acentos 

    def compara_palavras(self, frase):

        frase_palavras = self.limpa_setenca(frase)
        bag = [0] * len(self.palavras)

        for palavra in frase_palavras:
            for i, palavra_2 in  enumerate(self.palavras):
                if palavra == palavra_2:
                    bag[i] = 1
        # para cada palavra em comum que o input tenha com a minha lista de palavras
        # sera trocado para 1 o valor na lista 'bag'

        return np.array(bag)

    def predicao_classe(self, sentenca):
        
        bag = self.compara_palavras(sentenca)
        predicao = self.modelo.predict(np.array([bag]))[0]
        
        ERRO_LIMITE = 0.50 

        resultados = [[i, res] for i, res in enumerate(predicao) if res > ERRO_LIMITE]

        resultados.sort(key=lambda x: x[1], reverse=True)
            
        
        # reverse classica em ordem decrescente e key é a função usada na classificação
        # que nesse caso recebe x e retorna x[1] para ser usado como parâmetro de classi-
        # ficação.

        return_lista = []

        for resultado in resultados:
            return_lista.append({'intencao': self.classes[resultado[0]], 'probabilidade': str(resultado[1])})
        
        return return_lista

    def pega_resultado(self, intencoes_lista, intencoes_json):
        
        if intencoes_lista == []:
            resultado = "Não sei como responder isso."
            return False,resultado

        tag = intencoes_lista[0]['intencao']
        lista_de_intencoes = intencoes_json['intencoes']

        for i in lista_de_intencoes:
            if i['tag'] == tag:
                resultado = random.choice(i['respostas'])
                break
        print(intencoes_lista)
        return i,resultado 

# Criando o abjeto do tipo ChatBot

modelo = load_model('/home/herton/Documentos/PROGRAMAÇÃO/Machine Learning/Chat_IA/chatbot.h5')
palavras = pkl.load(open('/home/herton/Documentos/PROGRAMAÇÃO/Machine Learning/Chat_IA/palavras.pkl', 'rb'))
classes = pkl.load(open('/home/herton/Documentos/PROGRAMAÇÃO/Machine Learning/Chat_IA/classes.pkl', 'rb'))
intencoes = json.loads(open('/home/herton/Documentos/PROGRAMAÇÃO/Machine Learning/Chat_IA/intencoes.json').read()) 

chatbot = Chatbot(modelo, palavras, classes, intencoes)

# Parte da API

app = FastAPI()

origins = [
    'https://hertonnn.github.io'
]
## Cadastro de origens 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## criando o tipo Mensagem

class Mensagem(BaseModel):
    mensagem: str

@app.post('/mensagem')
def pegar_resposta(msg: Mensagem):
    ints = chatbot.predicao_classe(str(msg.mensagem))
    tag, saida = chatbot.pega_resultado(ints, intencoes)

    if tag and tag['funcao']:
        retorno_extra = aplica(tag['tag'])
        return retorno_extra
    else:
        return saida

# Pôr no ar: python3.10 -m uvicorn server:app --reload 
# ERROR:    Error loading ASGI app. Could not import module "server".
# Resolvido com: abrir o folder do arquivo como principal no vs code
# ModuleNotFound:
# veirificar se o módulo está instalado pip3.10 list, se não pip3.10 install <modulo> 
