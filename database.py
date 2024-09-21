import sqlite3
import bcrypt

class Database:
    def __init__(self, db_name='papadobradofutebol.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        # Tabela de usuários
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password TEXT,
                nivel_acesso TEXT,
                status BOOLEAN DEFAULT 0
            )
        ''')

        # Tabela de atletas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS atletas (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                nome TEXT,
                data_nascimento DATE,
                altura REAL,
                peso REAL,
                posicao TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')

        # Tabela de atividades
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS atividades (
                id INTEGER PRIMARY KEY,
                atleta_id INTEGER,
                tipo TEXT,
                data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (atleta_id) REFERENCES atletas(id) ON DELETE CASCADE
            )
        ''')

        # Tabela de partidas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS partidas (
                id INTEGER PRIMARY KEY,
                data DATE,
                local TEXT,
                resultado TEXT
            )
        ''')

        # Tabela de presença em partidas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS presencas (
                id INTEGER PRIMARY KEY,
                partida_id INTEGER,
                atleta_id INTEGER,
                desempenho TEXT,
                FOREIGN KEY (partida_id) REFERENCES partidas(id) ON DELETE CASCADE,
                FOREIGN KEY (atleta_id) REFERENCES atletas(id) ON DELETE CASCADE
            )
        ''')

        # Tabela de materiais
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS materiais (
                id INTEGER PRIMARY KEY,
                nome TEXT,
                quantidade INTEGER
            )
        ''')

        # Tabela de cautelas de materiais
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cautelas (
                id INTEGER PRIMARY KEY,
                material_id INTEGER,
                atleta_id INTEGER,
                data_cautela TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                devolvido BOOLEAN DEFAULT 0,
                FOREIGN KEY (material_id) REFERENCES materiais(id) ON DELETE CASCADE,
                FOREIGN KEY (atleta_id) REFERENCES atletas(id) ON DELETE CASCADE
            )
        ''')

        # Tabela de pagamentos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pagamentos (
                id INTEGER PRIMARY KEY,
                atleta_id INTEGER,
                valor REAL,
                data_pagamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT,
                FOREIGN KEY (atleta_id) REFERENCES atletas(id) ON DELETE CASCADE
            )
        ''')

        # Tabela de rankings
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rankings (
                id INTEGER PRIMARY KEY,
                atleta_id INTEGER,
                pontos REAL,
                data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (atleta_id) REFERENCES atletas(id) ON DELETE CASCADE
            )
        ''')

        self.conn.commit()
        
    def verify_credentials(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute("SELECT password, status FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        if user:
            stored_password, status = user
            if status:
                return bcrypt.checkpw(password.encode('utf-8'), stored_password)
        return False

    def add_user(self, username, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor = self.conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, nivel_acesso, status) VALUES (?, ?, ?, ?)", (username, hashed_password, 'atleta', True))
            self.conn.commit()
            return {"success": True, "message": "Cadastro realizado! Solicite a aprovação do administrador."}
        except sqlite3.IntegrityError:
            return {"success": False, "message": "O nome de usuário já está em uso."}
        except Exception as e:
            return {"success": False, "message": f"Erro ao cadastrar usuário: {str(e)}"}

    def add_atleta(self, user_id, nome, data_nascimento, altura, peso, posicao):
        cursor = self.conn.cursor()
        try:
            cursor.execute("INSERT INTO atletas (user_id, nome, data_nascimento, altura, peso, posicao) VALUES (?, ?, ?, ?, ?, ?)", 
                           (user_id, nome, data_nascimento, altura, peso, posicao))
            self.conn.commit()
            return {"success": True, "message": "Atleta cadastrado com sucesso!"}
        except Exception as e:
            return {"success": False, "message": f"Erro ao cadastrar atleta: {str(e)}"}

    def add_partida(self, data, local, resultado):
        cursor = self.conn.cursor()
        try:
            cursor.execute("INSERT INTO partidas (data, local, resultado) VALUES (?, ?, ?)", 
                           (data, local, resultado))
            self.conn.commit()
            return {"success": True, "message": "Partida cadastrada com sucesso!"}
        except Exception as e:
            return {"success": False, "message": f"Erro ao cadastrar partida: {str(e)}"}

    def close(self):
        self.conn.close()
