from banco.conexao import BancoDados
from modelos.oficina import Oficina
from estruturas.cores import Cores
from modelos.estoque import Estoque
from datetime import datetime

def carregar_dados_iniciais(oficina):
    print("Carregando dados iniciais de teste...")
    
    oficina.registrar_chegada("ABC-1234", "Gabriel", "Civic", "Barulho no freio quando pisa", guincho=False)
    oficina.registrar_chegada("XYZ-9876", "Elielton", "Corolla", "Motor falhando e engasgando", guincho=True)
    oficina.registrar_chegada("JKL-4321", "Jaime Barbosa", "Fusca", "Não Liga", guincho=False)
    oficina.registrar_chegada("DEF-5678", "Ana", "Hilux", "Carro superaquecendo", guincho=False)
    
    for _ in range(2):
        oficina.chamar_proximo()
    
    print("Dados carregados com sucesso! (2 OSs abertas para teste)\n")

def menu():
    db = BancoDados()
    oficina = Oficina(db)
    db.popular_servicos_iniciais()
    
    estoque = Estoque(db)
    
    if not estoque.produtos:
        hoje = datetime.now().strftime("%Y-%m-%d")
        db.cadastrar_produto("O001", "Óleo Motor 5W30", "Fluido", 50.0, 10)
        db.adicionar_lote("O001", 5, 30.0, hoje, "2026-11-15")
        db.adicionar_lote("O001", 5, 30.0, hoje, "2025-01-01")
        
        pecas_teste = [
            ("P001", "Vela de Ignição", 4), ("P002", "Bobina", 4), ("P012", "Cabo de Vela", 4),
            ("P003", "Correia Dentada", 2), ("P008", "Radiador", 5), ("P009", "Mangueira", 5),
            ("P013", "Válvula Termostática", 2), ("P014", "Disco de Embreagem", 2),
            ("P015", "Platô", 2), ("P016", "Trambulador", 2), ("P004", "Pastilha Dianteira", 10),
            ("P005", "Disco Dianteiro", 5), ("P017", "Fluido de Freio", 5), ("P006", "Amortecedor", 4),
            ("P007", "Bandeja", 4), ("P018", "Pivô de Suspensão", 4), ("P019", "Caixa de Direção", 2),
            ("P020", "Terminal de Direção", 4), ("P010", "Bateria", 3), ("P011", "Alternador", 2),
            ("P021", "Motor de Partida", 2), ("P022", "Bico Injetor", 4), ("P023", "Bomba de Combustível", 2),
            ("P024", "Sensor de Oxigênio", 4)
        ]
        for cod, nome, min_qtd in pecas_teste:
            db.cadastrar_produto(cod, nome, "Peça", 150.0, min_qtd)
            db.adicionar_lote(cod, 2, 80.0, hoje, None)

    estoque.carregar_do_banco()
    estoque.verificar_alertas()
    carregar_dados_iniciais(oficina)

    while True:
        print(f"\n{Cores.CIANO}========================================{Cores.RESET}")
        print(f"{Cores.CIANO}{Cores.NEGRITO}   SISTEMA DE OFICINA MECÂNICA   {Cores.RESET}")
        print(f"{Cores.CIANO}========================================{Cores.RESET}")
        
        print(f"{Cores.NEGRITO}--- FLUXO DE ATENDIMENTO ---{Cores.RESET}")
        print("1. Registrar Chegada (Normal)")
        print("2. Registrar Chegada (Guincho)")
        print("3. Chamar Próximo para o Box")
        print("4. Ver Árvore de Diagnóstico")
        print("5. Adicionar Peça na OS")
        print("6. Adicionar Mão de Obra")
        print("7. Gerar Orçamento")
        print("8. Aprovar Orçamento")
        print("9. Liberar Box (Remontagem Concluída)")
        print("10. Fechar OS e Pagar")
        print("11. Desfazer Última Ação da OS (Undo)")
        
        print(f"\n{Cores.NEGRITO}--- GESTÃO E RELATÓRIOS ---{Cores.RESET}")
        print("12. Ver Peças em Teste (No Carro)")
        print("13. Gestão de Estoque e Compras")
        print("14. Relatórios Gerenciais (SQL)")
        print("15. Painel de Controle (Ver Fila e Boxes)")
        print("0. Sair")
        print(f"{Cores.CIANO}========================================{Cores.RESET}")
        
        opcao = input("Escolha uma opção: ")

        if opcao in ["1", "2"]:
            placa = input("Placa do veículo (ou ENTER para cancelar): ").upper()
            if not placa: continue
            cliente = input("Nome do cliente: ")
            modelo = input("Modelo do carro (ex: Civic): ")
            queixa = input("Queixa relatada: ")
            guincho = (opcao == "2")
            oficina.registrar_chegada(placa, cliente, modelo, queixa, guincho)

        elif opcao == "3":
            boxes_ocupados_antes = [b for b, info in oficina.boxes.items() if info["status"] == "Ocupado"]
            oficina.chamar_proximo()
            
            for num_box, info in oficina.boxes.items():
                if info["status"] == "Ocupado" and num_box not in boxes_ocupados_antes:
                    os_num = info["os"]
                    os_atual = oficina.os_abertas.get(os_num)
                    if os_atual:
                        if num_box in [0, 1] and not os_atual.placa.startswith("GUI"):
                            print(f"{Cores.AMARELO}Nota: O Box {num_box} é preferencial, mas foi ocupado pois a fila de guincho estava vazia.{Cores.RESET}")
                        
                        queixa = getattr(os_atual, 'queixa', "")
                        from modelos.diagnostico import analisar_queixa
                        suspeitas_codigos = analisar_queixa(queixa)
                        if suspeitas_codigos:
                            nomes_pecas = [estoque.produtos[c].nome if c in estoque.produtos else c for c in suspeitas_codigos]
                            print(f"{Cores.AMARELO}Alerta: Peças suspeitas detectadas: {', '.join(nomes_pecas)}{Cores.RESET}")
                    break
        elif opcao == "4":
            entrada = input("Digite o número da OS (ou ENTER para cancelar): ")
            if entrada.strip() == "": continue
            try:
                os_num = int(entrada)
            except ValueError:
                print(f"{Cores.VERMELHO}Erro: Digite apenas números.{Cores.RESET}")
                continue
                
            os_atual = oficina.os_abertas.get(os_num)
            if os_atual:
                queixa_teste = getattr(os_atual, 'queixa', "Problema não relatado")
                from modelos.diagnostico import analisar_queixa
                suspeitas_codigos = analisar_queixa(queixa_teste)
                
                modelo = getattr(os_atual, 'modelo_carro', 'N/A')
                print(f"\n--- ÁRVORE DE DIAGNÓSTICO (OS {os_num} - Cliente: {os_atual.cliente} | Carro: {os_atual.placa} ({modelo})) ---")
                if suspeitas_codigos:
                    nomes_suspeitos = [estoque.produtos[c].nome if c in estoque.produtos else c for c in suspeitas_codigos]
                    print(f"{Cores.AMARELO}Atenção: Suspeitas em: {', '.join(nomes_suspeitos)}{Cores.RESET}")
                else:
                    print("Nenhuma suspeita detectada pela queixa.")
                oficina.arvore_diagnostico.percorrer_pre_ordem(pecas_suspeitas=suspeitas_codigos)
                print("-----------------------------\n")
            else:
                print("OS não encontrada.")

        elif opcao == "5":
            entrada = input("Número da OS (ou ENTER para cancelar): ")
            if entrada.strip() == "": continue
            try:
                os_num = int(entrada)
            except ValueError:
                print(f"{Cores.VERMELHO}Erro: Digite apenas números.{Cores.RESET}")
                continue
                
            os_atual = oficina.os_abertas.get(os_num)
            if os_atual:
                modelo = getattr(os_atual, 'modelo_carro', 'N/A')
                print(f"\n{Cores.AZUL}--- ADICIONAR PEÇA ---{Cores.RESET}")
                print(f"OS: {os_num} | Cliente: {Cores.NEGRITO}{os_atual.cliente}{Cores.RESET} | Carro: {Cores.NEGRITO}{os_atual.placa} ({modelo}){Cores.RESET}")
                
                if os_atual.status != "Aberta":
                    print(f"{Cores.VERMELHO}Não é possível adicionar peças. A OS está {os_atual.status}.{Cores.RESET}")
                    continue

                print(f"\n{Cores.CIANO}--- CATÁLOGO DE PEÇAS ---{Cores.RESET}")
                print(f"{Cores.NEGRITO}[Motor]{Cores.RESET}")
                for cod, prod in estoque.produtos.items():
                    if cod in ["P001", "P002", "P003", "P012"]:
                        print(f"  {cod} - {prod.nome} (Estoque: {prod.quantidade_total()})")
                print(f"{Cores.NEGRITO}[Freios]{Cores.RESET}")
                for cod, prod in estoque.produtos.items():
                    if cod in ["P004", "P005", "P017"]:
                        print(f"  {cod} - {prod.nome} (Estoque: {prod.quantidade_total()})")
                print(f"{Cores.NEGRITO}[Suspensão]{Cores.RESET}")
                for cod, prod in estoque.produtos.items():
                    if cod in ["P006", "P007", "P018"]:
                        print(f"  {cod} - {prod.nome} (Estoque: {prod.quantidade_total()})")
                print(f"{Cores.NEGRITO}[Outros]{Cores.RESET}")
                for cod, prod in estoque.produtos.items():
                    if cod not in ["P001", "P002", "P003", "P012", "P004", "P005", "P017", "P006", "P007", "P018"]:
                        print(f"  {cod} - {prod.nome} (Estoque: {prod.quantidade_total()})")
                print(f"{Cores.CIANO}-------------------------------------------------------{Cores.RESET}")
                
                # --- LAÇO DE REPETIÇÃO DA PEÇA ---
                while True:
                    codigo_input = input("Digite o CÓDIGO da peça (ou ENTER para cancelar): ").upper()
                    if not codigo_input: break
                    
                    if codigo_input.isdigit():
                        codigo_formatado = "P" + codigo_input.zfill(3)
                    else:
                        codigo_formatado = codigo_input

                    if codigo_formatado not in estoque.produtos:
                        print(f"{Cores.VERMELHO}Produto não cadastrado no estoque. Tente novamente.{Cores.RESET}")
                        continue 

                    prod = estoque.produtos[codigo_formatado]
                    print(f"{Cores.VERDE}Produto selecionado: {prod.nome}{Cores.RESET}")
                    
                    try:
                        qtd_input = input("Quantidade (ou ENTER para cancelar): ")
                        if not qtd_input: break
                        qtd = int(qtd_input)
                        if qtd <= 0:
                            print(f"{Cores.VERMELHO}A quantidade deve ser maior que zero.{Cores.RESET}")
                            continue
                    except ValueError:
                        print(f"{Cores.VERMELHO}Erro: Você digitou uma letra. Digite apenas números inteiros.{Cores.RESET}")
                        continue

                    confirmacao = input(f"{Cores.AMARELO}Confirmar envio de {Cores.NEGRITO}{qtd}x {codigo_formatado} - {prod.nome}{Cores.RESET}{Cores.AMARELO} para a OS {os_num}? (S/N): {Cores.RESET}").upper()
                    
                    if confirmacao == "S":
                        sucesso, mensagem = estoque.enviar_para_teste(codigo_formatado, qtd, os_num)
                        if sucesso:
                            os_atual.adicionar_peca(codigo_formatado, qtd)
                            print(f"{Cores.VERDE}Peça adicionada com sucesso!{Cores.RESET}")
                            for item in estoque.em_teste:
                                print(f"OS {item['os']} | {item['quantidade']}x {item['codigo']} - {item['produto']}")
                            break 
                        else:
                            print(f"{Cores.VERMELHO}Erro: {mensagem}{Cores.RESET}")
                            break 
                    else:
                        print("Ação cancelada.")
                        break 
            else:
                print("OS não encontrada.")

        elif opcao == "6":
            entrada = input("Número da OS (ou ENTER para cancelar): ")
            if entrada.strip() == "": continue
            try:
                os_num = int(entrada)
            except ValueError:
                print(f"{Cores.VERMELHO}Erro: Digite apenas números.{Cores.RESET}")
                continue

            os_atual = oficina.os_abertas.get(os_num)
            if os_atual:
                modelo = getattr(os_atual, 'modelo_carro', 'N/A')
                print(f"\n{Cores.AZUL}--- ADICIONAR MÃO DE OBRA ---{Cores.RESET}")
                print(f"OS: {os_num} | Cliente: {Cores.NEGRITO}{os_atual.cliente}{Cores.RESET} | Carro: {Cores.NEGRITO}{os_atual.placa} ({modelo}){Cores.RESET}")
                
                if os_atual.status != "Aberta":
                    print(f"{Cores.VERMELHO}Não é possível adicionar serviços. A OS está {os_atual.status}.{Cores.RESET}")
                    continue
                
                print(f"\n{Cores.CIANO}--- TABELA DE SERVIÇOS ---{Cores.RESET}")
                servicos_db = db.buscar_servicos()
                for s in servicos_db:
                    print(f"{s[0]} - {s[1]}: R$ {s[2]:.2f}")
                
                # --- LAÇO DE REPETIÇÃO DO SERVIÇO ---
                while True:
                    cod_servico = input("Digite o CÓDIGO do serviço (ou ENTER para cancelar): ").upper()
                    if not cod_servico: break
                        
                    encontrado = next((s for s in servicos_db if s[0] == cod_servico), None)
                    
                    if encontrado:
                        confirmacao = input(f"{Cores.AMARELO}Confirmar adição do serviço '{encontrado[1]}' (R$ {encontrado[2]:.2f}) à OS {os_num}? (S/N): {Cores.RESET}").upper()
                        if confirmacao == "S":
                            os_atual.adicionar_servico(encontrado[1], encontrado[2])
                            print(f"{Cores.VERDE}Serviço adicionado com sucesso!{Cores.RESET}")
                            break 
                        else:
                            print("Ação cancelada.")
                            break 
                    else:
                        print(f"{Cores.VERMELHO}Código inválido! Tente novamente.{Cores.RESET}")
            else:
                print("OS não encontrada.")

        elif opcao == "7":
            entrada = input("Número da OS para gerar orçamento (ou ENTER para cancelar): ")
            if entrada.strip() == "": continue
            try:
                os_num = int(entrada)
            except ValueError:
                print(f"{Cores.VERMELHO}Erro: Digite apenas números.{Cores.RESET}")
                continue
                
            os_atual = oficina.os_abertas.get(os_num)
            if not os_atual:
                print("OS não encontrada.")
                continue

            modelo = getattr(os_atual, 'modelo_carro', 'N/A')
            print(f"\n{Cores.NEGRITO}=== ORÇAMENTO - OS {os_num} ==={Cores.RESET}")
            print(f"Cliente: {os_atual.cliente} | Carro: {os_atual.placa} ({modelo})")
            
            print(f"\n{Cores.NEGRITO}Peças:{Cores.RESET}")
            valor_pecas = 0
            for p in os_atual.pecas:
                cod = p['peca']
                qtd = p['qtd']
                nome_peca = estoque.produtos[cod].nome if cod in estoque.produtos else cod
                
                if cod in estoque.produtos:
                    valor_peca, tem_desconto = estoque.produtos[cod].calcular_preco_com_desconto(qtd)
                    if tem_desconto:
                        print(f"  - {qtd}x {nome_peca} (R$ {estoque.produtos[cod].preco_venda:.2f}) -> {Cores.MAGENTA}[DESCONTO 20% APLICADO] R$ {valor_peca:.2f}{Cores.RESET}")
                    else:
                        print(f"  - {qtd}x {nome_peca}: R$ {valor_peca:.2f}")
                else:
                    valor_peca = qtd * 150.0
                    print(f"  - {qtd}x {nome_peca}: R$ {valor_peca:.2f}")
                valor_pecas += valor_peca
                
            print(f"\n{Cores.NEGRITO}Serviços:{Cores.RESET}")
            valor_mao_obra = 0
            for s in os_atual.servicos:
                print(f"  - {s['descricao']}: R$ {s['valor']:.2f}")
                valor_mao_obra += s['valor']
                
            print(f"\n{Cores.NEGRITO}Total Estimado: R$ {valor_pecas + valor_mao_obra:.2f}{Cores.RESET}")
            
            os_atual.status = "Aguardando Aprovação"
            print(f"{Cores.AMARELO}Status: {os_atual.status}{Cores.RESET}")

        elif opcao == "8":
            entrada = input("Número da OS para aprovar (ou ENTER para cancelar): ")
            if entrada.strip() == "": continue
            try:
                os_num = int(entrada)
            except ValueError:
                print(f"{Cores.VERMELHO}Erro: Digite apenas números.{Cores.RESET}")
                continue
                
            os_atual = oficina.os_abertas.get(os_num)
            if os_atual:
                if os_atual.status == "Aguardando Aprovação":
                    confirmacao = input(f"{Cores.AMARELO}O cliente {os_atual.cliente} aprovou o orçamento da OS {os_num}? (S/N): {Cores.RESET}").upper()
                    if confirmacao == "S":
                        os_atual.status = "Aguardando Pagamento"
                        print(f"{Cores.VERDE}Orçamento APROVADO!{Cores.RESET}")
                    else:
                        print("Ação cancelada.")
                else:
                    print(f"{Cores.VERMELHO}Status atual: {os_atual.status}{Cores.RESET}")
            else:
                print("OS não encontrada.")

        elif opcao == "9":
            print(f"\n{Cores.CIANO}--- MAPA DOS BOXES ---{Cores.RESET}")
            
            for num, info in oficina.boxes.items():
                if info["status"] == "Ocupado":
                    os_num = info["os"]
                    os_atual = oficina.os_abertas.get(os_num)
                    if os_atual:
                        modelo = getattr(os_atual, 'modelo_carro', 'N/A')
                        
                        if os_atual.status == "Aberta":
                            status_cor = f"{Cores.VERDE}Em Execução{Cores.RESET}"
                        elif os_atual.status == "Aguardando Aprovação":
                            status_cor = f"{Cores.AMARELO}Aguardando Aprovação{Cores.RESET}"
                        elif os_atual.status == "Aguardando Pagamento":
                            status_cor = f"{Cores.CIANO}Pronto p/ Pagto{Cores.RESET}"
                        else:
                            status_cor = os_atual.status
                            
                        print(f"Box {num}: Ocupado | OS {os_num} | {os_atual.placa} ({modelo}) - {os_atual.cliente}")
                        print(f"       Status da OS: {status_cor}")
                else:
                    print(f"Box {num}: {Cores.VERDE}Livre{Cores.RESET}")
            print(f"{Cores.CIANO}----------------------{Cores.RESET}")

            entrada = input("Digite o Número do Box que deseja liberar (ou ENTER para cancelar): ")
            if entrada.strip() == "":
                print("Ação cancelada. Voltando ao menu...")
                continue
                
            try:
                box = int(entrada)
            except ValueError:
                print(f"{Cores.VERMELHO}Erro: Digite apenas números.{Cores.RESET}")
                continue
                
            if box in oficina.boxes and oficina.boxes[box]["status"] == "Ocupado":
                num_os = oficina.boxes[box]["os"]
                os_atual = oficina.os_abertas.get(num_os)
                if os_atual:
                    if os_atual.status != "Aguardando Pagamento":
                        print(f"{Cores.VERMELHO}Erro: A OS {num_os} está '{os_atual.status}'. Gere e aprove o orçamento primeiro.{Cores.RESET}")
                        continue
                    
                    modelo = getattr(os_atual, 'modelo_carro', 'N/A')
                    confirmacao = input(f"{Cores.AMARELO}Remontagem do Box {box} (OS {num_os} | Cliente: {os_atual.cliente} | Carro: {os_atual.placa}) concluída? (S/N): {Cores.RESET}").upper()
                    if confirmacao == "S":
                        oficina.liberar_box(box)
                else:
                    print("OS não encontrada no Box.")
            else:
                print("Box já está livre ou inválido.")

        elif opcao == "10":
            entrada = input("Número da OS (ou ENTER para cancelar): ")
            if entrada.strip() == "": continue
            try:
                os_num = int(entrada)
            except ValueError:
                print(f"{Cores.VERMELHO}Erro: Digite apenas números.{Cores.RESET}")
                continue
                
            os_atual = oficina.os_abertas.get(os_num)
            if not os_atual:
                print("OS não encontrada.")
                continue
            if os_atual.status != "Aguardando Pagamento":
                print(f"{Cores.VERMELHO}A OS não está aguardando pagamento (Status: {os_atual.status}).{Cores.RESET}")
                continue

            modelo = getattr(os_atual, 'modelo_carro', 'N/A')
            print(f"\n{Cores.NEGRITO}--- RESUMO DA OS {os_num} ---{Cores.RESET}")
            print(f"Cliente: {os_atual.cliente} | Carro: {os_atual.placa} ({modelo}) | Mecânico: {os_atual.mecanico}")
            
            print(f"{Cores.NEGRITO}Peças:{Cores.RESET}")
            valor_pecas = 0
            for p in os_atual.pecas:
                cod = p['peca']
                qtd = p['qtd']
                nome_peca = estoque.produtos[cod].nome if cod in estoque.produtos else cod
                
                if cod in estoque.produtos:
                    valor_peca, tem_desconto = estoque.produtos[cod].calcular_preco_com_desconto(qtd)
                    if tem_desconto:
                        print(f"  - {qtd}x {nome_peca} (R$ {estoque.produtos[cod].preco_venda:.2f}) -> {Cores.MAGENTA}[DESCONTO 20% APLICADO] R$ {valor_peca:.2f}{Cores.RESET}")
                    else:
                        print(f"  - {qtd}x {nome_peca}: R$ {valor_peca:.2f}")
                else:
                    valor_peca = qtd * 150.0
                    print(f"  - {qtd}x {nome_peca}: R$ {valor_peca:.2f}")
                valor_pecas += valor_peca
                
            print(f"{Cores.NEGRITO}Mão de Obra:{Cores.RESET}")
            valor_mao_obra = 0
            for s in os_atual.servicos:
                print(f"  - {s['descricao']}: R$ {s['valor']:.2f}")
                valor_mao_obra += s['valor']
            
            total = valor_pecas + valor_mao_obra
            print(f"\n{Cores.NEGRITO}Total a Pagar: R$ {total:.2f}{Cores.RESET}")
            
            print("\n--- FORMA DE PAGAMENTO ---")
            print("1. PIX\n2. Cartão\n3. Dinheiro")
            escolha_pgto = input("Escolha (1-3) ou ENTER para cancelar: ")
            if escolha_pgto.strip() == "": continue
            
            if escolha_pgto == "1": forma, parcelas = "PIX", 1
            elif escolha_pgto == "2": 
                try:
                    parcelas = int(input("Parcelas: "))
                except ValueError:
                    print(f"{Cores.VERMELHO}Erro: Digite apenas números.{Cores.RESET}")
                    continue
                forma = "Cartão"
            elif escolha_pgto == "3": forma, parcelas = "Dinheiro", 1
            else: 
                print(f"{Cores.VERMELHO}Opção inválida.{Cores.RESET}")
                continue 
            
            oficina.fechar_os_e_pagar(os_num, forma, parcelas, total) # Passamos o total calculado
            estoque.em_teste = [item for item in estoque.em_teste if item["os"] != os_num]
            print(f"{Cores.VERDE}OS {os_num} paga. Peças removidas do estoque de teste.{Cores.RESET}")

        elif opcao == "11":
            entrada = input("Número da OS para desfazer (ou ENTER para cancelar): ")
            if entrada.strip() == "": continue
            try:
                os_num = int(entrada)
            except ValueError:
                print(f"{Cores.VERMELHO}Erro: Digite apenas números.{Cores.RESET}")
                continue
                
            os_atual = oficina.os_abertas.get(os_num)
            if os_atual:
                if os_atual.historico_acoes.esta_vazia():
                    print(f"{Cores.VERMELHO}Não há ações para desfazer.{Cores.RESET}")
                    continue
                ultima_acao = os_atual.historico_acoes.topo.valor
                
                if ultima_acao["tipo"] == "add_peca":
                    cod = ultima_acao["dados"]["peca"]
                    qtd = ultima_acao["dados"]["qtd"]
                    nome = estoque.produtos[cod].nome if cod in estoque.produtos else cod
                    descricao = f"{Cores.NEGRITO}{qtd}x {cod} - {nome}{Cores.RESET}"
                elif ultima_acao["tipo"] == "add_servico":
                    descricao = f"{Cores.NEGRITO}{ultima_acao['dados']['descricao']}{Cores.RESET}"
                
                confirmacao = input(f"{Cores.AMARELO}Desfazer a adição de {descricao} para a OS {os_num}? (S/N): {Cores.RESET}").upper()
                
                if confirmacao == "S":
                    if ultima_acao["tipo"] == "add_peca":
                        codigo_peca = ultima_acao["dados"]["peca"]
                        for i in range(len(estoque.em_teste) - 1, -1, -1):
                            if estoque.em_teste[i]["os"] == os_num and estoque.em_teste[i]["codigo"] == codigo_peca:
                                estoque.em_teste.pop(i)
                                break
                    
                    os_atual.desfazer_ultima_acao()
                    print(f"{Cores.VERDE}Peça removida da OS.{Cores.RESET}")
                    estoque.ver_teste()
                else:
                    print("Ação cancelada.")
            else:
                print("OS não encontrada.") 

        elif opcao == "12":
            estoque.ver_teste()

        elif opcao == "13":
            print("\n--- GESTÃO DE ESTOQUE ---")
            print("1. Cadastrar Novo Produto")
            print("2. Repor Estoque (Adicionar Lote)")
            print("3. Relatório de Estoque Mínimo/Promoções")
            print("4. Relatório de Perdas")
            print("0. Voltar ao Menu Principal")
            sub_opcao = input("Escolha: ")
            
            if sub_opcao == "0":
                continue

            if sub_opcao == "1":
                cod = input("Código (ou ENTER para cancelar): ").upper()
                if not cod: continue
                nome = input("Nome: ")
                cat = input("Categoria (Peça/Fluido): ")
                try:
                    preco_input = input("Preço de Venda: R$ ")
                    if not preco_input: continue
                    preco = float(preco_input)
                    min_qtd_input = input("Estoque Mínimo: ")
                    if not min_qtd_input: continue
                    min_qtd = int(min_qtd_input)
                except ValueError:
                    print(f"{Cores.VERMELHO}Erro: Preço ou quantidade inválidos.{Cores.RESET}")
                    continue
                if db.cadastrar_produto(cod, nome, cat, preco, min_qtd):
                    print(f"{Cores.VERDE}Produto cadastrado!{Cores.RESET}")
                    estoque.carregar_do_banco()
                else:
                    print(f"{Cores.VERMELHO}Código já existe.{Cores.RESET}")
                    
            elif sub_opcao == "2":
                cod_input = input("Código do Produto (ou ENTER para cancelar): ").upper()
                if not cod_input: continue
                cod = "P" + cod_input.zfill(3) if not cod_input.startswith("P") else cod_input
                if cod in estoque.produtos:
                    produto = estoque.produtos[cod]
                    print(f"{Cores.VERDE}Produto: {produto.nome} | Estoque Atual: {produto.quantidade_total()}{Cores.RESET}")
                    try:
                        qtd_input = input("Quantidade a adicionar: ")
                        if not qtd_input: continue
                        qtd = int(qtd_input)
                        preco_compra_input = input("Preço de Compra: R$ ")
                        if not preco_compra_input: continue
                        preco_compra = float(preco_compra_input)
                    except ValueError:
                        print(f"{Cores.VERMELHO}Erro: Digite apenas números.{Cores.RESET}")
                        continue
                    validade = input("Validade (AAAA-MM-DD) ou ENTER para nenhuma: ")
                    if validade == "": validade = None
                    hoje = datetime.now().strftime("%Y-%m-%d")
                    if db.adicionar_lote(cod, qtd, preco_compra, hoje, validade):
                        print(f"{Cores.VERDE}Lote adicionado!{Cores.RESET}")
                        estoque.carregar_do_banco()
                else:
                    print(f"{Cores.VERMELHO}Produto não cadastrado!{Cores.RESET}")
                    
            elif sub_opcao == "3":
                estoque.verificar_alertas()
                
            elif sub_opcao == "4":
                db.cursor.execute("SELECT produto_nome, SUM(quantidade), SUM(prejuizo_financeiro) FROM perdas GROUP BY produto_nome")
                perdas = db.cursor.fetchall()
                print(f"\n{Cores.NEGRITO}--- RELATÓRIO DE PERDAS ---{Cores.RESET}")
                if not perdas: print("Nenhuma perda registrada.")
                for p in perdas: print(f"{p[0]} | Qtd: {p[1]} | Prejuízo: R$ {p[2]:.2f}")

        elif opcao == "14":
            print("\n--- RELATÓRIOS GERENCIAIS ---")
            mais_usado = db.relatorio_metodo_mais_usado()
            if mais_usado:
                print(f"Método mais usado: {Cores.VERDE}{mais_usado[0]}{Cores.RESET} ({mais_usado[1]} vezes)")
            else:
                print("Nenhum pagamento registrado ainda.")
            print(f"Faturamento Total: R$ {db.relatorio_faturamento_total():.2f}")
            print(f"Ticket Médio: R$ {db.relatorio_ticket_medio():.2f}")
            
            print("\nTop 5 Peças Trocadas:")
            pecas = db.relatorio_principais_pecas()
            if not pecas: print("Nenhuma peça registrada.")
            for peca, qtd in pecas: print(f" - {peca}: {qtd} unidades")

            print("\nDesempenho dos Mecânicos:")
            mecanicos = db.relatorio_mecanicos()
            if not mecanicos: print("Nenhuma OS fechada por mecânicos ainda.")
            for mec, qtd, total in mecanicos: print(f" - {mec}: {qtd} OS(s) | Faturamento: R$ {total:.2f}")
            print("-----------------------------\n")

        elif opcao == "15":
            print(f"\n{Cores.NEGRITO}========= PAINEL DE CONTROLE ========={Cores.RESET}")
            
            print(f"{Cores.CIANO}--- BOXES ---{Cores.RESET}")
            for num_box, box in oficina.boxes.items():
                tipo = "Guincho" if num_box in [0, 1] else "Normal"
                if box["status"] == "Ocupado":
                    os_atual = oficina.os_abertas.get(box["os"])
                    if os_atual:
                        modelo = getattr(os_atual, 'modelo_carro', 'N/A')
                        print(f"Box {num_box} ({tipo}): {Cores.AMARELO}Ocupado{Cores.RESET} | OS {box['os']} | {os_atual.placa} ({modelo}) - {os_atual.cliente}")
                else:
                    print(f"Box {num_box} ({tipo}): {Cores.VERDE}Livre{Cores.RESET}")

            print(f"\n{Cores.CIANO}--- FILA DE ESPERA ---{Cores.RESET}")
            print(f"{Cores.NEGRITO}[Guincho]{Cores.RESET}")
            if oficina.fila_guincho.esta_vazia():
                print("  (Vazia)")
            else:
                atual = oficina.fila_guincho.itens.inicio
                while atual:
                    v = atual.valor
                    print(f"  {v['placa']} ({v['modelo']}) - {v['cliente']}")
                    atual = atual.proximo
                    
            print(f"{Cores.NEGRITO}[Normal]{Cores.RESET}")
            if oficina.fila_normal.esta_vazia():
                print("  (Vazia)")
            else:
                atual = oficina.fila_normal.itens.inicio
                while atual:
                    v = atual.valor
                    print(f"  {v['placa']} ({v['modelo']}) - {v['cliente']}")
                    atual = atual.proximo
                    
            print(f"{Cores.NEGRITO}======================================{Cores.RESET}\n")

        elif opcao == "0":
            print("Encerrando...")
            db.fechar_conexao()
            break
        else:
            print(f"{Cores.VERMELHO}Opção inválida!{Cores.RESET}")

if __name__ == "__main__":
    menu()