from estruturas.fila import Fila
from modelos.os import OrdemServico
from modelos.diagnostico import criar_arvore_carro, analisar_queixa
from datetime import datetime

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
                    nova_os = OrdemServico(num_os, veiculo["placa"], veiculo["cliente"], "Mecânico Padrão")
                    self.os_abertas[num_os] = nova_os
                    box["status"] = "Ocupado"
                    box["os"] = num_os
                    
                    print(f"\n--- BOX {num_box} LIBERADO ---")
                    print(f"Chamando veículo {veiculo['placa']} para o Box {num_box}.")
                    print(f"OS {num_os} aberta. Queixa: {veiculo['queixa']}")
                    
                    pecas_suspeitas = analisar_queixa(veiculo["queixa"])
                    if pecas_suspeitas:
                        print(f"Alerta: Peças suspeitas detectadas pela queixa: {pecas_suspeitas}")
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
        if not os_atual:
            print("OS não encontrada.")
            return
        if os_atual.status != "Aguardando Pagamento":
            print("A OS ainda não foi liberada pelo mecânico.")
            return

        valor_pecas = sum([p['qtd'] * 150.0 for p in os_atual.pecas]) 
        valor_mao_obra = sum([s['valor'] for s in os_atual.servicos])
        total = valor_pecas + valor_mao_obra

        os_dados = {
            'numero_os': os_atual.numero, 'cliente': os_atual.cliente, 'placa': os_atual.placa,
            'mecanico': os_atual.mecanico, 'forma_pagamento': forma_pagamento, 'parcelas': parcelas,
            'valor_pecas': valor_pecas, 'valor_mao_obra': valor_mao_obra, 'valor_total': total,
            'data_hora': datetime.now().strftime("%Y-%m-%d %H:%M"), 'garantia_dias': 90
        }
        pecas_db = [{'codigo': p['peca'], 'nome': p['peca'], 'qtd': p['qtd'], 'valor': 150.0} for p in os_atual.pecas]
        
        self.banco.registrar_pagamento(os_dados, pecas_db)
        os_atual.status = "Fechada"
        print(f"OS {num_os} paga via {forma_pagamento}. Total: R$ {total:.2f}. Obrigado!")