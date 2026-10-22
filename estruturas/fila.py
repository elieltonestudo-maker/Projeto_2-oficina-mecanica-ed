from estruturas.lista import Lista

class Fila:
    def __init__(self):
        self.itens = Lista()

    def enfileirar(self, valor):
        self.itens.inserir(valor)

    def desenfileirar(self):
        if self.itens.esta_vazia():
            return None
        valor = self.itens.inicio.valor
        self.itens.inicio = self.itens.inicio.proximo
        self.itens.tamanho -= 1
        return valor

    def esta_vazia(self):
        return self.itens.esta_vazia()
        
    def tamanho(self):
        return self.itens.tamanho