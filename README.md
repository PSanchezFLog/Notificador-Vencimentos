# Notificador-Vencimentos
###### Versão 1.0
## Funcionalidade principal: App de Notificação por email dos vencimentos de licenças dos sistemas

### 1. Como utilizar:

1. Configurar um container Docker utilizando o arquivo Dockerfile como base
1. i. A configuração do container deve ter a pass trough de portas de rede (utilizar a porta padrão: 5000)
2. Após colocar para funcionar o conatiner, necessário realizar a inicialização do servidor Flask (localizado em: /flask/app.py)
3. Verificar os arquivos de venv ou configurar o arquivo main (/app/main.py) para realizar o envio de e-mails para os destinatarios desejados
4. Rodar o programa e realizar manutenções periodicas e/ou atualizações no serviço

### 2. Processo de envio de email:

O programa roda uma rotina e fica validando diariamente se existe alguma licença que está para vencer num intervalo de D-30 para que haja tempo habil de se validar a renovação ou não do serviço

### 3. Atualizações
--Por ora na versão 1.0 ainda--

### 4. Limitações:

* Ainda não foram encontradas limitações visiveis

### 5. Contato
e-mail: pedro.sanchez@fatlog.com.br
celular: (11) 91933-5693

### 6. Requisitos do Programa:

* Python 3.x
* Schedule
* Pandas
* smtplib
* MIMEText
* MIMEMultipart