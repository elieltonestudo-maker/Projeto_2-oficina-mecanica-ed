class No:
    def __init__(self, valor):
        self.valor = valor
        self.proximo = None

class Lista:
    def __init__(self):
        self.inicio = None
        self.tamanho = 0

    def inserir(self, valor):
        novo = No(valor)
        if self.inicio is None:
            self.inicio = novo
        else:
            atual = self.inicio
            while atual.proximo:
                atual = atual.proximo
            atual.proximo = novo
        self.tamanho += 1

    def percorrer(self):
        atual = self.inicio
        while atual:
            yield atual.valor
            atual = atual.proximo

    def esta_vazia(self):
        return self.inicio is None