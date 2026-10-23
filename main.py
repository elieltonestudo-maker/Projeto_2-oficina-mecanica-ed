from banco.conexao import BancoDados
from modelos.oficina import Oficina
from estruturas.cores import Cores

def carregar_dados_iniciais(oficina):
    print("Carregando dados iniciais de teste...")
    oficina.registrar_chegada("ABC-1234", "Gabriel", "Barulho no freio quando pisa", guincho=False)
    oficina.registrar_chegada("XYZ-9876", "Elielton", "Motor falhando e engasgando", guincho=True)
    oficina.registrar_chegada("DEF-5678", "Ana", "Carro superaquecendo", guincho=False)
    print("Dados carregados com sucesso!\n")

def menu():
    db = BancoDados()
    oficina = Oficina(db)
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
        print("0. Sair")
        print("="*40)
        
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
                # Para simular, vamos puxar a queixa de um dos carros iniciais baseado no cliente
                queixa_teste = ""
                if os_atual.cliente == "Elielton": queixa_teste = "Motor falhando e engasgando"
                elif os_atual.cliente == "Gabriel": queixa_teste = "Barulho no freio"
                elif os_atual.cliente == "Ana": queixa_teste = "Carro superaquecendo"
                else: queixa_teste = "Problema não relatado"

                from modelos.diagnostico import analisar_queixa
                suspeitas = analisar_queixa(queixa_teste)
                
                print(f"\n--- ÁRVORE DE DIAGNÓSTICO (OS {os_num}) ---")
                if suspeitas:
                    print(f"Queixa relatada: '{queixa_teste}'")
                    print(f"Atenção: O sistema detectou suspeitas nos códigos {suspeitas}")
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
                codigo = input("Código da peça (ex: P001): ").upper()
                qtd = int(input("Quantidade: "))
                os_atual.adicionar_peca(codigo, qtd)
                print(f"Peça {codigo} (x{qtd}) adicionada à OS {os_num}.")
            else:
                print("OS não encontrada.")

        elif opcao == "7":
            os_num = int(input("Número da OS: "))
            forma = input("Forma de Pagamento (PIX/Cartao/Dinheiro): ")
            parcelas = 1
            if forma.lower() == "cartao":
                parcelas = int(input("Quantidade de parcelas: "))
            oficina.fechar_os_e_pagar(os_num, forma, parcelas)

        elif opcao == "8":
            print("\n--- RELATÓRIOS GERENCIAIS ---")
            mais_usado = db.relatorio_metodo_mais_usado()
            if mais_usado:
                print(f"Método mais usado: {mais_usado[0]} ({mais_usado[1]} vezes)")
            else:
                print("Nenhum pagamento registrado ainda.")
                
            print(f"Faturamento Total: R$ {db.relatorio_faturamento_total():.2f}")
            print(f"Ticket Médio: R$ {db.relatorio_ticket_medio():.2f}")
            
            print("\nTop 5 Peças Trocadas:")
            for peca, qtd in db.relatorio_principais_pecas():
                print(f" - {peca}: {qtd} unidades")
            print("-----------------------------\n")

        elif opcao == "0":
            print("Encerrando o sistema...")
            db.fechar_conexao()
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu()