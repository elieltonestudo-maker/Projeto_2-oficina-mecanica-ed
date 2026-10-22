class NoArvore:
    def __init__(self, nome, codigo_peca=None, categoria="Sistema"):
        self.nome = nome
        self.codigo_peca = codigo_peca
        self.categoria = categoria # "Sistema", "Subsistema", "Peça"
        self.estado = "OK"
        self.filhos = [] # Lista interna simples do Python

    def adicionar_filho(self, filho):
        self.filhos.append(filho)

class ArvoreDiagnostico:
    def __init__(self, raiz):
        self.raiz = raiz

    def percorrer_pre_ordem(self, no=None, nivel=0):
        if no is None:
            no = self.raiz
        
        espacos = "    " * nivel
        codigo = f" [Cód: {no.codigo_peca}]" if no.codigo_peca else ""
        status = f" -> ({no.estado})" if no.categoria == "Peça" else ""
        
        print(f"{espacos}- {no.nome}{codigo}{status}")

        for filho in no.filhos:
            self.percorrer_pre_ordem(filho, nivel + 1)
            
    def buscar_peca_por_codigo(self, no, codigo):
        if no.codigo_peca == codigo:
            return no
        for filho in no.filhos:
            resultado = self.buscar_peca_por_codigo(filho, codigo)
            if resultado:
                return resultado
        return None