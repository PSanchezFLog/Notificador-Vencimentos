# Importação de bibiliotecas
import pandas as pd
import datetime
from dotenv import load_dotenv
import os

# Carregando variaveis de ambiente
load_dotenv(r'.\.venv\.env')
remetente = os.getenv('email')
senha = os.getenv('senha')
destinatario1 = os.getenv('destinatario1')
destinatario2 = os.getenv('destinatario2')
destinatario3 = os.getenv('destinatario3')

print(destinatario1, destinatario2, destinatario3)


# Aquisição da data de hoje
today_complete = datetime.datetime.today()
today = today_complete.date()

# Aquisição da lista com as licenças
lista_licenca = pd.read_csv('licencas.csv', sep=';')
df = pd.DataFrame(lista_licenca)

# Converter a coluna Vencimento_Licenca para datetime
df['Vencimento_Licenca'] = pd.to_datetime(df['Vencimento_Licenca']).dt.date

# Contador de linhas
linhas = 0

# Itera sobre cada  item dentro da tabela
try:
    for vencimento in df['Vencimento_Licenca']:
        dias = vencimento - today
        nome_licenca = df['Nome_Licenca'].iloc[linhas]

        if dias.days > 30:
            print()
            print(nome_licenca)
            print('Ainda Okay')

        elif dias.days < 0:
            print()
            print(nome_licenca)
            print('Vencida')

        elif dias.days == 0:
            print()
            print(nome_licenca)
            print('Vencimento hoje!')

        else:
            raise Exception("ERRO! VALOR NÃO ESPERADO! CONFERIR BASE DE DADOS")
        
        linhas += 1
except Exception as e:
    print(e)
