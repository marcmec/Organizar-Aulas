import re
from datetime import datetime, timedelta

# Modelagem dos Dados 

class Aula:
    """Representa uma única aula com seu tema, professor e duração em minutos."""
    def __init__(self, tema, professor, duracao):
        self.tema = tema
        self.professor = professor
        self.duracao = duracao

    def __repr__(self):
        return f"Aula(Tema: {self.tema}, Prof: {self.professor}, Duração: {self.duracao}min)"

class Sessao:
    """Representa uma sessão de aulas (manhã ou tarde) em um dia."""
    def __init__(self, nome, hora_inicio, duracao_maxima):
        self.nome = nome
        self.hora_inicio = hora_inicio
        self.duracao_maxima = duracao_maxima
        self.aulas_agendadas = []
        self.tempo_utilizado = 0
        self.professores_alocados = set()

    def tempo_restante(self):
        return self.duracao_maxima - self.tempo_utilizado

    def tentar_adicionar_aula(self, aula: Aula) -> bool:
        """Tenta adicionar uma aula à sessão, se houver tempo e o professor estiver livre."""
        if aula.duracao <= self.tempo_restante() and aula.professor not in self.professores_alocados:
            self.aulas_agendadas.append(aula)
            self.tempo_utilizado += aula.duracao
            self.professores_alocados.add(aula.professor)
            return True
        return False

class Dia:
    """Representa um dia de aulas, com uma sessão de manhã e uma de tarde."""
    def __init__(self, nome):
        self.nome = nome
        self.sessao_manha = Sessao("Manhã", datetime(1, 1, 1, 9, 0), 180)  # 9h às 12h = 180 min
        self.sessao_tarde = Sessao("Tarde", datetime(1, 1, 1, 13, 0), 240) # 13h às 17h = 240 min
    
    def sessoes(self):
        return [self.sessao_manha, self.sessao_tarde]

#  Funções de Parsing e Agendamento (https://pt.stackoverflow.com/questions/99632/o-que-é-parse-e-como-funciona-o-parse-do-dom-no-html5)

def parse_duracao(duracao_str: str) -> int:
    """Converte a string de duração para minutos (ex: '60min' ou 'lightning')."""
    if duracao_str.lower() == 'lightning':
        return 5
    return int(re.sub(r'\D', '', duracao_str))

def carregar_aulas_de_arquivo(caminho_arquivo: str) -> list[Aula]:
    """Lê um arquivo de texto e o converte em uma lista de objetos Aula."""
    aulas = []
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        for linha in f:
            linha = linha.strip()
            if not linha or linha.startswith('#'):
                continue
            
            partes = linha.rsplit(' ', 1)
            duracao_str = partes[1]
            
            info_aula = partes[0].rsplit(' - ', 1)
            tema = info_aula[0].strip()
            professor = info_aula[1].strip()
            
            duracao_min = parse_duracao(duracao_str)
            aulas.append(Aula(tema, professor, duracao_min))
    return aulas

class Agenda:
    """Organiza a lista de aulas em uma grade horária."""
    def __init__(self, aulas: list[Aula]):
        # Ordenar por duração (decrescente) para encaixar as aulas maiores primeiro
        self.aulas_para_agendar = sorted(aulas, key=lambda x: x.duracao, reverse=True)
        self.dias = []

    def agendar(self):
        """Executa o processo de agendamento, alocando todas as aulas."""
        aulas_agendadas = set()

        dia_atual_idx = 0
        while len(aulas_agendadas) < len(self.aulas_para_agendar):
            # Adiciona um novo dia se necessário
            if dia_atual_idx >= len(self.dias):
                nomes_dias = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira"]
                self.dias.append(Dia(nomes_dias[dia_atual_idx]))
            
            dia_atual = self.dias[dia_atual_idx]

            # Itera sobre as aulas e tenta encaixá-las nas sessões do dia
            for aula in self.aulas_para_agendar:
                if aula in aulas_agendadas:
                    continue # Pula aulas que já foram agendadas
                
                for sessao in dia_atual.sessoes():
                    if sessao.tentar_adicionar_aula(aula):
                        aulas_agendadas.add(aula)
                        break # Aula agendada, passa para a próxima aula
            
            dia_atual_idx += 1 # Move para o próximo dia

        return self.dias

#  Função de Impressão 

def imprimir_grade(dias_agendados: list[Dia]):
    """Imprime a grade horária formatada no console."""
    if not dias_agendados:
        print("Nenhuma aula para agendar.")
        return

    for dia in dias_agendados:
        print(f"📅 {dia.nome}:")
        
        # Manhã
        hora_atual = dia.sessao_manha.hora_inicio
        if not dia.sessao_manha.aulas_agendadas:
             print(f"{hora_atual.strftime('%H:%M')} (sem aulas disponíveis)")
        else:
            for aula in dia.sessao_manha.aulas_agendadas:
                duracao_str = "lightning" if aula.duracao == 5 else f"{aula.duracao}min"
                print(f"{hora_atual.strftime('%H:%M')} {aula.tema} - {aula.professor} {duracao_str}")
                hora_atual += timedelta(minutes=aula.duracao)
        
        print("12:00 Intervalo para Almoço\n")
        
        # Tarde
        hora_atual = dia.sessao_tarde.hora_inicio
        if not dia.sessao_tarde.aulas_agendadas:
             print(f"{hora_atual.strftime('%H:%M')} (sem aulas disponíveis)")
        else:
            for aula in dia.sessao_tarde.aulas_agendadas:
                duracao_str = "lightning" if aula.duracao == 5 else f"{aula.duracao}min"
                print(f"{hora_atual.strftime('%H:%M')} {aula.tema} - {aula.professor} {duracao_str}")
                hora_atual += timedelta(minutes=aula.duracao)

        print("17:00 Reunião de Professores")
        # Adiciona uma linha em branco se não for o último dia
        if dia != dias_agendados[-1]:
            print("\n" + "---" * 10 + "\n")