# Solução por Pedro Teixeira - LAA02
from organizador import carregar_disciplinas, GradeHoraria, exibir_cronograma

def executar():
    """Função principal para gerar o cronograma de aulas."""
    try:
        # 1. Carregar as disciplinas do arquivo
        caminho_arquivo = 'disciplinas.txt' 
        lista_disciplinas = carregar_disciplinas(caminho_arquivo)
        
        # 2. Criar e executar o organizador
        organizador = GradeHoraria(lista_disciplinas)
        cronograma = organizador.organizar()
        
        # 3. Exibir o resultado formatado
        exibir_cronograma(cronograma)

    except FileNotFoundError:
        print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")
    except Exception as erro:
        print(f"Erro inesperado: {erro}")

if __name__ == "__main__":
    executar()