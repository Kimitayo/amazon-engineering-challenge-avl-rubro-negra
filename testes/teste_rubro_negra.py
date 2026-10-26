import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from arvore_rubro_negra import ArvoreRN, PRETO, VERMELHO


class TestesRubroNegra(unittest.TestCase): # vou utlizar frameworks para teste
    def setUp(self):
        self.arvore = ArvoreRN()
        self.referencia = set()

    def conferir(self):
        valido, mensagem = self.arvore.validar_rn()
        self.assertTrue(valido, mensagem)
        self.assertEqual(self.arvore.percurso_em_ordem(), sorted(self.referencia))
        self.assertEqual(self.arvore.raiz is self.arvore.NIL, not self.referencia)
        self.assertEqual(self.arvore.NIL.cor, PRETO)
        if self.referencia:
            self.assertEqual(self.arvore.raiz.cor, PRETO)
        estatisticas = self.arvore.obter_estatisticas()
        self.assertGreaterEqual(estatisticas['altura'], 0)
        self.assertGreaterEqual(estatisticas['rotacoes'], 0)
        self.assertGreaterEqual(estatisticas['recoloracoes'], 0)

    def inserir(self, valor):
        self.arvore.inserir(valor)
        self.referencia.add(valor)
        self.conferir()

    def remover(self, valor):
        self.arvore.remover(valor)
        self.referencia.discard(valor)
        self.conferir()

    def test_arvore_vazia_e_um_elemento(self):
        self.conferir()
        self.assertFalse(self.arvore.buscar(42))
        self.remover(42)
        self.inserir(42)
        self.assertTrue(self.arvore.buscar(42))
        self.remover(42)
        self.assertFalse(self.arvore.buscar(42))

    def test_insercao_crescente(self):
        for valor in range(1, 101):
            self.inserir(valor)

    def test_insercao_decrescente(self):
        for valor in range(100, 0, -1):
            self.inserir(valor)

    def test_insercao_embaralhada(self):
        valores = list(range(1, 101))
        random.Random(2026).shuffle(valores)
        for valor in valores:
            self.inserir(valor)

    def test_buscas_existentes_e_inexistentes(self):
        for valor in [50, 30, 70, 20, 40, 60, 80]:
            self.inserir(valor)
        for valor in [20, 40, 50, 80]:
            self.assertTrue(self.arvore.buscar(valor))
        for valor in [-1, 0, 35, 999]:
            self.assertFalse(self.arvore.buscar(valor))
        self.conferir()

    def test_duplicados(self):
        for valor in [30, 20, 30, 20, 40, 40, 30]:
            self.inserir(valor)
        self.assertEqual(self.arvore.percurso_em_ordem(), [20, 30, 40])

    def test_remocao_folha_um_filho_dois_filhos_e_inexistente(self):
        for valor in [50, 30, 70, 20, 40, 60, 80]:
            self.inserir(valor)
        for valor in [20, 30, 50, 999]:
            self.remover(valor)
            self.assertFalse(self.arvore.buscar(valor))
        self.assertEqual(self.arvore.percurso_em_ordem(), [40, 60, 70, 80])

    def test_remover_todos_em_ordem_inversa(self):
        for valor in range(1, 101):
            self.inserir(valor)
        for valor in range(100, 0, -1):
            self.remover(valor)
        self.assertEqual(self.arvore.percurso_em_ordem(), [])

    def test_rotacoes_e_recoloracoes(self):
        for valor in [50, 30, 20]:
            self.inserir(valor)
        self.assertGreaterEqual(self.arvore.total_rotacoes, 1)
        self.assertGreaterEqual(self.arvore.total_recoloracoes, 1)

    def test_operacoes_aleatorias_reproduziveis(self):
        gerador = random.Random(2026)
        for _ in range(1000):
            valor = gerador.randint(-200, 200)
            operacao = gerador.choice(('inserir', 'remover', 'buscar'))
            if operacao == 'inserir':
                self.inserir(valor)
            elif operacao == 'remover':
                self.remover(valor)
            else:
                self.assertEqual(self.arvore.buscar(valor), valor in self.referencia)
                self.conferir()

    def test_validador_identifica_violacao_vermelho_vermelho(self):
        for valor in [50, 30, 70]:
            self.inserir(valor)
        self.arvore.raiz.esquerda.cor = VERMELHO
        self.arvore.raiz.cor = VERMELHO
        valido, _ = self.arvore.validar_rn()
        self.assertFalse(valido)


if __name__ == '__main__':
    unittest.main(verbosity=2)
