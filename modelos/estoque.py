from modelos.produto import Produto, Lote
from estruturas.cores import Cores
from datetime import datetime

class Estoque:
    def __init__(self, banco):
        self.banco = banco
        self.produtos = {} 
        self.em_teste = [] # Lista de itens em teste (no carro)

    def carregar_do_banco(self):
        self.banco.cursor.execute("SELECT id, codigo, nome, categoria, preco_venda, estoque_minimo FROM produtos")
        produtos_db = self.banco.cursor.fetchall()
        
        for p in produtos_db:
            prod_id, codigo, nome, cat, preco, min_qtd = p
            novo_prod = Produto(nome, codigo, cat, preco, min_qtd)
            
            self.banco.cursor.execute("SELECT quantidade, preco_compra, data_compra, data_validade FROM lotes WHERE produto_id = ?", (prod_id,))
            lotes_db = self.banco.cursor.fetchall()
            for l in lotes_db:
                novo_lote = Lote(f"L{prod_id}", l[1], l[2], l[3], l[0]) 
                novo_prod.adicionar_lote(novo_lote)
                
            self.produtos[codigo] = novo_prod

    def verificar_alertas(self):
        print(f"\n{Cores.CIANO}--- VERIFICAÇÃO AUTOMÁTICA DE ESTOQUE ---{Cores.RESET}")
        tem_alerta = False
        
        for codigo, produto in self.produtos.items():
            perdas = produto.descartar_vencidos()
            if perdas > 0:
                print(f"{Cores.VERMELHO}[PERDA] {perdas} un. de '{produto.nome}' venceram e foram descartadas.{Cores.RESET}")
                self.banco.registrar_perda(produto.nome, perdas, "Vencimento", perdas * produto.preco_venda)
                tem_alerta = True
            
            if produto.verificar_estoque_minimo():
                print(f"{Cores.AMARELO}[ALERTA] Estoque de '{produto.nome}' abaixo do mínimo! (Atual: {produto.quantidade_total()}, Mín: {produto.estoque_minimo}){Cores.RESET}")
                tem_alerta = True
                
            tem_promocao = False
            menor_dias = 9999
            for lote in produto.fila_lotes:
                if lote.perto_de_vencer():
                    tem_promocao = True
                    if lote.dias_para_vencer() < menor_dias:
                        menor_dias = lote.dias_para_vencer()
                    
            if tem_promocao:
                print(f"{Cores.MAGENTA}[PROMOÇÃO] '{produto.nome}' possui lotes vencendo em até {menor_dias} dias. Sugerimos aplicar desconto!{Cores.RESET}")
                tem_alerta = True
                    
        if not tem_alerta:
            print(f"{Cores.VERDE}Todos os produtos estão com estoque regular e dentro da validade.{Cores.RESET}")
        print(f"{Cores.CIANO}-----------------------------------------{Cores.RESET}\n")

    def enviar_para_teste(self, codigo_produto, quantidade, numero_os):
        if codigo_produto in self.produtos:
            produto = self.produtos[codigo_produto]
            
            if produto.quantidade_total() < quantidade:
                return False, "Estoque físico insuficiente."
            
            self.em_teste.append({
                "produto": produto.nome,
                "codigo": codigo_produto,
                "quantidade": quantidade,
                "os": numero_os
            })
            return True, f"{quantidade}x {produto.nome} enviada(s) para TESTE na OS {numero_os}."
        return False, "Produto não encontrado."

    def ver_teste(self):
        if not self.em_teste:
            print(f"{Cores.VERDE}Nenhuma peça em teste no momento.{Cores.RESET}")
            return
            
        print(f"\n{Cores.CIANO}--- PEÇAS EM TESTE (NO CARRO) ---{Cores.RESET}")
        for item in self.em_teste:
            print(f"OS {item['os']} | {item['quantidade']}x {item['produto']} (Cód: {item['codigo']})")
        print(f"{Cores.CIANO}----------------------------------{Cores.RESET}")