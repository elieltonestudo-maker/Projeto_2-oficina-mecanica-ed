class NoPilha:
    def __init__(self, valor):
        self.valor = valor
        self.proximo = None

class Pilha:
    def __init__(self):
        self.topo = None
        self.tamanho = 0

    def empilhar(self, valor):
        novo_no = NoPilha(valor)
        novo_no.proximo = self.topo
        self.topo = novo_no
        self.tamanho += 1

    def desempilhar(self):
        if self.esta_vazia():
            return None
        valor = self.topo.valor
        self.topo = self.topo.proximo
        self.tamanho -= 1
        return valor

    def esta_vazia(self):
        return self.topo is None