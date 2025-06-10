# Testes por [SEU NOME] - LAA02

import unittest
from organizador import Disciplina, BlocoAulas, converter_carga_horaria, carregar_disciplinas
from datetime import datetime
import os

class TestOrganizador(unittest.TestCase):

    def test_converter_carga_horaria(self):
        self.assertEqual(converter_carga_horaria('60min'), 60)
        self.assertEqual(converter_carga_horaria('lightning'), 5)

    def test_carregar_disciplinas(self):
        conteudo = "Matemática - Prof. Silva 60min\nFísica - Prof. Costa lightning"
        arquivo_teste = "disciplinas_teste.txt"
        
        with open(arquivo_teste, "w", encoding="utf-8") as f:
            f.write(conteudo)

        disciplinas = carregar_disciplinas(arquivo_teste)
        self.assertEqual(len(disciplinas), 2)
        os.remove(arquivo_teste)

    def test_alocacao_disciplinas(self):
        bloco = BlocoAulas("Teste", datetime(1,1,1,9,0), 180)
        disciplina1 = Disciplina("Química", "Prof. Lima", 60)
        self.assertTrue(bloco.alocar_disciplina(disciplina1))

if __name__ == '__main__':
    unittest.main()