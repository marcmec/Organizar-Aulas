import re
from datetime import datetime, timedelta

class Aula:
    def __init__(self, tema, professor, duracao):
        self.tema = tema
        self.professor = professor
        self.duracao = duracao

    def __str__(self):
        return f"{self.tema} - {self.professor} ({self.duracao}min)"

class Bloco:
    def __init__(self, periodo, inicio, tempo_limite):
        self.periodo = periodo
        self.inicio = inicio
        self.tempo_max = tempo_limite
        self.aulas = []
        self.tempo_ocupado = 0
        self.professores_usados = set()

    def ainda_cabe(self, aula):
        return (
            self.tempo_ocupado + aula.duracao <= self.tempo_max and 
            aula.professor not in self.professores_usados
        )

    def adicionar(self, aula):
        if self.ainda_cabe(aula):
            self.aulas.append(aula)
            self.tempo_ocupado += aula.duracao
            self.professores_usados.add(aula.professor)
            return True
        return False

class DiaLetivo:
    def __init__(self, nome):
        self.nome = nome
        self.manha = Bloco("Manhã", datetime(1, 1, 1, 9, 0), 180)
        self.tarde = Bloco("Tarde", datetime(1, 1, 1, 13, 0), 240)

    def blocos(self):
        return [self.manha, self.tarde]

def interpretar_duracao(texto):
    return 5 if "lightning" in texto.lower() else int(re.sub(r'\D', '', texto))

def ler_aulas_arquivo(caminho):
    lista = []
    with open(caminho, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if not linha:
                continue
            partes = linha.rsplit(' ', 1)
            duracao = interpretar_duracao(partes[1])
            tema, prof = partes[0].rsplit(' - ', 1)
            lista.append(Aula(tema.strip(), prof.strip(), duracao))
    return lista

class GradeHoraria:
    def __init__(self, aulas):
        self.aulas = sorted(aulas, key=lambda x: -x.duracao)
        self.dias = []

    def montar_grade(self):
        agendadas = set()
        idx = 0
        nomes_dias = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira"]

        while len(agendadas) < len(self.aulas):
            if idx >= len(self.dias):
                self.dias.append(DiaLetivo(nomes_dias[idx]))

            dia = self.dias[idx]
            for aula in self.aulas:
                if aula in agendadas:
                    continue
                for bloco in dia.blocos():
                    if bloco.adicionar(aula):
                        agendadas.add(aula)
                        break
            idx += 1
        return self.dias

        
def mostrar_grade(dias):
    for dia in dias:
        print(f"📅 {dia.nome}")
        for bloco in [dia.manha, dia.tarde]:
            horario = bloco.inicio
            if not bloco.aulas:
                print(f"{horario.strftime('%H:%M')} (sem aulas disponíveis)")
            else:
                for aula in bloco.aulas:
                    tag_duracao = "lightning" if aula.duracao == 5 else f"{aula.duracao}min"
                    print(f"{horario.strftime('%H:%M')} {aula.tema} - {aula.professor} {tag_duracao}")
                    horario += timedelta(minutes=aula.duracao)

            if bloco.periodo == "Manhã":
                print("12:00 Pausa para almoço\n")
            else:
                print("17:00 Reunião dos Professores")
        print("-" * 30)
