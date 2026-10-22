import sqlite3

class BancoDados:
    def __init__(self, nome_arquivo="oficina.db"):
        self.conexao = sqlite3.connect(nome_arquivo)
        self.cursor = self.conexao.cursor()
        self.criar_tabelas()

    def criar_tabelas(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pagamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_os INTEGER,
                cliente TEXT,
                placa TEXT,
                mecanico TEXT,
                forma_pagamento TEXT,
                parcelas INTEGER,
                valor_pecas REAL,
                valor_mao_obra REAL,
                valor_total REAL,
                data_hora TEXT,
                garantia_dias INTEGER
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pecas_usadas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_os INTEGER,
                codigo_peca TEXT,
                nome_peca TEXT,
                quantidade INTEGER,
                valor_unitario REAL
            )
        """)
        self.conexao.commit()

    def registrar_pagamento(self, os_dados, pecas_utilizadas):
        self.cursor.execute("""
            INSERT INTO pagamentos (numero_os, cliente, placa, mecanico, forma_pagamento, 
                                    parcelas, valor_pecas, valor_mao_obra, valor_total, data_hora, garantia_dias)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (os_dados['numero_os'], os_dados['cliente'], os_dados['placa'], os_dados['mecanico'],
              os_dados['forma_pagamento'], os_dados['parcelas'], os_dados['valor_pecas'], 
              os_dados['valor_mao_obra'], os_dados['valor_total'], os_dados['data_hora'], os_dados['garantia_dias']))
        
        for peca in pecas_utilizadas:
            self.cursor.execute("""
                INSERT INTO pecas_usadas (numero_os, codigo_peca, nome_peca, quantidade, valor_unitario)
                VALUES (?, ?, ?, ?, ?)
            """, (os_dados['numero_os'], peca['codigo'], peca['nome'], peca['qtd'], peca['valor']))
        self.conexao.commit()

    def relatorio_metodo_mais_usado(self):
        self.cursor.execute("SELECT forma_pagamento, COUNT(*) as qtd FROM pagamentos GROUP BY forma_pagamento ORDER BY qtd DESC LIMIT 1")
        return self.cursor.fetchone()

    def relatorio_faturamento_total(self):
        self.cursor.execute("SELECT SUM(valor_total) FROM pagamentos")
        resultado = self.cursor.fetchone()
        return resultado[0] if resultado[0] else 0.0

    def relatorio_ticket_medio(self):
        self.cursor.execute("SELECT AVG(valor_total) FROM pagamentos")
        resultado = self.cursor.fetchone()
        return resultado[0] if resultado[0] else 0.0

    def relatorio_principais_pecas(self):
        self.cursor.execute("SELECT nome_peca, SUM(quantidade) as total FROM pecas_usadas GROUP BY nome_peca ORDER BY total DESC LIMIT 5")
        return self.cursor.fetchall()
        
    def fechar_conexao(self):
        self.conexao.close()