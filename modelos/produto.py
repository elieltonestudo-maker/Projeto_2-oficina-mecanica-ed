import datetime
from estruturas.cores import Cores

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