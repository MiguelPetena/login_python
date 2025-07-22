import smtplib
import random
import sqlite3
from email.mime.text import MIMEText
import time

# Conexão com o banco de dados usando UTF-8
db = sqlite3.connect("../testes/login_python/usuarios.db", detect_types=sqlite3.PARSE_DECLTYPES)
db.text_factory = lambda b: b.decode("utf-8")
cursor = db.cursor()

def enviar_email(destinatario, codigo):
    remetente = "maikoncleber988@gmail.com"
    senha = "ttoj nhgy iudf xpub"
    msg = MIMEText(f"Seu código de recuperação é: {codigo}", _charset="utf-8")
    msg["Subject"] = "Recuperação de Senha"
    msg["From"] = remetente
    msg["To"] = destinatario
    try:
        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(remetente, senha)
        servidor.sendmail(remetente, destinatario, msg.as_string())
        servidor.quit()
        print("E-mail enviado!")
    except Exception as e:
        print("Erro ao enviar e-mail:", e)

def login():
    tentativas = 5
    """
    Realiza o login do usuário.
    
    Pede o login e senha ao usuário e verifica se estão corretos no banco de dados.
    Se estiverem corretos, imprime "Acesso Permitido" e sai da função.
    Se não estiverem corretos, decrementa o contador de tentativas e imprime
    "Acesso Negado! Tentativas restantes: X", onde X é o valor atual do contador.
    Se o contador chegar a 0, imprime "Número de tentativas excedido!".
    """
    while tentativas > 0:
        usuario = input("Login: ")
        senha = input("Senha: ")
        cursor.execute("SELECT * FROM usuarios WHERE login = ? AND senha = ?", (usuario, senha))
        resultado = cursor.fetchone()
        
        if resultado:
            print("Acesso Permitido")
            return
        else:
            tentativas -= 1
            print(f"Acesso Negado! Tentativas restantes: {tentativas}")
    print("Número de tentativas excedido!")

def recuperar_senha():
    usuario = input("Informe seu login: ").strip()
    
    cursor.execute("SELECT id, login FROM usuarios WHERE login = ?", (usuario,))
    resultado = cursor.fetchone()
    
    if resultado:
        usuario_id, email = resultado
        codigo = str(random.randint(100000, 999999))  # Gera um código de 6 dígitos
        expira_em = int(time.time()) + 600  # Token válido por 10 minutos
        
        # Atualizar o token e tempo de expiração no banco de dados
        cursor.execute("UPDATE usuarios SET token = ?, token_expira = ? WHERE id = ?", (codigo, expira_em, usuario_id))
        db.commit()
        
        enviar_email(email, codigo)

        # Agora, o usuário deve digitar o código recebido
        try:
            codigo_digitado = input("Digite o código recebido no e-mail: ").strip()
        except KeyboardInterrupt:
            print("\nOperação cancelada pelo usuário.")
            return
        
        cursor.execute("SELECT token, token_expira FROM usuarios WHERE id = ?", (usuario_id,))
        token_armazenado = cursor.fetchone()

        if token_armazenado:
            token, expira_em = token_armazenado
            if codigo_digitado == token and int(time.time()) < expira_em:
                nova_senha = input("Digite a nova senha: ").strip()
                cursor.execute("UPDATE usuarios SET senha = ?, token = NULL, token_expira = NULL WHERE id = ?", (nova_senha, usuario_id))
                db.commit()
                print("Senha alterada com sucesso!")
            else:
                print("Código incorreto ou expirado!")
        else:
            print("Token inválido!")
    else:
        print("Usuário não encontrado!")

# Exemplo de execução:
try:
    escolha = input("Digite 1 para Login ou 2 para Recuperação de Senha: ").strip()
    if escolha == "1":
        login()
    elif escolha == "2":
        recuperar_senha()
    else:
        print("Opção inválida!")
except KeyboardInterrupt:
    print("\nOperação cancelada pelo usuário.")

# Fechar a conexão com o banco de dados
db.close()
