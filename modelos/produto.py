import datetime

class Lote:
    def __init__(self, codigo_lote, preco_compra, data_compra, validade=None, quantidade=0):
        self.codigo_lote = codigo_lote
        self.preco_compra = preco_compra
        self.data_compra = data_compra
        self.validade = validade 
        self.quantidade = quantidade

    def dias_para_vencer(self):
        if not self.validade:
            return 9999 # Não vence
        hoje = datetime.date.today()
        validade_data = datetime.datetime.strptime(self.validade, "%Y-%m-%d").date()
        return (validade_data - hoje).days

    def esta_vencido(self):
        return self.dias_para_vencer() < 0

    def perto_de_vencer(self):
        # Retorna True se faltar 60 dias ou menos para vencer
        dias = self.dias_para_vencer()
        return 0 <= dias <= 60


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
        # Ordena para o lote mais antigo ficar sempre no início
        self.fila_lotes.sort(key=lambda l: l.data_compra)

    def quantidade_total(self):
        return sum(lote.quantidade for lote in self.fila_lotes)

    def verificar_estoque_minimo(self):
        return self.quantidade_total() < self.estoque_minimo

    def descartar_vencidos(self):
        perdas = 0
        for lote in self.fila_lotes:
            if lote.esta_vencido() and lote.quantidade > 0:
                perdas += lote.quantidade
                lote.quantidade = 0 # Zera o lote para não ser usado
        return perdas