import sys
import re
from datetime import datetime, timedelta
from collections import defaultdict

class Aula:
    def __init__(self, titulo, professor, duracao):
        self.titulo = titulo
        self.professor = professor
        self.duracao = duracao  

class Sessao:
    def __init__(self, tipo, inicio, fim):
        self.tipo = tipo
        self.inicio = inicio
        self.fim = fim
        self.aulas = []
        self.tempo_usado = 0

    def tempo_disponivel(self):
        return int((self.fim - self.inicio).total_seconds() / 60) - self.tempo_usado

class Dia:
    def __init__(self, nome):
        self.nome = nome
        self.manha = Sessao('manha', datetime.strptime('09:00', '%H:%M'), datetime.strptime('12:00', '%H:%M'))
        self.tarde = Sessao('tarde', datetime.strptime('13:00', '%H:%M'), datetime.strptime('17:00', '%H:%M'))


def ler_arquivo_aulas(caminho):
    aulas = []
    padrao = re.compile(r'^(.*?)\s*-\s*Prof\.?\s(.*?)\s(\d+min|lightning)$')
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            for i, linha in enumerate(f, 1):
                linha = linha.strip()
                if not linha:
                    continue
                m = padrao.match(linha)
                if not m:
                    raise ValueError(f"Erro na linha {i}: Formato inválido: '{linha}'\nEsperado: <Título> - Prof. <Nome> <Duração>")
                titulo = m.group(1).strip()
                professor = f"Prof. {m.group(2).strip()}"
                duracao_txt = m.group(3)
                duracao = 5 if duracao_txt == 'lightning' else int(duracao_txt.replace('min', ''))
                aulas.append(Aula(titulo, professor, duracao))
        if not aulas:
            raise ValueError("O arquivo está vazio ou contém apenas linhas inválidas.")
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo '{caminho}' não encontrado.")
    except Exception as e:
        raise e
    return aulas

def alocar_aulas(aulas):
    dias = []
    dia_atual = Dia('Dia 1')
    dias.append(dia_atual)

    professores_ocupados = defaultdict(list)

    for aula in aulas:
        alocada = False
        for dia in dias:
            for sessao in [dia.manha, dia.tarde]:
                hora_inicio = sessao.inicio + timedelta(minutes=sessao.tempo_usado)
                hora_fim = hora_inicio + timedelta(minutes=aula.duracao)
                if hora_fim <= sessao.fim and not conflito_professor(sessao, aula):
                    sessao.aulas.append(aula)
                    sessao.tempo_usado += aula.duracao
                    professores_ocupados[aula.professor].append((dia.nome, sessao.tipo))
                    alocada = True
                    break
            if alocada:
                break
        if not alocada:
            novo_dia = Dia(f'Dia {len(dias) + 1}')
            dias.append(novo_dia)
            novo_dia.manha.aulas.append(aula)
            novo_dia.manha.tempo_usado += aula.duracao
            professores_ocupados[aula.professor].append((novo_dia.nome, 'manha'))

    return dias

def conflito_professor(sessao, aula):
    for existente in sessao.aulas:
        if existente.professor == aula.professor:
            return True
    return False

def formatar_grade(dias):
    dias_semana = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira']
    for i, dia in enumerate(dias):
        nome_semana = dias_semana[i % len(dias_semana)]
        print(f"\n{nome_semana} ({dia.nome}):")
        for sessao in [dia.manha, dia.tarde]:
            hora_atual = sessao.inicio
            print(f"  {sessao.tipo.upper()}:")
            for aula in sessao.aulas:
                hora_fim = hora_atual + timedelta(minutes=aula.duracao)
                if hora_fim > sessao.fim:
                    print(f"    ERRO: Aula '{aula.titulo}' excede o horário permitido da sessão!")
                else:
                    print(f"    {hora_atual.strftime('%H:%M')} - {hora_fim.strftime('%H:%M')} | {aula.professor} - {aula.titulo}")
                hora_atual = hora_fim
            if not sessao.aulas:
                print("    (sem aulas)")
        print("  17:00 - REUNIÃO DE PROFESSORES")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python sistema_horarios.py <arquivo_aulas.txt>")
        sys.exit(1)

    caminho = sys.argv[1]
    try:
        aulas = ler_arquivo_aulas(caminho)
        dias = alocar_aulas(aulas)
        formatar_grade(dias)
    except Exception as e:
        print(f"Erro ao processar: {e}")
        sys.exit(1)
