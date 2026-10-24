from estruturas.fila import Fila
from modelos.os import OrdemServico
from modelos.diagnostico import criar_arvore_carro, analisar_queixa
from datetime import datetime
from estruturas.cores import Cores
import random

class Oficina:
    def __init__(self, banco_dados):
        self.banco = banco_dados
        self.fila_normal = Fila()
        self.fila_guincho = Fila()
        
        # 4 Boxes: 0 e 1 (Guincho), 2 e 3 (Normais)
        self.boxes = {
            0: {"status": "Livre", "os": None, "tipo": "Guincho"},
            1: {"status": "Livre", "os": None, "tipo": "Guincho"},
            2: {"status": "Livre", "os": None, "tipo": "Normal"},
            3: {"status": "Livre", "os": None, "tipo": "Normal"}
        }
        self.arvore_diagnostico = criar_arvore_carro()
        self.os_abertas = {} 
        self.proximo_numero_os = 1000

    def registrar_chegada(self, placa, cliente, queixa, guincho=False):
        dados = {"placa": placa, "cliente": cliente, "queixa": queixa}
        if guincho:
            self.fila_guincho.enfileirar(dados)
            print(f"Veículo {placa} (GUINCHO) na fila prioritária.")
        else:
            self.fila_normal.enfileirar(dados)
            print(f"Veículo {placa} na fila normal.")

    def chamar_proximo(self):
        for num_box, box in self.boxes.items():
            if box["status"] == "Livre":
                veiculo = None
                if not self.fila_guincho.esta_vazia():
                    veiculo = self.fila_guincho.desenfileirar()
                elif not self.fila_normal.esta_vazia():
                    veiculo = self.fila_normal.desenfileirar()
                
                if veiculo:
                    num_os = self.proximo_numero_os
                    self.proximo_numero_os += 1
                    
                    # Sorteio do mecânico responsável
                    mecanicos = ["João (Motor)", "Carlos (Suspensão)", "Ana (Elétrica)"]
                    mec_responsavel = random.choice(mecanicos)
                    
                    # Criação da OS com o mecânico sorteado
                    nova_os = OrdemServico(num_os, veiculo["placa"], veiculo["cliente"], mec_responsavel)
                    nova_os.queixa = veiculo["queixa"]
                    
                    self.os_abertas[num_os] = nova_os
                    box["status"] = "Ocupado"
                    box["os"] = num_os
                    
                    print(f"\n{Cores.AZUL}--- BOX {num_box} LIBERADO ---{Cores.RESET}")
                    print(f"Chamando veículo {Cores.NEGRITO}{veiculo['placa']}{Cores.RESET} (Cliente: {veiculo['cliente']}) para o Box {num_box}.")
                    print(f"OS {num_os} aberta. Queixa: {veiculo['queixa']}")
                    print(f"Mecânico responsável: {Cores.CIANO}{mec_responsavel}{Cores.RESET}")
                    
                    pecas_suspeitas = analisar_queixa(veiculo["queixa"])
                    if pecas_suspeitas:
                        print(f"{Cores.AMARELO}Alerta: Peças suspeitas detectadas pela queixa: {pecas_suspeitas}{Cores.RESET}")
                    return
        print("Todos os boxes estão ocupados no momento.")

    def liberar_box(self, num_box):
        if num_box in self.boxes and self.boxes[num_box]["status"] == "Ocupado":
            num_os = self.boxes[num_box]["os"]
            os_atual = self.os_abertas.get(num_os)
            if os_atual:
                os_atual.status = "Aguardando Pagamento"
                print(f"Box {num_box} liberado. OS {num_os} aguardando pagamento.")
            self.boxes[num_box]["status"] = "Livre"
            self.boxes[num_box]["os"] = None
        else:
            print(f"Box {num_box} já está livre ou não existe.")

    def fechar_os_e_pagar(self, num_os, forma_pagamento, parcelas=1):
        os_atual = self.os_abertas.get(num_os)
        
        # Cálculo de valores
        valor_pecas = sum([p['qtd'] * 150.0 for p in os_atual.pecas]) 
        valor_mao_obra = sum([s['valor'] for s in os_atual.servicos])
        total = valor_pecas + valor_mao_obra

        # 1. BAIXA DE ESTOQUE (Simulação visual)
        print("\n--- BAIXA DE ESTOQUE ---")
        for peca in os_atual.pecas:
            print(f"Baixando {peca['qtd']}x do produto {peca['peca']} do estoque físico...")
        print("Estoque atualizado com sucesso.")

        # 2. REGISTRO DO PAGAMENTO (Novo formato do Banco de Dados)
        os_dados = {
            'numero_os': os_atual.numero, 
            'cliente': os_atual.cliente, 
            'placa': os_atual.placa,
            'mecanico': os_atual.mecanico, 
            'forma_pagamento': forma_pagamento, 
            'parcelas': parcelas,
            'valor_total': total,
            'data_hora': datetime.now().strftime("%Y-%m-%d %H:%M"), 
            'garantia_dias': 90
        }
        
        # Prepara a lista de itens no formato que o banco espera
        itens_utilizados = [{'nome': p['peca'], 'qtd': p['qtd'], 'valor': 150.0} for p in os_atual.pecas]
        
        # Chama o método do banco atualizado
        self.banco.registrar_pagamento(os_dados, itens_utilizados)
        
        os_atual.status = "Fechada"
        print(f"\n{Cores.VERDE}OS {num_os} paga via {forma_pagamento} ({parcelas}x). Total: R$ {total:.2f}. Obrigado!{Cores.RESET}")