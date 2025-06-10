import re
from datetime import datetime, timedelta

class Disciplina:
    """Representa uma disciplina com seus dados."""
    def __init__(self, materia, docente, carga_horaria):
        self.materia = materia
        self.docente = docente
        self.carga_horaria = carga_horaria

    def __repr__(self):
        return f"Disciplina({self.materia}, Docente: {self.docente}, Carga: {self.carga_horaria}min)"

class BlocoAulas:
    """Representa um bloco de aulas (manhã/tarde)."""
    def __init__(self, nome, inicio, duracao_max):
        self.nome = nome
        self.inicio = inicio
        self.duracao_max = duracao_max
        self.disciplinas = []
        self.tempo_ocupado = 0
        self.docentes_alocados = set()

    def tempo_disponivel(self):
        return self.duracao_max - self.tempo_ocupado

    def alocar_disciplina(self, disciplina: Disciplina) -> bool:
        """Tenta alocar uma disciplina no bloco."""
        if (disciplina.carga_horaria <= self.tempo_disponivel() 
            and disciplina.docente not in self.docentes_alocados):
            self.disciplinas.append(disciplina)
            self.tempo_ocupado += disciplina.carga_horaria
            self.docentes_alocados.add(disciplina.docente)
            return True
        return False

class DiaLetivo:
    """Representa um dia de aulas com dois blocos."""
    def __init__(self, nome):
        self.nome = nome
        self.manha = BlocoAulas("Manhã", datetime(1, 1, 1, 9, 0), 180)
        self.tarde = BlocoAulas("Tarde", datetime(1, 1, 1, 13, 0), 240)
    
    def blocos(self):
        return [self.manha, self.tarde]

def converter_carga_horaria(carga_str: str) -> int:
    """Converte a string de carga horária para minutos."""
    return 5 if carga_str.lower() == 'lightning' else int(re.sub(r'\D', '', carga_str))

def carregar_disciplinas(arquivo: str) -> list[Disciplina]:
    """Carrega disciplinas de um arquivo."""
    disciplinas = []
    with open(arquivo, 'r', encoding='utf-8') as f:
        for linha in f:
            linha = linha.strip()
            if not linha or linha.startswith('#'):
                continue
            
            partes = linha.rsplit(' ', 1)
            carga_str = partes[1]
            
            info = partes[0].rsplit(' - ', 1)
            disciplina = Disciplina(
                info[0].strip(),
                info[1].strip(),
                converter_carga_horaria(carga_str)
            )
            disciplinas.append(disciplina)
    return disciplinas

class GradeHoraria:
    """Organiza as disciplinas em uma grade."""
    def __init__(self, disciplinas: list[Disciplina]):
        self.disciplinas = sorted(disciplinas, key=lambda x: x.carga_horaria, reverse=True)
        self.dias = []

    def organizar(self):
        """Gera o cronograma."""
        disciplinas_alocadas = set()
        dias_semana = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira"]
        
        while len(disciplinas_alocadas) < len(self.disciplinas):
            if len(self.dias) >= len(dias_semana):
                break
                
            dia = DiaLetivo(dias_semana[len(self.dias)])
            
            for disciplina in self.disciplinas:
                if disciplina in disciplinas_alocadas:
                    continue
                    
                for bloco in dia.blocos():
                    if bloco.alocar_disciplina(disciplina):
                        disciplinas_alocadas.add(disciplina)
                        break
            
            self.dias.append(dia)
        
        return self.dias

def exibir_cronograma(dias: list[DiaLetivo]):
    """Exibe o cronograma formatado."""
    for dia in dias:
        print(f"\n📅 {dia.nome}:")
        
        # Bloco da manhã
        hora = dia.manha.inicio
        for disciplina in dia.manha.disciplinas:
            carga = "lightning" if disciplina.carga_horaria == 5 else f"{disciplina.carga_horaria}min"
            print(f"{hora.strftime('%H:%M')} {disciplina.materia} - {disciplina.docente} {carga}")
            hora += timedelta(minutes=disciplina.carga_horaria)
        
        print("12:00 Intervalo para Almoço")
        
        # Bloco da tarde
        hora = dia.tarde.inicio
        for disciplina in dia.tarde.disciplinas:
            carga = "lightning" if disciplina.carga_horaria == 5 else f"{disciplina.carga_horaria}min"
            print(f"{hora.strftime('%H:%M')} {disciplina.materia} - {disciplina.docente} {carga}")
            hora += timedelta(minutes=disciplina.carga_horaria)
        
        print("17:00 Reunião Docente")