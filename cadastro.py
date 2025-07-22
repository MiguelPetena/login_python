import sqlite3
import hashlib

db = sqlite3.connect("../testes/login_python/usuarios.db")
cursor = db.cursor()


def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()


def cadastrar_usuario():
    login = input(str("Digite seu login: ")).strip()
    senha = input(str("Digite sua senha: ")).strip()
    confirmar_senha = input(str("Confirme sua senha: ")).strip()

    if not login or not senha or not confirmar_senha:
        print(" Todos os campos são obrigatórios!")
        return

    if senha != confirmar_senha:
        print(" As senhas não coincidem!")
        return

    senha_hash = hash_senha(senha)  # Criptografa a senha

    try:
        cursor.execute("INSERT INTO usuarios (login, senha) VALUES ( ?, ?)", (login, senha_hash,))
        db.commit()
        print("Usuário cadastrado com sucesso!")
    except sqlite3.IntegrityError:
        print("Este login já está cadastrado!")



cadastrar_usuario()

db.close()
