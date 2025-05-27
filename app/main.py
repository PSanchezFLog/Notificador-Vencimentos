# Importação de bibiliotecas
import pandas as pd
import datetime
from dotenv import load_dotenv
import os
import app.envia_email as envia
import time
import schedule

# Carregando variaveis de ambiente
load_dotenv(r'.\.venv\.env')
remetente = os.getenv('email')
senha = os.getenv('senha')
destinatario1 = os.getenv('destinatario1')
destinatario2 = os.getenv('destinatario2')

lista_destinatarios = [destinatario1, destinatario2]


cabecalho = '''
<h2>Olá</h2>
<img src="https://www.fatelog.com.br/assets/images/design-sem-nome-2.png" alt="Logo Fatelog" style="float: right;">
<p>Bom dia, Prezados!</p>
<p>Segue abaixo as nossas licenças que estão para vencer:</p>
<ul>
'''

def rotina_licenca():
    # Aquisição da lista com as licenças
    lista_licenca = pd.read_csv('licencas.csv', sep=';')
    df = pd.DataFrame(lista_licenca)
    
    # Converter a coluna Vencimento_Licenca para datetime
    df['Vencimento_Licenca'] = pd.to_datetime(df['Vencimento_Licenca'], dayfirst= True).dt.date

    # Aquisição da data de hoje
    today_complete = datetime.datetime.today()
    today = today_complete.date()
    
    print()
    print("Executando rotina de verificação de licenças...")
    print(f"Executado dia: {today}")
    print()
    
    global cabecalho
    conteudo_email = ''
    # Faz a tentativa de abrir a lista e iterar sobre os valores dela
    try:
        
        # Itera sobre cada um dos valores da lista
        for linhas, vencimento in enumerate(df['Vencimento_Licenca']):
            dias = vencimento - today
            nome_licenca = df['Nome_Licenca'].iloc[linhas]
            valor = df['Valor'].iloc[linhas]

            if dias.days > 30: # Mais de 30 dias para vencer
                print(nome_licenca, "OK")

            elif dias.days < 0: # Já vencida
                print(nome_licenca, 'Vencida')
                conteudo_email += f'''
<li>
    <b><h3 style="color: red;">{nome_licenca}</h3></b>
    <p>Esta vencida há <b style="font-size: 20px;">{dias.days*-1}</b> dias</p>
    <p>Nossa última negociação de valores dela foi: R${valor:,.2f}</p>
</li>
                '''
            
            elif dias.days == 1: # Vencimento no dia seguinte
                print(nome_licenca, 'Vencimento amanhã!')
                conteudo_email += f'''
<li>
    <b><h3 style="color: #970a00;">{nome_licenca}</h3></b>
    <p>Esta licença irá vencer <b style="font-size: 20px;">AMANHÃ</b></p>
    <p>Nossa última negociação de valores dela foi: R${valor:,.2f}</p>
</li>
                '''            

            elif dias.days == 0: # Vence no dia
                print(nome_licenca, 'Vencimento hoje!')
                conteudo_email += f'''
<li>
    <b><h3 style="color: #970a00;">{nome_licenca}</h3></b>
    <p>Esta licença irá vencer <b style="font-size: 20px;">HOJE</b></p>
    <p>Nossa última negociação de valores dela foi: R${valor:,.2f}</p>
</li>
                '''
            
            elif dias.days < 30 and dias.days > 1: # Venciemento maior que 1 dia e menor que 30
                print(nome_licenca, f"Vence em {dias.days} dias")
                conteudo_email += f'''
<li>
    <b><h3 style="color: #540600;">{nome_licenca}</h3></b>
    <p>Esta licença irá vencer nos próximos <b style="font-size: 20px;">{dias.days}</b> dias</p>
    <p>Nossa última negociação de valores dela foi: R${valor:,.2f}</p>
</li>
                '''

            else:
                raise Exception("ERRO! VALOR NÃO ESPERADO! CONFERIR BASE DE DADOS")
            
    except Exception as e:
        print(e)
    conteudo_email += "</ul>"
    
    # Soma o conteudo do corpo do e-mail
    conteudo = cabecalho + conteudo_email
    
    # Chama a função de enviar e-mail
    envia.email_vencimento(remetente, senha, lista_destinatarios, conteudo)

# Colocando rotina no arquivo
schedule.every().day.at("14:00").do(rotina_licenca)

while True:
    schedule.run_pending()
    print('Verificando a Hora de envio!')
    time.sleep(60)