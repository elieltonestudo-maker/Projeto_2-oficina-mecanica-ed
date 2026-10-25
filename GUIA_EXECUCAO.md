# 🚀 Guia de Execução - Sistema de Oficina Mecânica

Este documento descreve o passo a passo para executar e testar o sistema.

## 🛠️ Pré-requisitos
*   Python 3.8 ou superior instalado.
*   VS Code (ou qualquer editor de texto).
*   Git (opcional, para clonar o repositório).

## 📥 1. Preparação do Ambiente

1. Clone o repositório ou baixe os arquivos.
2. Abra o terminal na pasta raiz do projeto.
3. Crie o ambiente virtual:
   `python -m venv .venv`
4. Ative o ambiente virtual:
   - **Windows (PowerShell):** `.venv\Scripts\Activate.ps1`
   - **Windows (CMD):** `.venv\Scripts\activate.bat`
   - **Mac/Linux:** `source .venv/bin/activate`
5. (Opcional) Verifique as dependências:
   `pip install -r requirements.txt`

## 🏃 2. Executando o Sistema

Com o ambiente ativado, execute:
`python main.py`

## 🧪 3. Roteiro de Teste (Passo a Passo)

O sistema já inicia com 2 veículos nos boxes (Elielton e Gabriel) e 2 na fila (Fusca e Ana). Siga os passos para testar o fluxo completo:

1. **Verificar a Fila e os Boxes:**
   Digite `15` (Painel de Controle). Veja quem está na fila e nos boxes.
2. **Chamar os carros da fila:**
   Digite `3` duas vezes. O Fusca vai para o Box 2 (OS 1002) e a Ana para o Box 3 (OS 1003).
3. **Ver o Diagnóstico Inteligente:**
   Digite `4` e insira a OS `1002` (Fusca). Veja a árvore apontar as peças de ignição suspeitas pela queixa "Não Liga".
4. **Adicionar Peças e Mão de Obra:**
   Digite `5` (OS `1002`, código `P001`, qtd `2`).
   Digite `6` (OS `1002`, código `S004`).
5. **Gerar e Aprovar Orçamento:**
   Digite `7` e insira a OS `1002`. Veja o valor total.
   Digite `8` e aprove o orçamento.
6. **Liberar Box e Pagar:**
   Digite `9`, libere o Box `2`.
   Digite `10`, pague a OS `1002` com PIX.
7. **Ver Relatórios:**
   Digite `14` e veja o faturamento e o ranking de peças e mecânicos.   

## 📚 Guia de Execução
Para instruções detalhadas de como rodar e testar o sistema, consulte o arquivo [GUIA_EXECUCAO.md](GUIA_EXECUCAO.md).   
