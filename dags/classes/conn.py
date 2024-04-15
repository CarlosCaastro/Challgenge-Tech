import mysql.connector


class Conexao:
    def __init__(self, host, usuario, senha, banco):
        self.host = host
        self.usuario = usuario
        self.senha = senha
        self.banco = banco
        self.conexao = None

    def conectar(self):
        try:
            self.conexao = mysql.connector.connect(
                host=self.host,
                user=self.usuario,
                password=self.senha,
                database=self.banco,
            )
            print("Conexão estabelecida.")
            return self.conexao

        except mysql.connector.Error as erro:
            print(f"Erro ao conectar ao banco de dados: {erro}")
            return None

    def executar_sql(self, sql):
        try:
            cursor = self.conexao.cursor()
            cursor.execute(sql)
            print("Comando SQL executado com sucesso.")
        except mysql.connector.Error as erro:
            print(f"Erro ao executar o comando SQL: {erro}")

    def fechar_conexao(self):
        if self.conexao:
            self.conexao.close()
            print("Conexão fechada.")
        else:
            print("Não há nenhuma conexão para fechar.")
