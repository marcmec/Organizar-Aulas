from datetime import datetime, timedelta
import re

MANHA_INICIO = datetime.strptime("09:00", "%H:%M")
MANHA_FIM = datetime.strptime("12:00", "%H:%M")
TARDE_INICIO = datetime.strptime("13:00", "%H:%M")
TARDE_FIM = datetime.strptime("17:00", "%H:%M")

aulas_brutas = [
    "Introdução à IA - Prof. João 60min",
    "Técnicas de Aprendizado Supervisionado - Prof. Ana 45min",
    "Redes Neurais Convolucionais - Prof. João 30min",
    "Ética na IA - Prof. Carla lightning",
    "Linguagens de Programação Funcionais - Prof. Paulo 45min",
    "História da Computação - Prof. Carla 30min",
    "Banco de Dados NoSQL - Prof. Ana 60min",
    "Lógica Computacional - Prof. Paulo 45min",
    "Compiladores e Interpretadores - Prof. João 60min",
    "Computação Quântica - Prof. Carla 45min",
    "Algoritmos Avançados - Prof. Ana 60min",
    "Programação Paralela - Prof. Paulo 30min",
    "Pensamento Computacional - Prof. Carla 30min"
]

def carregar_aulas_da_lista(aulas_brutas):
    aulas = []
    for linha in aulas_brutas:
        match = re.match(r"(.+?)\s+-\s+Prof\.\s+(.+?)\s+(?:(\d+)min|lightning)", linha.strip())
        if match:
            titulo, professor, duracao = match.groups()
            duracao = 5 if duracao is None else int(duracao)
            aulas.append({'titulo': titulo, 'professor': professor, 'duracao': duracao})
    return aulas

def carregar_aulas(arquivo):
    aulas = []
    with open(arquivo, 'r', encoding='utf-8') as f:
        for linha in f:
            match = re.match(r"(.+?)\s+-\s+Prof\.\s+(.+?)\s+(?:(\d+)min|lightning)", linha.strip())
            if match:
                titulo, professor, duracao = match.groups()
                duracao = 5 if duracao is None else int(duracao)
                aulas.append({'titulo': titulo, 'professor': professor, 'duracao': duracao})
    return aulas

def alocar_aulas(aulas):
    dias = []
    nao_alocadas = aulas.copy()
    while nao_alocadas:
        dia = {'manha': [], 'tarde': [], 'ocupado_professores': {'manha': {}, 'tarde': {}}}
        nao_alocadas = alocar_sessao(nao_alocadas, dia, 'manha', MANHA_INICIO, MANHA_FIM)
        nao_alocadas = alocar_sessao(nao_alocadas, dia, 'tarde', TARDE_INICIO, TARDE_FIM)
        dias.append(dia)
    return dias

def alocar_sessao(aulas, dia, periodo, inicio, fim):
    tempo = inicio
    ocupados = dia['ocupado_professores'][periodo]
    aulas_restantes = []
    
    for aula in aulas:
        duracao = timedelta(minutes=aula['duracao'])
        
        if tempo + duracao > fim:
            aulas_restantes.append(aula)
            continue
            
        if aula['professor'] in ocupados and tempo < ocupados[aula['professor']]:
            aulas_restantes.append(aula)
            continue
            
        dia[periodo].append((tempo.strftime("%H:%M"), aula))
        tempo += duracao
        ocupados[aula['professor']] = tempo
    
    return aulas_restantes

def print_agenda(dias):
    dias_semana = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira"]
    
    for i, dia in enumerate(dias):
        print(f"{dias_semana[i]}:")
        for hora, aula in dia['manha']:
            print(f"  {hora} {aula['titulo']} - Prof. {aula['professor']} ({aula['duracao']} min)")
        
        print("  12:00 Intervalo para Almoço\n")

        for hora, aula in dia['tarde']:
            print(f"  {hora} {aula['titulo']} - Prof. {aula['professor']} ({aula['duracao']} min)")
        
        print("  17:00 Reunião de Professores\n")

if __name__ == "__main__":
    aulas = carregar_aulas_da_lista(aulas_brutas)
    agenda = alocar_aulas(aulas)
    print_agenda(agenda)