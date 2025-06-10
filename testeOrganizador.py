import unittest
from organizador import Aula, Bloco, interpretar_duracao, ler_aulas_arquivo
from datetime import datetime
import os

class TesteAgendador(unittest.TestCase):

    def testeDeduracao(self):
        self.assertEqual(interpretar_duracao("45min"), 45)
        self.assertEqual(interpretar_duracao("lightning"), 5)

    def testDeAulas(self):
        arquivo_temp = "teste_aulas.txt"
        with open(arquivo_temp, "w", encoding="utf-8") as f:
            f.write("Introdução à IA - Prof. João 60min\nÉtica na IA - Prof. Carla lightning")

        aulas = ler_aulas_arquivo(arquivo_temp)
        os.remove(arquivo_temp)

        self.assertEqual(len(aulas), 2)
        self.assertEqual(aulas[0].tema, "Introdução à IA")
        self.assertEqual(aulas[0].professor, "Prof. João")
        self.assertEqual(aulas[0].duracao, 60)
        self.assertEqual(aulas[1].tema, "Ética na IA")
        self.assertEqual(aulas[1].duracao, 5)

    def testeProfessorRepetido(self):
        bloco = Bloco("Manhã", datetime(1, 1, 1, 9, 0), 180)

        aula1 = Aula("Introdução à IA", "Prof. João", 60)
        aula2 = Aula("Banco de Dados NoSQL", "Prof. Ana", 60)
        aula3 = Aula("Redes Neurais Convolucionais", "Prof. João", 30)  

        self.assertTrue(bloco.adicionar(aula1))
        self.assertTrue(bloco.adicionar(aula2))
        self.assertFalse(bloco.adicionar(aula3))  

    def testeSemEspaco(self):
        bloco = Bloco("Tarde", datetime(1, 1, 1, 13, 0), 90)

        aula1 = Aula("Lógica Computacional", "Prof. Paulo", 45)
        aula2 = Aula("História da Computação", "Prof. Carla", 30)
        aula3 = Aula("Pensamento Computacional", "Prof. Carla", 30)  
        aula4 = Aula("Compiladores e Interpretadores", "Prof. João", 60) 

        self.assertTrue(bloco.adicionar(aula1))
        self.assertTrue(bloco.adicionar(aula2))
        self.assertFalse(bloco.adicionar(aula3))  
        self.assertFalse(bloco.adicionar(aula4)) 

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)
