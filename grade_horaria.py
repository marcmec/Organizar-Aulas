import re
from datetime import datetime, timedelta
from collections import defaultdict

class Aula:
    def __init__(self, titulo, professor, duracao):
        self.titulo = titulo
        self.professor = professor
        self.duracao = 5 if duracao == "lightning" else int(duracao)
    
    def __str__(self):
        duracao_str = "lightning" if self.duracao == 5 else f"{self.duracao}min"
        return f"{self.titulo} - {self.professor} {duracao_str}"

class Dia:
    def __init__(self, nome):
        self.nome = nome
        self.manha = []
        self.tarde = []
        self.horario_manha_inicio = datetime.strptime("09:00", "%H:%M")
        self.horario_manha_fim = datetime.strptime("12:00", "%H:%M")
        self.horario_tarde_inicio = datetime.strptime("13:00", "%H:%M")
        self.horario_tarde_fim = datetime.strptime("17:00", "%H:%M")
    
    def adicionar_aula_manha(self, aula, horario):
        self.manha.append((horario, aula))
    
    def adicionar_aula_tarde(self, aula, horario):
        self.tarde.append((horario, aula))
    
    def __str__(self):
        output = f"📅 {self.nome}:\n"
        
        # Sessão da manhã
        current_time = self.horario_manha_inicio
        for horario, aula in sorted(self.manha, key=lambda x: x[0]):
            output += f"{horario.strftime('%H:%M')} {aula.titulo} - {aula.professor} {aula.duracao}min\n"
            current_time = horario + timedelta(minutes=aula.duracao)
        
        output += "12:00 Intervalo para Almoço\n\n"
        
        # Sessão da tarde
        current_time = self.horario_tarde_inicio
        aulas_tarde = sorted(self.tarde, key=lambda x: x[0])
        
        if not aulas_tarde:
            output += "13:00 (sem aulas disponíveis)\n"
        else:
            for horario, aula in aulas_tarde:
                output += f"{horario.strftime('%H:%M')} {aula.titulo} - {aula.professor} {aula.duracao}min\n"
                current_time = horario + timedelta(minutes=aula.duracao)
        
        output += "17:00 Reunião de Professores\n"
        return output

class GradeHoraria:
    DIAS_SEMANA = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira"]
    
    def __init__(self):
        self.dias = [Dia(nome) for nome in self.DIAS_SEMANA]
        self.professor_horarios = defaultdict(list)
    
    def alocar_aulas(self, aulas):
        for aula in sorted(aulas, key=lambda x: -x.duracao):  # Ordena por duração decrescente
            self._alocar_aula(aula)
    
    def _alocar_aula(self, aula):
        for dia in self.dias:
            # Tentar alocar na manhã
            if self._pode_alocar(dia.manha, aula, dia.horario_manha_inicio, dia.horario_manha_fim):
                horario = self._calcular_horario(dia.manha, dia.horario_manha_inicio)
                dia.adicionar_aula_manha(aula, horario)
                self.professor_horarios[aula.professor].append((dia.nome, horario, aula.duracao))
                return
            
            # Tentar alocar na tarde
            if self._pode_alocar(dia.tarde, aula, dia.horario_tarde_inicio, dia.horario_tarde_fim):
                horario = self._calcular_horario(dia.tarde, dia.horario_tarde_inicio)
                dia.adicionar_aula_tarde(aula, horario)
                self.professor_horarios[aula.professor].append((dia.nome, horario, aula.duracao))
                return
    
    def _pode_alocar(self, sessao, aula, inicio, fim):
        # Verifica se há tempo suficiente na sessão
        tempo_total = sum(a.duracao for _, a in sessao)
        tempo_disponivel = (fim - inicio).total_seconds() / 60 - tempo_total
        if aula.duracao > tempo_disponivel:
            return False
        
        # Verifica conflitos de horário para o professor
        horarios_professor = self.professor_horarios.get(aula.professor, [])
        for dia_nome, horario, duracao in horarios_professor:
            # Verifica se o professor já tem aula no mesmo dia
            if any(d.nome == dia_nome for d in self.dias if d.manha == sessao or d.tarde == sessao):
                # Verifica se há sobreposição com aulas existentes
                for h_existente, a_existente in sessao:
                    novo_horario = self._calcular_horario(sessao, inicio)
                    novo_fim = novo_horario + timedelta(minutes=aula.duracao)
                    existente_fim = h_existente + timedelta(minutes=a_existente.duracao)
                    
                    if (novo_horario < existente_fim) and (novo_fim > h_existente):
                        return False
        return True
    
    def _calcular_horario(self, sessao, inicio_sessao):
        if not sessao:
            return inicio_sessao
        
        ultima_aula_horario, ultima_aula = sessao[-1]
        return ultima_aula_horario + timedelta(minutes=ultima_aula.duracao)
    
    def __str__(self):
        return "\n".join(str(dia) for dia in self.dias)

def ler_aulas(arquivo):
    aulas = []
    padrao = re.compile(r"(.+)\s-\sProf\.\s(.+)\s(\d+|lightning)min?")
    
    with open(arquivo, 'r', encoding='utf-8') as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            
            match = padrao.match(linha)
            if match:
                titulo = match.group(1).strip()
                professor = f"Prof. {match.group(2).strip()}"
                duracao = match.group(3).strip()
                aulas.append(Aula(titulo, professor, duracao))
    
    return aulas

def main():
    try:
        aulas = ler_aulas("aulas.txt")
        grade = GradeHoraria()
        grade.alocar_aulas(aulas)
        print(grade)
    except FileNotFoundError:
        print("Erro: Arquivo 'aulas.txt' não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")

if __name__ == "__main__":
    main()