from estruturas.pilha import Pilha

class OrdemServico:
    def __init__(self, numero, placa, cliente, mecanico):
        self.numero = numero
        self.placa = placa
        self.cliente = cliente
        self.mecanico = mecanico
        self.status = "Aberta"
        self.pecas = [] 
        self.servicos = [] 
        self.historico_acoes = Pilha()

    def adicionar_peca(self, peca, quantidade):
        self.pecas.append({"peca": peca, "qtd": quantidade})
        acao = {"tipo": "add_peca", "dados": {"peca": peca, "qtd": quantidade}}
        self.historico_acoes.empilhar(acao)

    def adicionar_servico(self, descricao, valor):
        self.servicos.append({"descricao": descricao, "valor": valor})
        acao = {"tipo": "add_servico", "dados": {"descricao": descricao, "valor": valor}}
        self.historico_acoes.empilhar(acao)

    def desfazer_ultima_acao(self):
        if self.historico_acoes.esta_vazia():
            print("Nenhuma ação para desfazer.")
            return
        ultima_acao = self.historico_acoes.desempilhar()
        if ultima_acao["tipo"] == "add_peca":
            self.pecas.pop()
            print(f"Desfeito: Peça {ultima_acao['dados']['peca']} removida da OS.")
        elif ultima_acao["tipo"] == "add_servico":
            self.servicos.pop()
            print(f"Desfeito: Serviço '{ultima_acao['dados']['descricao']}' removido da OS.")