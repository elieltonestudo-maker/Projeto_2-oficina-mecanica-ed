from estruturas.cores import Cores

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

    def percorrer_pre_ordem(self, no=None, nivel=0, pecas_suspeitas=None):
        if no is None:
            no = self.raiz
        if pecas_suspeitas is None:
            pecas_suspeitas = []
        
        espacos = "    " * nivel
        codigo = f" [Cód: {no.codigo_peca}]" if no.codigo_peca else ""
        
        if no.categoria == "Peça":
            if no.codigo_peca in pecas_suspeitas:
                status = f"{Cores.AMARELO} -> ({no.estado}) [SUSPEITA PELA QUEIXA] {Cores.RESET}"
            else:
                status = f"{Cores.VERDE} -> ({no.estado}) {Cores.RESET}"
        else:
            status = ""
            
        if no.codigo_peca in pecas_suspeitas and no.categoria == "Peça":
            print(f"{espacos}- {Cores.NEGRITO}{no.nome}{Cores.RESET}{codigo}{status}")
        else:
            print(f"{espacos}- {no.nome}{codigo}{status}")

        for filho in no.filhos:
            self.percorrer_pre_ordem(filho, nivel + 1, pecas_suspeitas)
            
    def buscar_peca_por_codigo(self, no, codigo):
        if no.codigo_peca == codigo:
            return no
        for filho in no.filhos:
            resultado = self.buscar_peca_por_codigo(filho, codigo)
            if resultado:
                return resultado
        return None