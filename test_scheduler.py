import unittest
from scheduler import Aula, Sessao, parse_duracao, carregar_aulas_de_arquivo
from datetime import datetime
import os

class TestScheduler(unittest.TestCase):

    def test_parse_duracao(self):
        """Testa se a conversão da string de duração para minutos está correta."""
        self.assertEqual(parse_duracao('60min'), 60)
        self.assertEqual(parse_duracao('lightning'), 5)
        self.assertEqual(parse_duracao('30min'), 30)

    def test_carregar_aulas(self):
        """Testa o carregamento e parsing de aulas de um arquivo."""
        # Cria um arquivo de teste temporário
        conteudo_teste = "Aula Teste 1 - Prof. Teste 45min\nÉtica - Prof. Alpha lightning"
        caminho_teste = "aulas_teste.txt"
        with open(caminho_teste, "w", encoding="utf-8") as f:
            f.write(conteudo_teste)

        aulas = carregar_aulas_de_arquivo(caminho_teste)
        self.assertEqual(len(aulas), 2)
        
        self.assertEqual(aulas[0].tema, "Aula Teste 1")
        self.assertEqual(aulas[0].professor, "Prof. Teste")
        self.assertEqual(aulas[0].duracao, 45)
        
        self.assertEqual(aulas[1].tema, "Ética")
        self.assertEqual(aulas[1].professor, "Prof. Alpha")
        self.assertEqual(aulas[1].duracao, 5)

        # Remove o arquivo de teste
        os.remove(caminho_teste)

    def test_adicionar_aula_sessao(self):
        """Testa a lógica de adicionar aulas a uma sessão."""
        sessao = Sessao("Manhã Teste", datetime(1,1,1,9,0), 180)
        aula1 = Aula("Cálculo", "Prof. Gauss", 60)
        aula2 = Aula("Álgebra", "Prof. Euler", 60)
        aula_conflito_prof = Aula("Geometria", "Prof. Gauss", 30) # Mesmo professor
        aula_sem_tempo = Aula("Física", "Prof. Newton", 100) # Excede o tempo restante

        # Adiciona primeira aula com sucesso
        self.assertTrue(sessao.tentar_adicionar_aula(aula1))
        self.assertEqual(sessao.tempo_utilizado, 60)
        self.assertIn("Prof. Gauss", sessao.professores_alocados)

        # Adiciona segunda aula com sucesso
        self.assertTrue(sessao.tentar_adicionar_aula(aula2))
        self.assertEqual(sessao.tempo_utilizado, 120)

        # Falha ao adicionar por conflito de professor
        self.assertFalse(sessao.tentar_adicionar_aula(aula_conflito_prof))
        self.assertEqual(sessao.tempo_utilizado, 120) # Não deve mudar

        # Falha ao adicionar por falta de tempo
        self.assertFalse(sessao.tentar_adicionar_aula(aula_sem_tempo))
        self.assertEqual(sessao.tempo_utilizado, 120) # Não deve mudar

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)