import unittest
from datetime import datetime, timedelta
from organizador import Aula, Sessao, OrganizadorHorarios

class TestAula(unittest.TestCase):
    def test_criacao_aula_normal(self):
        aula = Aula("Teste", "Prof. João", 60)
        self.assertEqual(aula.titulo, "Teste")
        self.assertEqual(aula.professor, "Prof. João")
        self.assertEqual(aula.duracao, 60)
    
    def test_str_aula_normal(self):
        aula = Aula("Teste", "Prof. João", 60)
        self.assertEqual(str(aula), "Teste - Prof. João 60min")
    
    def test_str_aula_lightning(self):
        aula = Aula("Teste Lightning", "Prof. Ana", 5)
        self.assertEqual(str(aula), "Teste Lightning - Prof. Ana lightning")

class TestSessao(unittest.TestCase):
    def setUp(self):
        self.inicio = datetime(2025, 6, 9, 9, 0)
        self.fim = datetime(2025, 6, 9, 12, 0)
        self.sessao = Sessao("manhã", self.inicio, self.fim)
    
    def test_tempo_disponivel_inicial(self):
        self.assertEqual(self.sessao.tempo_disponivel(), 180)  # 3 horas = 180 min
    
    def test_adicionar_aula_sucesso(self):
        aula = Aula("Teste", "Prof. João", 60)
        resultado = self.sessao.adicionar_aula(aula)
        self.assertTrue(resultado)
        self.assertEqual(len(self.sessao.aulas), 1)
        self.assertEqual(self.sessao.tempo_disponivel(), 120)
    
    def test_adicionar_aula_sem_tempo(self):
        aula = Aula("Teste Longa", "Prof. João", 200)  # Mais que 180 min disponíveis
        resultado = self.sessao.adicionar_aula(aula)
        self.assertFalse(resultado)
        self.assertEqual(len(self.sessao.aulas), 0)
    
    def test_conflito_professor(self):
        aula1 = Aula("Teste 1", "Prof. João", 60)
        aula2 = Aula("Teste 2", "Prof. João", 60)
        
        self.assertTrue(self.sessao.adicionar_aula(aula1))
        self.assertTrue(self.sessao.adicionar_aula(aula2))  # Deve conseguir após a primeira
        
        self.assertEqual(len(self.sessao.aulas), 2)

class TestOrganizadorHorarios(unittest.TestCase):
    def setUp(self):
        self.organizador = OrganizadorHorarios()
    
    def test_parsear_arquivo(self):
        conteudo = """Introdução à IA - Prof. João 60min
Ética na IA - Prof. Carla lightning
Teste - Prof. Ana 45min"""
        
        aulas = self.organizador.parsear_arquivo(conteudo)
        
        self.assertEqual(len(aulas), 3)
        self.assertEqual(aulas[0].titulo, "Introdução à IA")
        self.assertEqual(aulas[0].professor, "Prof. João")
        self.assertEqual(aulas[0].duracao, 60)
        
        self.assertEqual(aulas[1].titulo, "Ética na IA")
        self.assertEqual(aulas[1].duracao, 5)  # lightning = 5 min
    
    def test_organizacao_aulas_simples(self):
        conteudo = """Aula 1 - Prof. João 60min
Aula 2 - Prof. Ana 45min"""
        
        aulas = self.organizador.parsear_arquivo(conteudo)
        resultado = self.organizador.organizar_aulas(aulas)
        
        self.assertTrue(resultado)
    
    def test_organizacao_aulas_complexas(self):
        conteudo = """Introdução à IA - Prof. João 60min
Técnicas de Aprendizado Supervisionado - Prof. Ana 45min
Redes Neurais Convolucionais - Prof. João 30min
Ética na IA - Prof. Carla lightning
Linguagens de Programação Funcionais - Prof. Paulo 45min"""
        
        aulas = self.organizador.parsear_arquivo(conteudo)
        resultado = self.organizador.organizar_aulas(aulas)
        
        self.assertTrue(resultado)

class TestIntegracao(unittest.TestCase):
    def test_exemplo_completo(self):
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
        
        organizador = OrganizadorHorarios()
        aulas = organizador.parsear_arquivo(conteudo_arquivo)
        resultado = organizador.organizar_aulas(aulas)
        
        # Verifica se todas as aulas foram organizadas
        self.assertTrue(resultado)
        
        # Verifica se há aulas organizadas
        total_aulas_organizadas = 0
        for sessoes_dia in organizador.sessoes:
            for sessao in sessoes_dia:
                total_aulas_organizadas += len(sessao.aulas)
        
        self.assertEqual(total_aulas_organizadas, len(aulas))

if __name__ == '__main__':
    # Executa os testes
    unittest.main(verbosity=2)