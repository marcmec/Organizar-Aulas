import re
from datetime import datetime, timedelta
from collections import defaultdict

HORARIO_MANHA = ("09:00", "12:00")
HORARIO_TARDE = ("13:00", "17:00")

MINUTOS_MANHA = 180
MINUTOS_TARDE = 240

def minutos_para_hora(base_time, minutos):
    return (datetime.strptime(base_time, "%H:%M") + timedelta(minutes=minutos)).strftime("%H:%M")

class Aula:
    def __init__(self, titulo, professor, duracao):
        self.titulo = titulo
        self.professor = professor
        self.duracao = 5 if duracao.lower() == "lightning" else int(re.sub(r"\D", "", duracao))

    def __repr__(self):
        return f"{self.titulo} - {self.professor} {self.duracao}min"

class Sessao:
    def __init__(self, tipo, hora_inicio, duracao_max):
        self.tipo = tipo
        self.hora_inicio = hora_inicio
        self.duracao_max = duracao_max
        self.horario_atual = 0
        self.aulas = []
        self.professores_ocupados = []

    def pode_alocar(self, aula):
        if self.horario_atual + aula.duracao > self.duracao_max:
            return False
        for hora, a in self.aulas:
            if a.professor == aula.professor:
                return False
        return True

    def alocar(self, aula):
        if self.pode_alocar(aula):
            hora_formatada = minutos_para_hora(self.hora_inicio, self.horario_atual)
            self.aulas.append((hora_formatada, aula))
            self.horario_atual += aula.duracao
            return True
        return False

class Dia:
    def __init__(self, nome_dia):
        self.nome = nome_dia
        self.manha = Sessao("Manhã", HORARIO_MANHA[0], MINUTOS_MANHA)
        self.tarde = Sessao("Tarde", HORARIO_TARDE[0], MINUTOS_TARDE)

    def tentar_alocar(self, aula):
        return self.manha.alocar(aula) or self.tarde.alocar(aula)

    def imprimir(self):
        print(f"\n📅 {self.nome}:")
        for sessao in [self.manha, self.tarde]:
            print()
            if not sessao.aulas:
                print(f"{sessao.hora_inicio} (sem aulas disponíveis)")
            else:
                for hora, aula in sessao.aulas:
                    print(f"{hora} {aula.titulo} - {aula.professor} {aula.duracao}min")
            if sessao.tipo == "Manhã":
                print("12:00 Intervalo para Almoço")
        print("17:00 Reunião de Professores")

def ler_aulas(arquivo):
    aulas = []
    with open(arquivo, "r", encoding="utf-8") as f:
        for linha in f:
            if linha.strip():
                match = re.match(r"(.+?) - Prof\. (.+?) (\d+min|lightning)", linha.strip())
                if match:
                    titulo, professor, duracao = match.groups()
                    aulas.append(Aula(titulo.strip(), professor.strip(), duracao.strip()))
    return aulas

def organizar_aulas(aulas):
    dias_da_semana = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira"]
    aulas_unicas = list({(a.titulo, a.professor, a.duracao): a for a in aulas}.values())
    aulas_restantes = sorted(aulas_unicas, key=lambda x: -x.duracao)
    dias = []
    dia_index = 0

    while aulas_restantes:
        if dia_index >= len(dias):
            nome = dias_da_semana[dia_index] if dia_index < len(dias_da_semana) else f"Dia Extra {dia_index + 1}"
            dias.append(Dia(nome))

        dia = dias[dia_index]
        ainda_restam = []

        for aula in aulas_restantes:
            if not dia.tentar_alocar(aula):
                ainda_restam.append(aula)

        aulas_restantes = ainda_restam
        dia_index += 1

    if aulas_restantes:
        for aula in aulas_restantes:
            for dia in dias:
                if dia.tentar_alocar(aula):
                    break 

    for dia in dias:
        dia.imprimir()

if __name__ == "__main__":
    aulas = ler_aulas("aulas.txt")
    organizar_aulas(aulas)
