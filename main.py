from banco.conexao import BancoDados
from modelos.oficina import Oficina
from estruturas.cores import Cores
from modelos.estoque import Estoque
from datetime import datetime

def carregar_dados_iniciais(oficina):
    print("Carregando dados iniciais de teste...")
    oficina.registrar_chegada("ABC-1234", "Gabriel", "Barulho no freio quando pisa", guincho=False)
    oficina.registrar_chegada("XYZ-9876", "Elielton", "Motor falhando e engasgando", guincho=True)
    oficina.registrar_chegada("DEF-5678", "Ana", "Carro superaquecendo", guincho=False)
    print("Dados carregados com sucesso!\n")

def menu():
    db = BancoDados()
    oficina = Oficina(db)
    
    # Inicializa o Estoque
    estoque = Estoque(db)
    
    # --- POPULANDO O BANCO PARA TESTE (Só roda se o banco estiver vazio) ---
    if not estoque.produtos:
        db.cadastrar_produto("O001", "Óleo Motor 5W30", "Fluido", 50.0, 10)
        hoje = datetime.now().strftime("%Y-%m-%d")
        db.adicionar_lote("O001", 5, 30.0, hoje, "2026-11-15") # Perto de vencer
        db.adicionar_lote("O001", 5, 30.0, hoje, "2025-01-01") # Já venceu
        
        db.cadastrar_produto("P001", "Vela de Ignição", "Peça", 150.0, 4)
        db.adicionar_lote("P001", 2, 80.0, hoje, None) # Estoque baixo (2 < 4)

    # Carrega do banco para a memória e checa alertas automaticamente
    estoque.carregar_do_banco()
    estoque.verificar_alertas()
    
    carregar_dados_iniciais(oficina)

    while True:
        print(f"{Cores.CIANO}========================================{Cores.RESET}")
        print(f"{Cores.CIANO}{Cores.NEGRITO}   SISTEMA DE OFICINA MECÂNICA   {Cores.RESET}")
        print(f"{Cores.CIANO}========================================{Cores.RESET}")
        print("1. Registrar Chegada (Normal)")
        print("2. Registrar Chegada (Guincho)")
        print("3. Chamar Próximo para o Box")
        print("4. Liberar Box (Remontagem Concluída)")
        print("5. Ver Árvore de Diagnóstico")
        print("6. Adicionar Peça na OS")
        print("7. Fechar OS e Pagar")
        print("8. Relatórios Gerenciais (SQL)")
        print("9. Gestão de Estoque e Compras")
        print("10. Ver Peças em Teste (No Carro)")
        print("0. Sair")
        print(f"{Cores.CIANO}========================================{Cores.RESET}")
        
        opcao = input("Escolha uma opção: ")

        if opcao in ["1", "2"]:
            placa = input("Placa do veículo: ").upper()
            cliente = input("Nome do cliente: ")
            queixa = input("Queixa relatada: ")
            guincho = (opcao == "2")
            oficina.registrar_chegada(placa, cliente, queixa, guincho)

        elif opcao == "3":
            oficina.chamar_proximo()

        elif opcao == "4":
            box = int(input("Número do Box a liberar (0 a 3): "))
            oficina.liberar_box(box)

        elif opcao == "5":
            os_num = int(input("Digite o número da OS que deseja ver o diagnóstico: "))
            os_atual = oficina.os_abertas.get(os_num)
            
            if os_atual:
                queixa_teste = getattr(os_atual, 'queixa', "Problema não relatado")

                from modelos.diagnostico import analisar_queixa
                suspeitas = analisar_queixa(queixa_teste)
                
                print(f"\n--- ÁRVORE DE DIAGNÓSTICO (OS {os_num}) ---")
                if suspeitas:
                    print(f"Queixa relatada: '{queixa_teste}'")
                    print(f"{Cores.AMARELO}Atenção: O sistema detectou suspeitas nos códigos {suspeitas}{Cores.RESET}")
                else:
                    print("Nenhuma suspeita detectada pela queixa.")
                    
                oficina.arvore_diagnostico.percorrer_pre_ordem(pecas_suspeitas=suspeitas)
                print("-----------------------------\n")
            else:
                print("OS não encontrada.")

        elif opcao == "6":
            os_num = int(input("Número da OS: "))
            os_atual = oficina.os_abertas.get(os_num)
            if os_atual:
                codigo_input = input("Código da peça (ex: P001 ou 001): ").upper()
                
                # Formata o código automaticamente
                if not codigo_input.startswith("P"):
                    codigo_formatado = "P" + codigo_input.zfill(3)
                else:
                    codigo_formatado = codigo_input

                qtd = int(input("Quantidade: "))
                
                # Chama a função do Estoque 
                sucesso, mensagem = estoque.enviar_para_teste(codigo_formatado, qtd, os_num)
                
                if sucesso:
                    os_atual.adicionar_peca(codigo_formatado, qtd)
                    print(f"{Cores.VERDE}{mensagem}{Cores.RESET}")
                    # Mostra o painel do estoque de teste
                    estoque.ver_teste() 
                else:
                    print(f"{Cores.VERMELHO}Erro: {mensagem}{Cores.RESET}")
            else:
                print("OS não encontrada.")

        elif opcao == "7":
            os_num = int(input("Número da OS: "))
            os_atual = oficina.os_abertas.get(os_num)
            if not os_atual:
                print("OS não encontrada.")
                continue
            if os_atual.status != "Aguardando Pagamento":
                print("A OS ainda não foi liberada pelo mecânico.")
                continue

            print(f"\n{Cores.NEGRITO}--- RESUMO DA OS {os_num} ---{Cores.RESET}")
            print(f"Cliente: {os_atual.cliente}")
            print(f"Placa: {os_atual.placa}")
            print(f"Mecânico: {os_atual.mecanico}")
            
            valor_pecas = sum([p['qtd'] * 150.0 for p in os_atual.pecas])
            valor_mao_obra = sum([s['valor'] for s in os_atual.servicos])
            print(f"Total a Pagar: R$ {valor_pecas + valor_mao_obra:.2f}")
            print(f"{Cores.NEGRITO}------------------------{Cores.RESET}")
            
            print("\n--- FORMA DE PAGAMENTO ---")
            print("1. PIX")
            print("2. Cartão de Crédito/Débito")
            print("3. Dinheiro")
            escolha_pgto = input("Escolha a forma de pagamento (1-3): ")
            
            if escolha_pgto == "1":
                forma = "PIX"
                parcelas = 1
            elif escolha_pgto == "2":
                forma = "Cartão"
                parcelas = int(input("Quantidade de parcelas (1 para à vista): "))
            elif escolha_pgto == "3":
                forma = "Dinheiro"
                parcelas = 1
            else:
                print(f"{Cores.VERMELHO}Opção inválida.{Cores.RESET}")
                continue 
            
            # 1. Registra o pagamento
            oficina.fechar_os_e_pagar(os_num, forma, parcelas)
            
            # 2. NOVO TRECHO: Remove as peças da lista de teste
            estoque.em_teste = [item for item in estoque.em_teste if item["os"] != os_num]
            print(f"{Cores.VERDE}Peças da OS {os_num} removidas do estoque de teste (aprovadas).{Cores.RESET}")

        elif opcao == "8":
            print("\n--- RELATÓRIOS GERENCIAIS ---")
            mais_usado = db.relatorio_metodo_mais_usado()
            if mais_usado:
                print(f"Método mais usado: {Cores.VERDE}{mais_usado[0]}{Cores.RESET} ({mais_usado[1]} vezes)")
            else:
                print("Nenhum pagamento registrado ainda.")
                
            print(f"Faturamento Total: R$ {db.relatorio_faturamento_total():.2f}")
            print(f"Ticket Médio: R$ {db.relatorio_ticket_medio():.2f}")
            
            print("\nTop 5 Peças Trocadas:")
            for peca, qtd in db.relatorio_principais_pecas():
                print(f" - {peca}: {qtd} unidades")
            print("-----------------------------\n")

        elif opcao == "9":
            print("\n--- GESTÃO DE ESTOQUE ---")
            print("1. Cadastrar Novo Produto")
            print("2. Repor Estoque (Adicionar Lote)")
            print("3. Relatório de Estoque Mínimo/Promoções")
            print("4. Relatório de Perdas")
            sub_opcao = input("Escolha: ")
            
            if sub_opcao == "1":
                cod = input("Código: ").upper()
                nome = input("Nome: ")
                cat = input("Categoria (Peça/Fluido): ")
                preco = float(input("Preço de Venda: R$ "))
                min_qtd = int(input("Estoque Mínimo: "))
                if db.cadastrar_produto(cod, nome, cat, preco, min_qtd):
                    print(f"{Cores.VERDE}Produto cadastrado!{Cores.RESET}")
                    estoque.carregar_do_banco()
                else:
                    print(f"{Cores.VERMELHO}Código já existe.{Cores.RESET}")
                    
            elif sub_opcao == "2":
                cod_input = input("Código do Produto: ").upper()
                
                # Padroniza o código
                if not cod_input.startswith("P"):
                    cod = "P" + cod_input.zfill(3)
                else:
                    cod = cod_input

                # Verifica se o produto existe ANTES de pedir os dados do lote
                if cod in estoque.produtos:
                    produto = estoque.produtos[cod]
                    print(f"{Cores.VERDE}Produto encontrado: {produto.nome} | Estoque Atual: {produto.quantidade_total()} unidades.{Cores.RESET}")
                    
                    qtd = int(input("Quantidade a adicionar no Lote: "))
                    preco_compra = float(input("Preço de Compra Unitário: R$ "))
                    validade = input("Data de Validade (AAAA-MM-DD) ou ENTER para nenhuma: ")
                    if validade == "": validade = None
                    
                    hoje = datetime.now().strftime("%Y-%m-%d")
                    if db.adicionar_lote(cod, qtd, preco_compra, hoje, validade):
                        print(f"{Cores.VERDE}Lote adicionado ao produto {cod}! Novo estoque: {produto.quantidade_total() + qtd}{Cores.RESET}")
                        estoque.carregar_do_banco() # Recarrega a memória
                else:
                    print(f"{Cores.VERMELHO}Produto não cadastrado no sistema!{Cores.RESET}")
                    
            elif sub_opcao == "3":
                estoque.verificar_alertas()
                
            elif sub_opcao == "4":
                db.cursor.execute("SELECT produto_nome, SUM(quantidade), SUM(prejuizo_financeiro) FROM perdas GROUP BY produto_nome")
                perdas = db.cursor.fetchall()
                print(f"\n{Cores.NEGRITO}--- RELATÓRIO DE PERDAS ---{Cores.RESET}")
                if not perdas:
                    print("Nenhuma perda registrada.")
                for p in perdas:
                    print(f"Produto: {p[0]} | Qtd Perdida: {p[1]} | Prejuízo: R$ {p[2]:.2f}")

        elif opcao == "10":
            estoque.ver_teste()

        elif opcao == "0":
            print("Encerrando o sistema...")
            db.fechar_conexao()
            break
        else:
            print(f"{Cores.VERMELHO}Opção inválida!{Cores.RESET}")

if __name__ == "__main__":
    menu()