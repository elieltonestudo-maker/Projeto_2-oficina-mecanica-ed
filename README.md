# Sistema de Gestão de Oficina Mecânica

Projeto 2 da disciplina de Estrutura de Dados. O sistema simula o ciclo completo de uma oficina, desde a chegada do veículo até o pagamento da Ordem de Serviço (OS), utilizando estruturas de dados implementadas do zero em Python e persistência em Banco de Dados Relacional (SQLite).

## 🏗️ Arquitetura e Combinações de Estruturas

Conforme exigido no edital, o projeto implementa combinações de estruturas de dados. Abaixo estão as justificativas de projeto, indicando as classes/métodos e a desvantagem de usar uma estrutura única.

### 1. Atendimento com Prioridade (Fila + Fila)
*   **Classes/Métodos envolvidos:** `Oficina`, `Fila` (métodos `enfileirar` e `desenfileirar`).
*   **Como funciona:** O sistema possui duas filas independentes (`fila_guincho` e `fila_normal`). A cada chamada para o box, o sistema verifica a fila de guincho primeiro.
*   **Justificativa:** Garante a prioridade absoluta do guincho, mas respeita a ordem de chegada (FIFO) entre os próprios guinchos.
*   **Desvantagem de uma única estrutura:** Uma única fila exigiria reordenação a cada nova chegada de guincho (custo O(n)), quebrando a ordem de chegada original entre os prioritários.

### 2. Estoque com Lotes (Lista de Produtos + Fila de Lotes)
*   **Classes/Métodos envolvidos:** `Estoque` (classe `Produto`, classe `Lote`).
*   **Como funciona:** O estoque gerencia os produtos em uma lista. Cada produto possui uma fila de lotes ordenada pela data de compra.
*   **Justificativa:** O consumo do lote mais antigo (FIFO) é feito de forma direta. A fila garante que o lote comprado primeiro seja o primeiro a sair, evitando vencimentos.
*   **Desvantagem de uma única estrutura:** Uma lista solta de lotes exigiria varrer todos os lotes de todos os produtos para achar o mais antigo a cada baixa (custo O(n) por operação).

### 3. Clientes e Veículos (Lista de Clientes + Lista de Veículos)
*   **Classes/Métodos envolvidos:** `CadastroClientes` (classe `Cliente`, classe `Veiculo`).
*   **Como funciona:** Uma lista encadeada de clientes, onde cada nó de cliente contém outra lista encadeada de veículos.
*   **Justificativa:** Relação 1:N (um cliente, vários veículos). Permite remover um cliente e seus veículos em cascata, além de buscar por CPF ou Placa.
*   **Desvantagem de uma única estrutura:** Perderia o vínculo de propriedade (quem é o dono do carro) e a busca por CPF exigiria varrer toda a base de veículos.

### 4. Pilha (Undo da OS)
*   **Classes/Métodos envolvidos:** `OrdemServico` (método `desfazer_ultima_acao`), `Pilha`.
*   **Justificativa:** Para permitir que o mecânico desfaça a última ação (peça ou serviço) adicionada à OS.
*   **Vantagem:** O conceito LIFO (Last In, First Out) do `desempilhar()` é O(1), perfeito para um "Ctrl+Z".

### 5. Árvore N-ária (Diagnóstico)
*   **Classes/Métodos envolvidos:** `ArvoreDiagnostico` (método `percorrer_pre_ordem`), `NoArvore`.
*   **Justificativa:** O carro é uma hierarquia (Veículo -> Motor -> Ignição -> Vela). O percurso pré-ordem permite exibir o diagnóstico indentado na tela e a busca por um código de peça é feita de forma hierárquica.
*   **Desvantagem:** Uma árvore binária não representaria a realidade de um carro (um sistema pode ter 0, 1 ou N subsistemas).

---

## 🧠 Regras de Negócio Avançadas (Diferenciais do Projeto)

Além do básico exigido, o sistema implementa regras reais de mercado:

### 1. Diagnóstico Inteligente (Queixa do Cliente x Árvore)
*   O atendente registra a queixa do cliente (ex: "Não Liga").
*   O método `analisar_queixa()` (em `modelos/diagnostico.py`) varre a queixa em busca de palavras-chave e destaca na árvore as peças prováveis com o alerta `[SUSPEITA PELA QUEIXA]` (em amarelo).
*   **Vantagem:** Simula a triagem real, guiando o mecânico antes mesmo de abrir o capô.

### 2. Estoque de Teste (Peças em Uso no Carro)
*   Quando o mecânico adiciona uma peça na OS, ela **não é dada como baixa definitiva** imediatamente.
*   Ela é movida do estoque físico para uma **Lista de Estoque de Teste**.
*   Se o cliente aprovar (pagamento), a peça é removida da lista de teste (baixa definitiva).
*   **Vantagem:** Rastreabilidade exata de onde está cada peça (na prateleira ou no carro).

### 3. Controle de Vencimentos e Estoque Mínimo
*   Na abertura do sistema, uma varredura é feita no banco de dados.
*   **Lotes Vencidos:** São descartados automaticamente e registrados como prejuízo na tabela `perdas`.
*   **Estoque Mínimo:** Se a quantidade total do produto for menor que o mínimo definido, um alerta amarelo é exibido.
*   **Promoção (Perto de Vencer):** Lotes que vencem em até 60 dias geram um alerta magenta sugerindo promoção para evitar perdas.

### 4. Orçamento e Tabela de Mão de Obra
*   **Tabela de Serviços:** Os serviços de mão de obra são pré-cadastrados no SQLite (tabela `servicos`), evitando que o mecânico digite valores aleatórios.
*   **Orçamento Travado:** A OS só pode ser remontada e paga após o status mudar para `"Aguardando Aprovação"` e, em seguida, `"Aguardando Pagamento"`. Isso impede que o mecânico faça um serviço caro sem a autorização do cliente.

## 💾 Banco de Dados SQLite
O sistema utiliza a biblioteca nativa `sqlite3` para persistir os dados. O banco possui 6 tabelas:
1.  `produtos`: Catálogo de itens.
2.  `lotes`: Controle de validade e quantidade.
3.  `perdas`: Histórico de prejuízos (vencimentos).
4.  `ordens_servico`: Histórico de OSs pagas.
5.  `itens_os`: Peças usadas em cada OS.
6.  `servicos`: Tabela de preços de mão de obra.

## 🚀 Como Executar
1.  Clone o repositório.
2.  Crie e ative o ambiente virtual (`python -m venv .venv`).
3.  Execute `python main.py`.

## 📦 Dependências e Requirements
O projeto foi construído utilizando o princípio de **"Zero Dependências Externas"** para garantir a leveza e a facilidade de execução em qualquer máquina (sem a necessidade de instalar pacotes pesados via pip).

O arquivo `requirements.txt` está presente na raiz do projeto, porém não possui bibliotecas externas listadas. As únicas bibliotecas utilizadas são nativas do Python (Standard Library):
*   `sqlite3`: Para a persistência e manipulação do banco de dados relacional.
*   `datetime`: Para o controle de horários de pagamento e cálculo de datas de vencimento dos lotes.
*   `random`: Para o sorteio dos mecânicos responsáveis na abertura da OS.

## 📚 Guia de Execução
Para instruções detalhadas de como rodar e testar o sistema, consulte o arquivo [GUIA_EXECUCAO.md](GUIA_EXECUCAO.md).