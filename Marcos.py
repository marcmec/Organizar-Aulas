from datetime import datetime, timedelta
import re


MANHA_INICIO = datetime.strptime("09:00", "%H:%M")
MANHA_FIM = datetime.strptime("12:00", "%H:%M")
TARDE_INICIO = datetime.strptime("13:00", "%H:%M")
TARDE_FIM = datetime.strptime("17:00", "%H:%M")


def carregar_aulas(arquivo):
    aulas = []
    with open(arquivo, 'r', encoding='utf-8') as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            match = re.match(r"(.+?) - Prof\. (.+?) (\d+min|lightning)", linha)
            if match:
                titulo, professor, duracao = match.groups()
                duracao_min = 5 if duracao == "lightning" else int(duracao.replace("min", ""))
                aulas.append({
                    "titulo": titulo.strip(),
                    "professor": professor.strip(),
                    "duracao": duracao_min
                })
    return aulas


def alocar_sessao(aulas, inicio, fim, professores_ocupados):
    horario_atual = inicio
    sessao = []
    i = 0
    while i < len(aulas):
        aula = aulas[i]
        duracao = timedelta(minutes=aula["duracao"])
        if horario_atual + duracao <= fim and not professor_ocupado(aula["professor"], horario_atual, duracao, professores_ocupados):
            sessao.append((horario_atual, aula))
            registrar_ocupacao(aula["professor"], horario_atual, duracao, professores_ocupados)
            horario_atual += duracao
            aulas.pop(i)
        else:
            i += 1
    return sessao

def professor_ocupado(professor, inicio, duracao, ocupados):
    fim = inicio + duracao
    for (ini, fim_existente) in ocupados.get(professor, []):
        if inicio < fim_existente and fim > ini:
            return True
    return False

def registrar_ocupacao(professor, inicio, duracao, ocupados):
    fim = inicio + duracao
    ocupados.setdefault(professor, []).append((inicio, fim))


def organizar_grade(aulas):
    dias = []
    professores_ocupados = {}
    dia_num = 0

    while aulas:
        dia_num += 1
        dia = {
            "nome": f"{['Segunda','Terça','Quarta','Quinta','Sexta','Sábado','Domingo'][dia_num - 1]}-feira",
            "manha": [],
            "tarde": []
        }
        dia["manha"] = alocar_sessao(aulas, MANHA_INICIO, MANHA_FIM, professores_ocupados)
        dia["tarde"] = alocar_sessao(aulas, TARDE_INICIO, TARDE_FIM, professores_ocupados)
        dias.append(dia)

    return dias


def imprimir_grade(dias):
    for dia in dias:
        print(f"📅 {dia['nome']}:")
        if not dia["manha"] and not dia["tarde"]:
            print("  (sem aulas)")
        else:
            for periodo, nome in [("manha", "09:00"), ("tarde", "13:00")]:
                for horario, aula in dia[periodo]:
                    tempo = "lightning" if aula["duracao"] == 5 else f"{aula['duracao']}min"
                    hora_str = horario.strftime("%H:%M")
                    print(f"{hora_str} {aula['titulo']} - Prof. {aula['professor']} {tempo}")
                if periodo == "manha":
                    print("12:00 Intervalo para Almoço\n")
            print("17:00 Reunião de Professores\n")


if __name__ == "__main__":
    aulas = carregar_aulas("aulas.txt")
    dias = organizar_grade(aulas)
    imprimir_grade(dias)