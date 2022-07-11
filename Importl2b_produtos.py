# Funciona
# imports
import requests
from tqdm import tqdm
from datetime import datetime, timedelta, date
import json
import os
url = 'https://app.leads2b.com/api/v2/items/list' # Url para facilitar

headers = {
    'Authorization': 'Bearer <key>'#onde está a <key> coloque a key que leads2b disponibilizou
} # cabeçario da Requisição

data_ref = '2022-03-08' #data de ref
data_form = datetime.strptime(data_ref, '%Y-%m-%d') #formantando para o tipo: datatime

data_de_hoje = date.today().strftime('%Y-%m-%d') # data de hoje formatada
data_de_hj_form = datetime.strptime(data_de_hoje, '%Y-%m-%d') # formantando para o tipo: datatime

x=0 # variavel zerada para rodar dia a dia

## barra de loading
data_loading = data_de_hj_form - data_form # diminuindo da data de hoje a data de inicio
data_loading = str(data_loading) # transformando em string
data_loading = data_loading.split(' ')[0] # restringindo a string ao número
# data_loading = data_loading[0:2] # restringindo a string ao número
data_loading = int(data_loading) # transformando em inteiro
##

with tqdm(total=data_loading) as contador:  # criando uma barra de

    for i in range(data_loading):  # while data_form < data_de_hj_form: # criando o while comparando o dia atual ao dia do inicio do projeto

        data_str = str(data_form)

        data_str = data_str.split(' ')[0]

        with open(f'files/produtos/{data_str}.json', 'w', encoding='utf8') as dic:  # {data_str} # criando o arquivo fora do while

            data_form = data_form + timedelta(days=x) # formula para percorrer os dias até o dia de hoje

            data_form1 = data_form + timedelta(days=1) # formula para percorrer os dias até o dia de hoje + 1

            x = +1 # variavel acumulativa

            parametros = {'limit': '100', 'start_at': f'{data_form}', 'finish_at': f'{data_form1}'} # parametros para requisição

            response = requests.get(url=url, headers=headers, params=parametros) # fazendo a requisição METODO GET

            # print(response.reason # status da requisição uma a uma caso precise

            dicionario = response.json() # criando um dicionario

            dicionario_form = dicionario['result']  # puxando apenas o resultado

            if dicionario_form != []: # if para não puxar dias nulos
                json.dump(dicionario_form, dic)
            else:
                os.remove(f'{data_str}.json')

            if response.status_code != 200: # status da requisição case de erro
                print(response.status_code) # status caso de erro
            contador.update(1) # atualizando no fim do while 1 na barra de loading
print(response.reason) #status da requisição