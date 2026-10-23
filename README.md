# Sistema de Gestão de Oficina Mecânica

Projeto 2 da disciplina de Estrutura de Dados. O sistema simula o ciclo completo de uma oficina, desde a chegada do veículo até o pagamento da Ordem de Serviço (OS), utilizando estruturas de dados implementadas do zero em Python.

## 🏗️ Arquitetura e Combinações de Estruturas

Conforme exigido no edital, o projeto implementa combinações de estruturas de dados. Abaixo estão as justificativas de projeto.

### 1. Atendimento com Prioridade (Fila + Fila)
*   **Classes envolvidas:** `Oficina`, `Fila`.
*   **Como funciona:** O sistema possui duas filas independentes (`fila_guincho` e `fila_normal`). A cada chamada para o box, o sistema verifica a fila de guincho primeiro.
*   **Justificativa:** Garante a prioridade absoluta do guincho, mas respeita a ordem de chegada (FIFO) entre os próprios guinchos.
*   **Desvantagem de usar uma única estrutura:** Uma única fila exigiria reordenação a cada nova chegada de guincho (custo O(n)), quebrando a ordem de chegada original.

[ Chegada ]
    ├── É guincho? ── Sim ──> [ Fila Guincho ] ──> (Atendido primeiro)
    └── É guincho? ── Não ──> [ Fila Normal  ] ──> (Atendido se box livre)


### 2. Estoque com Lotes (Lista de Produtos + Fila de Lotes)
*   **Classes envolvidas:** `Estoque`, `Produto`, `Fila`, `Lote`.
*   **Como funciona:** O estoque é uma lista de produtos. Cada produto possui uma fila de lotes ordenada pela data de compra.
*   **Justificativa:** O consumo do lote mais antigo (FIFO) é feito de forma direta. A fila garante que o lote comprado primeiro seja o primeiro a sair, evitando vencimentos.
*   **Desvantagem de usar uma única estrutura:** Uma lista solta de lotes exigiria varrer todos os lotes de todos os produtos para achar o mais antigo a cada baixa (custo O(n) por operação).

[ Lista de Produtos ]
    ├── Óleo 5W30 ──> [ Fila de Lotes ] ──> Lote A (Mais antigo) ──> Lote B
    └── Vela      ──> [ Fila de Lotes ] ──> Lote C (Sem validade)


### 3. Clientes e Veículos (Lista de Clientes + Lista de Veículos)
*   **Classes envolvidas:** `CadastroClientes`, `Cliente`, `Lista`.
*   **Como funciona:** Uma lista encadeada de clientes, onde cada nó de cliente contém outra lista encadeada de veículos.
*   **Justificativa:** Relação 1:N (um cliente, vários veículos). Permite remover um cliente e seus veículos em cascata, além de buscar por CPF ou Placa.
*   **Desvantagem de usar uma única estrutura:** Perderia o vínculo de propriedade e a busca por CPF exigiria varrer toda a base de veículos.

### 4. Estrutura Adicional: Pilha (Undo da OS)
*   **Classes envolvidas:** `OrdemServico`, `Pilha`.
*   **Justificativa:** Para permitir que o mecânico desfaça a última ação (ex: adicionou a peça errada na OS).
*   **Vantagem:** O conceito LIFO (Last In, First Out) do `desempilhar()` é O(1), perfeito para "Ctrl+Z".

### 5. Estrutura Adicional: Árvore N-ária (Diagnóstico)
*   **Classes envolvidas:** `ArvoreDiagnostico`, `NoArvore`.
*   **Justificativa:** O carro é uma hierarquia (Veículo -> Motor -> Ignição -> Vela).
*   **Vantagem:** O percurso pré-ordem permite exibir o diagnóstico indentado na tela e a busca por um código de peça é feita de forma hierárquica.

## 💾 Banco de Dados SQLite
O sistema utiliza a biblioteca nativa `sqlite3` para persistir os pagamentos e as peças usadas. Isso permite a geração de relatórios gerenciais (Ticket Médio, Faturamento, Método de Pagamento mais usado, Ranking de Peças).

## 🎨 Interface Visual no Terminal (Cores ANSI)
Foi criada uma classe utilitária chamada `Cores` (no arquivo `estruturas/cores.py`) que utiliza códigos de escape ANSI nativos do Python.
*   **Justificativa:** O sistema é executado inteiramente via terminal (CLI). Para melhorar a usabilidade e a experiência do mecânico/atendente, as informações foram categorizadas por cores:
    *   **Azul:** Cabeçalhos e abertura de Boxes.
    *   **Amarelo:** Alertas de peças suspeitas na árvore de diagnóstico (baseado na queixa do cliente).
    *   **Verde:** Confirmações de sucesso (peças com estado OK, pagamentos concluídos).
    *   **Vermelho:** Mensagens de erro (não implementado visualmente em todas as telas, mas previsto na classe).
    *   **Ciano:** Destaques de nomes de mecânicos e do título do sistema.

## 🧠 Diagnóstico Inteligente (Queixa do Cliente x Árvore)
O sistema vai além de apenas imprimir a árvore de componentes. No momento em que o veículo chega, o atendente registra a queixa relatada (ex: "barulho no freio").
*   O método `analisar_queixa()` (em `modelos/diagnostico.py`) varre essa queixa em busca de palavras-chave mapeadas no dicionário `SINTOMAS`.
*   Quando a árvore é exibida na tela (Opção 5 do menu), as peças que correspondem aos sintomas relatados são automaticamente destacadas com um alerta visual em amarelo: `[SUSPEITA PELA QUEIXA]`.
*   **Vantagem:** Isso simula a triagem real de uma oficina, guiando o mecânico para os componentes mais prováveis antes mesmo de abrir o capô do carro.