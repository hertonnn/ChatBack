import json 
from datetime import datetime

def aplica(funcao):

    if funcao == 'hora':
        hora_atual = datetime.now()
        hora =  "São exatamente: " + hora_atual.strftime("%H:%M")

        return hora
""" def aprende_resposta(arquivo):

    # separar em sentenças a msg
    stok = nltk.data.load('tokenizers/punkt/portuguese.pickle')
    
    mensagem = input('Semelhantes\n>')
    respostas = input('Resposta\n>')
    tag = input('Tag\n>')
    semelhantes = stok.tokenize(mensagem)

    with open(arquivo) as f:
        data = json.load(f)
    data['intencoes'].append({
            "tag": tag,
            "semelhantes": [semelhantes],
            "respostas": [respostas],
            "funcao": False
    })

    with open(arquivo, 'w') as f:
        json.dump(data, f, indent=1, ensure_ascii=False)

    f.close()
    print('certo') """
        
