# Funciona
# imports
import requests
from tqdm import tqdm
from datetime import datetime, timedelta, date
import json
import os
url = 'https://app.leads2b.com/api/v1/customers/list' # Url para facilitar

headers = {
    'Authorization': 'Bearer <key>'#onde está a <key> coloque a key que leads2b disponibilizou para ti
} # cabeçario da Requisição

data_ref = '2022-03-07 00:00:00' #data de ref
data_form = datetime.strptime(data_ref, '%Y-%m-%d %H:%M:%S') #formantando para o tipo: datatime


data_de_hoje = date.today().strftime('%Y-%m-%d %H:%M:%S') # data de hoje formatada
data_de_hj_form = datetime.strptime(data_de_hoje, '%Y-%m-%d %H:%M:%S') # formantando para o tipo: datatime


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

        k = x * 100

        parametros = {'limit': '100', 'updated_from': f'{data_form}', 'offset': f'{k}'}  # parametros para requisição

        x = x + 1  # variavel acumulativa

        response = requests.get(url=url, headers=headers, params=parametros)  # fazendo a requisição METODO GET
        # print(response.reason # status da requisição uma a uma caso precise

        if response.status_code != 200:  # status da requisição case de erro
            print(response.status_code)  # status caso de erro


        dicionario = response.json()  # criando um dicionario

        dicionario_form = dicionario['result']['customers']  # puxando apenas o resultado

        if dicionario_form != []:  # if para não puxar dias nulos
            with open(f'files/clientes/{i}.json', 'w',encoding='utf8') as dic:  # {data_str} # criando o arquivo fora do while
                json.dump(dicionario_form, dic)

        contador.update(1)  # atualizando no fim do while 1 na barra de loading

lista_de_arquivos = os.listdir('files/clientes/') # pegando todos os arquivos da pasta dos json

for arquivo in lista_de_arquivos: # percorrendo a variavel
    arq_bytes = os.path.getsize(f'files/clientes/{arquivo}')# pegando o tamanho de cada arquivo
    if arq_bytes <= 0:# conferindo se é 0
        os.remove(f'files/clientes/{arquivo}')#apaga o arquivo zerado

print(response.reason) #status da requisição