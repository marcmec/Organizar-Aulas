from datetime import datetime, timedelta

class Aula:
    def __init__(self, titulo, professor, duracao):
        self.titulo = titulo
        self.professor = professor
        self.duracao = duracao

def ler_aulas(nome_arquivo):
    aulas = []
    with open(nome_arquivo, 'r', encoding='utf-8') as f:
        for linha in f:
            partes = linha.strip().rsplit(" - ", 1)
            titulo = partes[0]
            professor_e_tempo = partes[1].rsplit(" ", 1)
            professor = professor_e_tempo[0]
            tempo = professor_e_tempo[1]
            duracao = 5 if tempo.lower() == "lightning" else int(tempo.replace("min", ""))
            aulas.append(Aula(titulo, professor, duracao))
    return aulas

def agendar_aulas(aulas):
    hora_manha_inicio = datetime.strptime("09:00", "%H:%M")
    hora_manha_fim = datetime.strptime("12:00", "%H:%M")
    hora_tarde_inicio = datetime.strptime("13:00", "%H:%M")
    hora_tarde_fim = datetime.strptime("17:00", "%H:%M")

    nomes_dias = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira"]
    
    dias = []

    index_dia = 0
    


    while aulas:
        nome_dia = nomes_dias[index_dia]
        dia = {"nome": nome_dia, "manha": [], "tarde": []}
        agenda_professor = {}

        for inicio, fim, chave in [(hora_manha_inicio, hora_manha_fim, "manha"), (hora_tarde_inicio, hora_tarde_fim, "tarde")]:
            hora = inicio
            i = 0
            while i < len(aulas):
                aula = aulas[i]
                dur = timedelta(minutes=aula.duracao)
                fim_aula = hora + dur

                conflitos = any(
                    start < fim_aula and hora < end
                    for start, end in agenda_professor.get(aula.professor, [])
                )
                if fim_aula <= fim and not conflitos:
                    dia[chave].append((hora.strftime("%H:%M"), aula))
                    agenda_professor.setdefault(aula.professor, []).append((hora, fim_aula))
                    hora = fim_aula
                    aulas.pop(i)
                else:
                    i += 1

        dias.append(dia)

        index_dia = (index_dia + 1) % 5

    return dias


def imprimir_agenda(dias):
    for dia in dias:
        print(f"====={dia['nome']}=====:")
        if dia["manha"]:
            for hora, aula in dia["manha"]:
                dur_str = f"{aula.duracao}min"
                print(f"{hora} {aula.titulo} - {aula.professor} {dur_str}")
        else:
            print("09:00 (sem aulas disponíveis)")
        print("12:00 Intervalo para Almoço\n")

        if dia["tarde"]:
            for hora, aula in dia["tarde"]:
                dur_str = f"{aula.duracao}min"
                print(f"{hora} {aula.titulo} - {aula.professor} {dur_str}")
        else:
            print("13:00 (sem aulas disponíveis)")
        print("17:00 Reunião de Professores\n")



if __name__ == "__main__":
    aulas = ler_aulas("aulas.txt")
    dias = agendar_aulas(aulas)
    imprimir_agenda(dias)
