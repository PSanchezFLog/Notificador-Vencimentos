# Impoortando bibliotecas
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def email_vencimento(remetente, senha, destinatario, corpo):
    # Remente: E-mail que envia
    # Senha: Senha de app do remetente
    # Destinatario: E-mail que recebe
    
    # Cria a mensagem de e-mail e o cabeçalho dela
    # Remetente, destinatario e o Assunto (está na mesma ordem aqui embaixo)
    msg = MIMEText(corpo, 'html')
    msg['From'] = remetente
    msg['To'] = ', '.join(destinatario)
    msg['Subject'] = 'As licenças da Fatelog precisam de atenção! 👀⌚'
    
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(remetente, senha)
            smtp.sendmail(remetente, destinatario, msg.as_string())
            print("E-mail enviado com sucesso!")
    except Exception as e:
        print("Erro ao enviar e-mail:", e)