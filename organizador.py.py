from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import re

class Aula:
    def __init__(self, titulo: str, professor: str, duracao: int):
        self.titulo = titulo
        self.professor = professor
        self.duracao = duracao  # em minutos
    
    def __str__(self):
        if self.duracao == 5:
            return f"{self.titulo} - {self.professor} lightning"
        return f"{self.titulo} - {self.professor} {self.duracao}min"

class Sessao:
    def __init__(self, tipo: str, inicio: datetime, fim: datetime):
        self.tipo = tipo  # "manhã" ou "tarde"
        self.inicio = inicio
        self.fim = fim
        self.aulas: List[Tuple[datetime, Aula]] = []
        self.professores_ocupados: Dict[str, List[Tuple[datetime, datetime]]] = {}
    
    def tempo_disponivel(self) -> int:
        """Retorna tempo disponível em minutos"""
        tempo_usado = sum(aula.duracao for _, aula in self.aulas)
        tempo_total = int((self.fim - self.inicio).total_seconds() / 60)
        return tempo_total - tempo_usado
    
    def professor_disponivel(self, professor: str, inicio: datetime, duracao: int) -> bool:
        """Verifica se professor está disponível no horário"""
        fim_aula = inicio + timedelta(minutes=duracao)
        
        if professor not in self.professores_ocupados:
            return True
        
        for inicio_ocupado, fim_ocupado in self.professores_ocupados[professor]:
            if not (fim_aula <= inicio_ocupado or inicio >= fim_ocupado):
                return False
        return True
    
    def adicionar_aula(self, aula: Aula) -> bool:
        """Tenta adicionar uma aula na sessão"""
        if self.tempo_disponivel() < aula.duracao:
            return False
        
        # Encontra próximo horário disponível
        horario_atual = self.inicio
        for _, aula_existente in sorted(self.aulas, key=lambda x: x[0]):
            horario_atual = max(horario_atual, 
                              self.aulas[self.aulas.index((_, aula_existente))][0] + 
                              timedelta(minutes=aula_existente.duracao))
        
        # Verifica se cabe no horário restante
        if horario_atual + timedelta(minutes=aula.duracao) > self.fim:
            return False
        
        # Verifica disponibilidade do professor
        if not self.professor_disponivel(aula.professor, horario_atual, aula.duracao):
            return False
        
        # Adiciona a aula
        self.aulas.append((horario_atual, aula))
        
        # Marca professor como ocupado
        if aula.professor not in self.professores_ocupados:
            self.professores_ocupados[aula.professor] = []
        
        fim_aula = horario_atual + timedelta(minutes=aula.duracao)
        self.professores_ocupados[aula.professor].append((horario_atual, fim_aula))
        
        return True

class OrganizadorHorarios:
    def __init__(self):
        self.dias = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira"]
        self.sessoes: List[List[Sessao]] = []
        self.professores_globais: Dict[str, Dict[str, List[Tuple[datetime, datetime]]]] = {}
        
        # Inicializa sessões para cada dia
        for i, dia in enumerate(self.dias):
            sessoes_dia = []
            
            # Sessão da manhã (9h às 12h)
            manha = Sessao("manhã", 
                          datetime(2025, 6, 9 + i, 9, 0),
                          datetime(2025, 6, 9 + i, 12, 0))
            
            # Sessão da tarde (13h às 17h)
            tarde = Sessao("tarde",
                          datetime(2025, 6, 9 + i, 13, 0),
                          datetime(2025, 6, 9 + i, 17, 0))
            
            sessoes_dia.extend([manha, tarde])
            self.sessoes.append(sessoes_dia)
    
    def parsear_arquivo(self, conteudo: str) -> List[Aula]:
        """Parse do arquivo de aulas"""
        aulas = []
        linhas = conteudo.strip().split('\n')
        
        for linha in linhas:
            if not linha.strip():
                continue
            
            # Regex para capturar título, professor e duração
            padrao = r'^(.+?) - (Prof\. .+?) ((?:\d+min)|(?:lightning))$'
            match = re.match(padrao, linha.strip())
            
            if match:
                titulo = match.group(1).strip()
                professor = match.group(2).strip()
                duracao_str = match.group(3).strip()
                
                if duracao_str == "lightning":
                    duracao = 5
                else:
                    duracao = int(duracao_str.replace("min", ""))
                
                aulas.append(Aula(titulo, professor, duracao))
        
        return aulas
    
    def professor_disponivel_globalmente(self, professor: str, dia_idx: int, 
                                       sessao_tipo: str, inicio: datetime, duracao: int) -> bool:
        """Verifica disponibilidade global do professor"""
        if professor not in self.professores_globais:
            self.professores_globais[professor] = {}
        
        dia_nome = self.dias[dia_idx]
        if dia_nome not in self.professores_globais[professor]:
            self.professores_globais[professor][dia_nome] = []
        
        fim_aula = inicio + timedelta(minutes=duracao)
        
        for inicio_ocupado, fim_ocupado in self.professores_globais[professor][dia_nome]:
            if not (fim_aula <= inicio_ocupado or inicio >= fim_ocupado):
                return False
        return True
    
    def organizar_aulas(self, aulas: List[Aula]) -> bool:
        """Organiza as aulas nas sessões disponíveis"""
        aulas_ordenadas = sorted(aulas, key=lambda x: x.duracao, reverse=True)
        aulas_nao_alocadas = []
        
        for aula in aulas_ordenadas:
            alocada = False
            
            # Tenta alocar em cada dia e sessão
            for dia_idx, sessoes_dia in enumerate(self.sessoes):
                if alocada:
                    break
                
                for sessao in sessoes_dia:
                    if sessao.adicionar_aula(aula):
                        # Marca professor como ocupado globalmente
                        dia_nome = self.dias[dia_idx]
                        if aula.professor not in self.professores_globais:
                            self.professores_globais[aula.professor] = {}
                        if dia_nome not in self.professores_globais[aula.professor]:
                            self.professores_globais[aula.professor][dia_nome] = []
                        
                        # Encontra horário da aula na sessão
                        for horario, aula_sessao in sessao.aulas:
                            if aula_sessao == aula:
                                fim_aula = horario + timedelta(minutes=aula.duracao)
                                self.professores_globais[aula.professor][dia_nome].append((horario, fim_aula))
                                break
                        
                        alocada = True
                        break
            
            if not alocada:
                aulas_nao_alocadas.append(aula)
        
        return len(aulas_nao_alocadas) == 0
    
    def imprimir_grade(self):
        """Imprime a grade de horários organizada"""
        for dia_idx, sessoes_dia in enumerate(self.sessoes):
            dia_nome = self.dias[dia_idx]
            
            # Verifica se há aulas no dia
            tem_aulas = any(len(sessao.aulas) > 0 for sessao in sessoes_dia)
            
            if not tem_aulas:
                continue
            
            print(f"📅 {dia_nome}:")
            
            for sessao in sessoes_dia:
                if len(sessao.aulas) == 0:
                    if sessao.tipo == "tarde":
                        print("13:00 (sem aulas disponíveis)")
                    continue
                
                # Ordena aulas por horário
                aulas_ordenadas = sorted(sessao.aulas, key=lambda x: x[0])
                
                for horario, aula in aulas_ordenadas:
                    horario_str = horario.strftime("%H:%M")
                    print(f"{horario_str} {aula}")
                
                # Adiciona intervalo para almoço após manhã
                if sessao.tipo == "manhã":
                    print("12:00 Intervalo para Almoço")
            
            print("17:00 Reunião de Professores")
            print()

def main():
    # Tenta ler arquivo externo primeiro
    conteudo_arquivo = None
    
    try:
        with open("aulas.txt", "r", encoding="utf-8") as arquivo:
            conteudo_arquivo = arquivo.read()
        print("📁 Lendo arquivo 'aulas.txt'...")
    except FileNotFoundError:
        print("📝 Arquivo 'aulas.txt' não encontrado, usando exemplo padrão...")
        # Exemplo padrão (fallback)
        conteudo_arquivo = """Introdução à IA - Prof. João 60min
Técnicas de Aprendizado Supervisionado - Prof. Ana 45min
Redes Neurais Convolucionais - Prof. João 30min
Ética na IA - Prof. Carla lightning
Linguagens de Programação Funcionais - Prof. Paulo 45min
História da Computação - Prof. Carla 30min
Banco de Dados NoSQL - Prof. Ana 60min
Lógica Computacional - Prof. Paulo 45min
Compiladores e Interpretadores - Prof. João 60min
Computação Quântica - Prof. Carla 45min
Algoritmos Avançados - Prof. Ana 60min
Programação Paralela - Prof. Paulo 30min
Pensamento Computacional - Prof. Carla 30min"""
    except Exception as e:
        print(f"❌ Erro ao ler arquivo: {e}")
        print("📝 Usando exemplo padrão...")    
    # Processa as aulas (independente da origem)
    organizador = OrganizadorHorarios()
    aulas = organizador.parsear_arquivo(conteudo_arquivo)
    
    print("🏫 Organizador de Horários de Aulas")
    print("=" * 50)
    print(f"📊 Total de aulas encontradas: {len(aulas)}")
    print()
    
    if organizador.organizar_aulas(aulas):
        print("✅ Todas as aulas foram organizadas com sucesso!")
        print()
        organizador.imprimir_grade()
    else:
        print("❌ Não foi possível organizar todas as aulas.")
        organizador.imprimir_grade()

if __name__ == "__main__":
    main()