import requests
import random
import openai
import json
import pandas as pd

sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app'

df = pd.read_csv('Ia_Generativa_em_ETL_Python\SDW2023.csv')
user_ids = df['UserID'].tolist()
print(user_ids)

# Funcao para fazer o GET na api
def get_user(id):
    response = requests.get(f'{sdw2023_api_url}/users/{id}')                 # Inserindo URL do GET 
    return response.json() if response.status_code == 200 else None          # Definindo o retorno, se o codigo de status for 200, retorne o JSON, senão retorne nada

openai.api_key = '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'

def generate_ai_msg(user):
    completion = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    messages = [
        {
            "role": "system",
            "content": "Voce é um especialista em marketing bancário."
        },
        {
            "role": "user",
            "content": f"Crie uma mensagem para {user['name']} sobre a importância dos investimentos (máximo de 100 caracteres)"
        }
    ]
    )
    numero_aleatorio = random.randint(0, 5)
    responseChatGPT = completion.choices[numero_aleatorio].message.content              # Se tiver adicionando aspas duplas, para remover basta incluir o .strip('\"')
    return responseChatGPT

def update_user(user):
    response = requests.put(f"{sdw2023_api_url}/users/{user['id']}", json = user)
    return 'Sim' if response.status_code == 200 else 'Nao'


users = [user for id in user_ids if (user := get_user(id)) is not None]  # := Walrus operator. A linha pega o usuario para a lista de ID's e atruibiu ele ao Get e so atribuira se de fato for None

for user in users:
    news = generate_ai_msg(user)
    print(news)
    user['news'].append({
        "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
        "description": news
    })

for user in users:
    success = update_user(user)
    print(f"O usuário {user['name']} foi atualizado? {success}")


