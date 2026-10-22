import datetime

class Lote:
    def __init__(self, codigo_lote, preco_compra, data_compra, validade=None, quantidade=0):
        self.codigo_lote = codigo_lote
        self.preco_compra = preco_compra
        self.data_compra = data_compra
        self.validade = validade 
        self.quantidade = quantidade

    def esta_vencido(self):
        if not self.validade:
            return False
        hoje = datetime.date.today()
        validade_data = datetime.datetime.strptime(self.validade, "%Y-%m-%d").date()
        return validade_data < hoje

class Produto:
    def __init__(self, nome, codigo, categoria, preco_venda, estoque_minimo):
        self.nome = nome
        self.codigo = codigo
        self.categoria = categoria # "Peça" ou "Fluido"
        self.preco_venda = preco_venda
        self.estoque_minimo = estoque_minimo
        self.fila_lotes = [] 

    def adicionar_lote(self, lote):
        self.fila_lotes.append(lote)
        self.fila_lotes.sort(key=lambda l: l.data_compra)

    def quantidade_total(self):
        return sum(lote.quantidade for lote in self.fila_lotes)