import unittest
from datetime import datetime
from problem import carregar_aulas_da_lista, alocar_aulas

class TesteAgendaIA(unittest.TestCase):
    def setUp(self):
        self.aulas_brutas = [
            "Introdução à IA - Prof. João 60min",
            "Redes Neurais Convolucionais - Prof. João 30min",
            "Ética na IA - Prof. Carla lightning",
            "Banco de Dados NoSQL - Prof. Ana 60min"
        ]

    def test_carregar_aulas_da_lista(self):
        aulas = carregar_aulas_da_lista(self.aulas_brutas)
        self.assertEqual(len(aulas), 4)
        self.assertEqual(aulas[2]['duracao'], 5)
        self.assertEqual(aulas[0]['professor'], "João")

    def test_alocar_aulas(self):
        aulas = carregar_aulas_da_lista(self.aulas_brutas)
        agenda = alocar_aulas(aulas)
        self.assertTrue(len(agenda) >= 1)
        total_aulas = sum(len(agenda[i]['manha']) + len(agenda[i]['tarde']) for i in range(len(agenda)))
        self.assertEqual(total_aulas, 4)

if __name__ == '__main__':
    unittest.main()
