from scheduler import carregar_aulas_de_arquivo, Agenda, imprimir_grade

def main():
    """Função principal para executar o programa de agendamento."""
    try:
        # 1 Carregar as aulas do arquivo
        caminho_arquivo = 'aulas.txt'
        lista_de_aulas = carregar_aulas_de_arquivo(caminho_arquivo)
        
        # 2 Criar e executar o agendador
        agendador = Agenda(lista_de_aulas)
        grade_final = agendador.agendar()
        
        # 3 Imprimir o resultado formatado
        imprimir_grade(grade_final)

    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    main()