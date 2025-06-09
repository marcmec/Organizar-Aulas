import unittest
from sistema_horarios import Aula, alocar_aulas, conflito_professor, Sessao, Dia
from datetime import datetime

class TestSistemaHorarios(unittest.TestCase):

    def setUp(self):
        self.aulas = [
            Aula("Introdução à IA", "Prof. João", 60),
            Aula("Banco de Dados", "Prof. Ana", 60),
            Aula("Redes", "Prof. João", 30),
            Aula("Ética", "Prof. Carla", 5)
        ]

    def test_alocacao_sem_conflito(self):
        dias = alocar_aulas(self.aulas)
        alocadas = sum(len(sessao.aulas) for dia in dias for sessao in [dia.manha, dia.tarde])
        self.assertEqual(alocadas, len(self.aulas))

    def test_conflito_professor(self):
        sessao = Sessao("manha", datetime.strptime("09:00", "%H:%M"), datetime.strptime("12:00", "%H:%M"))
        aula1 = Aula("Algoritmos", "Prof. João", 60)
        aula2 = Aula("Lógica", "Prof. João", 45)
        sessao.aulas.append(aula1)
        self.assertTrue(conflito_professor(sessao, aula2))

    def test_sem_conflito_professor(self):
        sessao = Sessao("tarde", datetime.strptime("13:00", "%H:%M"), datetime.strptime("17:00", "%H:%M"))
        aula1 = Aula("Cálculo", "Prof. Ana", 60)
        aula2 = Aula("Física", "Prof. Carla", 45)
        sessao.aulas.append(aula1)
        self.assertFalse(conflito_professor(sessao, aula2))

    def test_limite_tempo_sessao(self):
        dia = Dia("Dia 1")
        for i in range(6):
            dia.manha.aulas.append(Aula(f"Aula {i}", f"Prof. X{i}", 30))
            dia.manha.tempo_usado += 30
        self.assertEqual(dia.manha.tempo_disponivel(), 0)

if __name__ == '__main__':
    unittest.main()
