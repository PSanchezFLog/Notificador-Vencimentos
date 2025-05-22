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
lista_licenca = pd.read_excel('licencas.xlsx')
df = pd.DataFrame(lista_licenca)

# Converter a coluna Vencimento_Licenca para datetime
df['Vencimento_Licenca'] = pd.to_datetime(df['Vencimento_Licenca']).dt.date

# Itera sobre cada  item dentro da tabela
try:
    for vencimento in df['Vencimento_Licenca']:
        if vencimento > today:
            print('Ainda Okay')

        elif vencimento < today:
            print('Vencida')

        elif vencimento == today:
            print('Vencimento hoje!')

        else:
            raise Exception("ERRO! VALOR NÃO ESPERADO! CONFERIR BASE DE DADOS")
except Exception as e:
    print(e)

print(df)