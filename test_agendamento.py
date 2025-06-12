import pytest
from agendamento import ler_aulas, obter_grade_formatada, Aula, organizar_aulas

def test_leitura_aulas(tmp_path):
    conteudo = """Introdução à IA - Prof. Ana 60min
Machine Learning - Prof. João 45min
Deep Learning - Prof. Ana lightning
"""
    arquivo = tmp_path / "aulas.txt"
    arquivo.write_text(conteudo, encoding="utf-8")
    
    aulas = ler_aulas(arquivo)
    
    assert len(aulas) == 3
    assert aulas[0].titulo == "Introdução à IA"
    assert aulas[0].professor == "Ana"
    assert aulas[0].duracao == 60
    assert aulas[2].duracao == 5  # lightning

def test_geracao_grade():
    aulas = [
        Aula("Aula 1", "Prof. Ana", "60min"),
        Aula("Aula 2", "Prof. João", "45min"),
        Aula("Aula 3", "Prof. Ana", "lightning"),
        Aula("Aula 4", "Prof. Maria", "30min"),
    ]
    grade = obter_grade_formatada(aulas)
    assert "Prof. Ana" in grade
    assert "Aula 1" in grade
    assert "17:00 Reunião de Professores" in grade

def test_todas_aulas_alocadas():
    aulas = [
        Aula("A1", "Prof. Ana", "60min"),
        Aula("A2", "Prof. João", "45min"),
        Aula("A3", "Prof. Ana", "30min"),
        Aula("A4", "Prof. Maria", "30min"),
        Aula("A5", "Prof. João", "lightning"),
    ]
    dias = organizar_aulas(aulas)
    
    alocadas = []
    for dia in dias:
        for sessao in [dia.manha, dia.tarde]:
            alocadas.extend(a for _, a in sessao.aulas)
    
    assert len(alocadas) == len(aulas), "Nem todas as aulas foram alocadas!"

def test_sem_conflito_professores():
    aulas = [
        Aula("Longa 1", "Prof. A", "180min"),
        Aula("Longa 2", "Prof. A", "180min"),
        Aula("Curta", "Prof. B", "30min"),
    ]
    dias = organizar_aulas(aulas)

    professor_horarios = {}

    for dia in dias:
        for sessao in [dia.manha, dia.tarde]:
            for hora_inicio, aula in sessao.aulas:
                inicio = int(hora_inicio[:2]) * 60 + int(hora_inicio[3:])
                fim = inicio + aula.duracao

                if aula.professor not in professor_horarios:
                    professor_horarios[aula.professor] = []

                for start, end in professor_horarios[aula.professor]:
                    assert fim <= start or inicio >= end, f"Conflito detectado para {aula.professor} em {hora_inicio}"

                professor_horarios[aula.professor].append((inicio, fim))
