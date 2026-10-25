from estruturas.arvore import NoArvore, ArvoreDiagnostico

def criar_arvore_carro():
    raiz = NoArvore("Veículo")

    # 1. Motor
    motor = NoArvore("Motor")
    ignicao = NoArvore("Sistema de Ignição")
    ignicao.adicionar_filho(NoArvore("Vela", "P001", "Peça"))
    ignicao.adicionar_filho(NoArvore("Bobina", "P002", "Peça"))
    ignicao.adicionar_filho(NoArvore("Cabo de Vela", "P012", "Peça"))
    
    arrefecimento = NoArvore("Sistema de Arrefecimento")
    arrefecimento.adicionar_filho(NoArvore("Radiador", "P008", "Peça"))
    arrefecimento.adicionar_filho(NoArvore("Mangueira", "P009", "Peça"))
    arrefecimento.adicionar_filho(NoArvore("Válvula Termostática", "P013", "Peça"))
    
    motor.adicionar_filho(ignicao)
    motor.adicionar_filho(arrefecimento)
    motor.adicionar_filho(NoArvore("Correia Dentada", "P003", "Peça"))

    # 2. Transmissão
    transmissao = NoArvore("Transmissão")
    embreagem = NoArvore("Embreagem")
    embreagem.adicionar_filho(NoArvore("Disco de Embreagem", "P014", "Peça"))
    embreagem.adicionar_filho(NoArvore("Platô", "P015", "Peça"))
    cambio = NoArvore("Câmbio")
    cambio.adicionar_filho(NoArvore("Trambulador", "P016", "Peça"))
    transmissao.adicionar_filho(embreagem)
    transmissao.adicionar_filho(cambio)

    # 3. Freios
    freios = NoArvore("Freios")
    freios.adicionar_filho(NoArvore("Pastilha Dianteira", "P004", "Peça"))
    freios.adicionar_filho(NoArvore("Disco Dianteiro", "P005", "Peça"))
    freios.adicionar_filho(NoArvore("Fluido de Freio", "P017", "Peça"))

    # 4. Suspensão
    suspensao = NoArvore("Suspensão")
    suspensao.adicionar_filho(NoArvore("Amortecedor", "P006", "Peça"))
    suspensao.adicionar_filho(NoArvore("Bandeja", "P007", "Peça"))
    suspensao.adicionar_filho(NoArvore("Pivô de Suspensão", "P018", "Peça"))

    # 5. Direção
    direcao = NoArvore("Direção")
    direcao.adicionar_filho(NoArvore("Caixa de Direção", "P019", "Peça"))
    direcao.adicionar_filho(NoArvore("Terminal de Direção", "P020", "Peça"))

    # 6. Elétrico
    eletrico = NoArvore("Sistema Elétrico")
    eletrico.adicionar_filho(NoArvore("Bateria", "P010", "Peça"))
    eletrico.adicionar_filho(NoArvore("Alternador", "P011", "Peça"))
    eletrico.adicionar_filho(NoArvore("Motor de Partida", "P021", "Peça"))

    # 7. Injeção Eletrônica
    injecao = NoArvore("Injeção Eletrônica")
    injecao.adicionar_filho(NoArvore("Bico Injetor", "P022", "Peça"))
    injecao.adicionar_filho(NoArvore("Bomba de Combustível", "P023", "Peça"))
    injecao.adicionar_filho(NoArvore("Sensor de Oxigênio", "P024", "Peça"))

    # Adicionando na Raiz
    raiz.adicionar_filho(motor)
    raiz.adicionar_filho(transmissao)
    raiz.adicionar_filho(freios)
    raiz.adicionar_filho(suspensao)
    raiz.adicionar_filho(direcao)
    raiz.adicionar_filho(eletrico)
    raiz.adicionar_filho(injecao)

    return ArvoreDiagnostico(raiz)


SINTOMAS = {
    "falhando": ["P001", "P002", "P012"], 
    "engasgando": ["P001", "P002", "P024"],
    "não pega": ["P001", "P010", "P021", "P023"], 
    "nao pega": ["P001", "P010", "P021", "P023"],
    "não liga": ["P001", "P002", "P010", "P021", "P023"], # <--- NOVO AQUI
    "nao liga": ["P001", "P002", "P010", "P021", "P023"], # <--- NOVO AQUI
    "bateria": ["P010", "P011"], # <--- NOVO AQUI
    "perda de força": ["P001", "P022", "P023"],
    "cheiro de gasolina": ["P001", "P022", "P024"], "assobio": ["P003"], "correia": ["P003"],
    "superaquecendo": ["P008", "P009", "P013"], "fervendo": ["P008", "P009", "P013"],
    "água baixando": ["P008", "P009"], "fumando": ["P008", "P013"],
    "patinando": ["P014", "P015"], "marcha não engata": ["P016", "P014"], "pedal duro": ["P014", "P015"],
    "freio": ["P004", "P005", "P017"], "chiado": ["P004", "P017"], "rangido": ["P004", "P005"],
    "estalando": ["P004", "P005", "P018"], "pedal fundo": ["P017", "P008"],
    "batida seca": ["P006", "P007", "P018"], "balançando": ["P006", "P007"],
    "puxando para o lado": ["P006", "P007", "P020"], "buraco": ["P006", "P007", "P018"],
    "direção pesada": ["P019", "P020"], "folga no volante": ["P019", "P020"],
    "trepidação no volante": ["P019", "P020", "P005"], "barulho ao virar": ["P018", "P019", "P020"],
    "não acende": ["P010", "P011", "P021"], "luz fraca": ["P010", "P011"],
    "descarregando": ["P010", "P011"], "clique ao dar a partida": ["P010", "P021"],
    "falha em marcha lenta": ["P022", "P024"], "consumo alto": ["P022", "P023", "P024"],
    "cheiro forte de combustível": ["P022", "P023"]
}

def analisar_queixa(queixa_texto):
    queixa_minuscula = queixa_texto.lower()
    pecas_suspeitas = set()
    
    for sintoma, codigos in SINTOMAS.items():
        if sintoma in queixa_minuscula:
            for codigo in codigos:
                pecas_suspeitas.add(codigo)
                
    return list(pecas_suspeitas)