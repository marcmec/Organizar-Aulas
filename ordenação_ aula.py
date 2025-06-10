from datetime import datetime, timedelta

def ler_propostas(nome_arquivo):
    """
    Lê o arquivo de propostas e retorna uma lista de palestras com título e duração.
    """
    propostas = []
    with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if linha.endswith("min"):
                titulo, duracao = linha.rsplit(" ", 1)
                duracao = int(duracao.replace("min", ""))
            elif linha.endswith("lightning"):
                titulo, duracao = linha.rsplit(" ", 1)
                duracao = 5  # "lightning" equivale a 5 minutos
            else:
                continue
            propostas.append((titulo, duracao))
    return propostas

def formatar_horario(horario):
    """
    Formata um objeto datetime para o formato HH:MM.
    """
    return horario.strftime("%H:%M")

def organizar_sessoes(propostas):
    """
    Organiza as palestras em sessões da manhã e da tarde, 
    respeitando as restrições de tempo.
    """
    duracao_manha = 180  # 3 horas = 180 minutos
    duracao_tarde = 240  # 4 horas = 240 minutos
    inicio_networking = datetime.strptime("16:00", "%H:%M")
    fim_networking = datetime.strptime("17:00", "%H:%M")
    
    propostas.sort(key=lambda x: x[1], reverse=True)  # Ordena as palestras por duração decrescente
    sessao_manha, sessao_tarde = [], []
    horario_atual = datetime.strptime("09:00", "%H:%M")
    
    # Preenchendo a sessão da manhã
    tempo_total = 0
    for proposta in propostas[:]:
        if tempo_total + proposta[1] <= duracao_manha:
            sessao_manha.append((horario_atual, proposta[0], proposta[1]))
            horario_atual += timedelta(minutes=proposta[1])
            tempo_total += proposta[1]
            propostas.remove(proposta)
    
    # Preenchendo a sessão da tarde
    horario_atual = datetime.strptime("13:00", "%H:%M")
    tempo_total = 0
    for proposta in propostas[:]:
        if tempo_total + proposta[1] <= duracao_tarde:
            sessao_tarde.append((horario_atual, proposta[0], proposta[1]))
            horario_atual += timedelta(minutes=proposta[1])
            tempo_total += proposta[1]
            propostas.remove(proposta)
    
    # Ajustando o horário de início do networking
    if horario_atual < inicio_networking:
        horario_networking = inicio_networking
    else:
        horario_networking = horario_atual
    
    return sessao_manha, sessao_tarde, horario_networking

def imprimir_cronograma(pista_numero, sessao_manha, sessao_tarde, horario_networking):
    """
    Imprime o cronograma formatado para uma pista (track).
    """
    print(f"Pista {pista_numero}:")
    
    for horario, titulo, duracao in sessao_manha:
        print(f"{formatar_horario(horario)} {titulo} {duracao}min")
    print("12:00 Almoço")
    
    for horario, titulo, duracao in sessao_tarde:
        print(f"{formatar_horario(horario)} {titulo} {duracao}min")
    print(f"{formatar_horario(horario_networking)} Evento de Networking\n")

def principal():
    """
    Função principal que organiza e imprime o cronograma da mini-conferência.
    """
    propostas = ler_propostas("mini_proposals.txt")
    numero_pista = 1
    while propostas:
        sessao_manha, sessao_tarde, horario_networking = organizar_sessoes(propostas)
        imprimir_cronograma(numero_pista, sessao_manha, sessao_tarde, horario_networking)
        numero_pista += 1

if __name__ == "__main__":
    principal()
