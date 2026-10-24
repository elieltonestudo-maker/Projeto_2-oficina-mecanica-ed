import sqlite3
from datetime import datetime

class BancoDados:
    def __init__(self, nome_arquivo="oficina.db"):
        self.conexao = sqlite3.connect(nome_arquivo)
        self.cursor = self.conexao.cursor()
        self.criar_tabelas()

    def criar_tabelas(self):
        # 1. Produtos
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT UNIQUE,
                nome TEXT,
                categoria TEXT,
                preco_venda REAL,
                estoque_minimo INTEGER
            )
        """)
        
        # 2. Lotes
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS lotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_id INTEGER,
                quantidade INTEGER,
                preco_compra REAL,
                data_compra TEXT,
                data_validade TEXT,
                FOREIGN KEY(produto_id) REFERENCES produtos(id)
            )
        """)
        
        # 3. Perdas
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS perdas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_nome TEXT,
                quantidade INTEGER,
                motivo TEXT,
                data_perda TEXT,
                prejuizo_financeiro REAL
            )
        """)
        
        # 4. Ordens de Serviço
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS ordens_servico (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_os INTEGER,
                cliente TEXT,
                placa TEXT,
                mecanico TEXT,
                forma_pagamento TEXT,
                parcelas INTEGER,
                valor_total REAL,
                data_hora TEXT,
                garantia_dias INTEGER
            )
        """)
        
        # 5. Itens da OS
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS itens_os (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_os INTEGER,
                produto_nome TEXT,
                quantidade INTEGER,
                preco_unitario REAL
            )
        """)
        
        self.conexao.commit()

    # --- MÉTODOS DE ESTOQUE ---
    def cadastrar_produto(self, codigo, nome, categoria, preco_venda, estoque_minimo):
        try:
            self.cursor.execute("""
                INSERT INTO produtos (codigo, nome, categoria, preco_venda, estoque_minimo)
                VALUES (?, ?, ?, ?, ?)
            """, (codigo, nome, categoria, preco_venda, estoque_minimo))
            self.conexao.commit()
            return True
        except sqlite3.IntegrityError:
            return False # Produto já existe

    def adicionar_lote(self, codigo_produto, quantidade, preco_compra, data_compra, data_validade):
        self.cursor.execute("SELECT id FROM produtos WHERE codigo = ?", (codigo_produto,))
        produto = self.cursor.fetchone()
        if produto:
            self.cursor.execute("""
                INSERT INTO lotes (produto_id, quantidade, preco_compra, data_compra, data_validade)
                VALUES (?, ?, ?, ?, ?)
            """, (produto[0], quantidade, preco_compra, data_compra, data_validade))
            self.conexao.commit()
            return True
        return False

    def registrar_perda(self, produto_nome, quantidade, motivo, prejuizo):
        agora = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.cursor.execute("""
            INSERT INTO perdas (produto_nome, quantidade, motivo, data_perda, prejuizo_financeiro)
            VALUES (?, ?, ?, ?, ?)
        """, (produto_nome, quantidade, motivo, agora, prejuizo))
        self.conexao.commit()

    def buscar_produtos_estoque_baixo(self):
        # Soma a quantidade de todos os lotes e compara com o estoque_minimo
        self.cursor.execute("""
            SELECT p.nome, p.estoque_minimo, COALESCE(SUM(l.quantidade), 0) as qtd_atual
            FROM produtos p
            LEFT JOIN lotes l ON p.id = l.produto_id
            GROUP BY p.id
            HAVING qtd_atual < p.estoque_minimo
        """)
        return self.cursor.fetchall()

    # --- MÉTODOS DE PAGAMENTO E RELATÓRIOS ---
    def registrar_pagamento(self, os_dados, itens_utilizados):
        # Salva a OS
        self.cursor.execute("""
            INSERT INTO ordens_servico (numero_os, cliente, placa, mecanico, forma_pagamento, 
                                        parcelas, valor_total, data_hora, garantia_dias)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (os_dados['numero_os'], os_dados['cliente'], os_dados['placa'], os_dados['mecanico'],
              os_dados['forma_pagamento'], os_dados['parcelas'], os_dados['valor_total'], 
              os_dados['data_hora'], os_dados['garantia_dias']))
        
        # Salva os itens
        for item in itens_utilizados:
            self.cursor.execute("""
                INSERT INTO itens_os (numero_os, produto_nome, quantidade, preco_unitario)
                VALUES (?, ?, ?, ?)
            """, (os_dados['numero_os'], item['nome'], item['qtd'], item['valor']))
            
        self.conexao.commit()

    def relatorio_metodo_mais_usado(self):
        self.cursor.execute("SELECT forma_pagamento, COUNT(*) as qtd FROM ordens_servico GROUP BY forma_pagamento ORDER BY qtd DESC LIMIT 1")
        return self.cursor.fetchone()

    def relatorio_faturamento_total(self):
        self.cursor.execute("SELECT SUM(valor_total) FROM ordens_servico")
        resultado = self.cursor.fetchone()
        return resultado[0] if resultado[0] else 0.0

    def relatorio_ticket_medio(self):
        self.cursor.execute("SELECT AVG(valor_total) FROM ordens_servico")
        resultado = self.cursor.fetchone()
        return resultado[0] if resultado[0] else 0.0

    def relatorio_principais_pecas(self):
        self.cursor.execute("SELECT produto_nome, SUM(quantidade) as total FROM itens_os GROUP BY produto_nome ORDER BY total DESC LIMIT 5")
        return self.cursor.fetchall()
        
    def fechar_conexao(self):
        self.conexao.close()