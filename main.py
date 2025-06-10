from organizador import ler_aulas_arquivo, GradeHoraria, mostrar_grade

def main():
    try:
        caminho = 'aulas.txt'
        aulas = ler_aulas_arquivo(caminho)

        grade = GradeHoraria(aulas)
        dias = grade.montar_grade()

        mostrar_grade(dias)

    except FileNotFoundError:
        print(f"[ERRO] Arquivo '{caminho}' não encontrado.")
    except Exception as erro:
        print(f"[ERRO] Erro inesperado: {erro}")

if __name__ == "__main__":
    main()
