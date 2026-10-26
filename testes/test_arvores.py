import random
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from arvore_avl import ArvoreAVL
from arvore_rubro_negra import ArvoreRN


class ContratoArvores(unittest.TestCase):
    CLASSE = None

    # Validar árvore - feito com IA
    def setUp(self):
        if self.CLASSE is None:
            self.skipTest('Classe abstrata de testes')
        self.arvore = self.CLASSE()
        self.referencia = set()

    # Validar árvore - feito com IA
    def validar(self):
        if isinstance(self.arvore, ArvoreAVL):
            valido, mensagem = self.arvore.validar_avl()
        else:
            valido, mensagem = self.arvore.validar_rn()
        self.assertTrue(valido, mensagem)
        self.assertEqual(self.arvore.percurso_em_ordem(), sorted(self.referencia))
        dados = self.arvore.obter_estatisticas()
        self.assertGreaterEqual(dados['altura'], 0)
        self.assertGreaterEqual(dados['rotacoes'], 0)

    def inserir(self, valor):
        self.arvore.inserir(valor)
        self.referencia.add(valor)
        self.validar()

    def remover(self, valor):
        self.arvore.remover(valor)
        self.referencia.discard(valor)
        self.validar()

    def test_vazia_e_um_elemento(self):
        self.validar()
        self.assertFalse(self.arvore.buscar(5))
        self.remover(5)
        self.inserir(5)
        self.assertTrue(self.arvore.buscar(5))
        self.remover(5)
        self.assertFalse(self.arvore.buscar(5))

    def test_ordem_crescente(self):
        for valor in range(1, 101):
            self.inserir(valor)

    def test_ordem_decrescente(self):
        for valor in range(100, 0, -1):
            self.inserir(valor)

    def test_ordem_nao_ordenada(self):
        for valor in [50, 30, 70, 20, 40, 60, 80, 10, 90, 35]:
            self.inserir(valor)
        for valor in [10, 35, 50, 90, 999]:
            self.assertEqual(self.arvore.buscar(valor), valor in self.referencia)

    def test_duplicados(self):
        for valor in [30, 20, 30, 20, 40, 40, 30]:
            self.inserir(valor)
        self.assertEqual(self.arvore.percurso_em_ordem(), [20, 30, 40])

    def test_remocao_folha_um_filho_dois_filhos(self):
        for valor in [50, 30, 70, 20, 40, 60, 80]:
            self.inserir(valor)
        # A sequência de diferentes configurações, a estrutura pode mudar entre as árvores em função dos rebalanceamentos
        for valor in [20, 30, 50, 999, 70, 40, 60, 80]:
            self.remover(valor)
            self.assertFalse(self.arvore.buscar(valor))

    def test_remocoes_em_serie(self):
        for valor in range(1, 101):
            self.inserir(valor)
        for valor in range(100, 0, -1):
            self.remover(valor)
        self.assertEqual(self.arvore.percurso_em_ordem(), [])

    def test_operacoes_aleatorias_reproduziveis(self):
        gerador = random.Random(2026)
        for _ in range(600):
            valor = gerador.randrange(-100, 101)
            operacao = gerador.choice(['inserir', 'remover', 'buscar'])
            if operacao == 'inserir':
                self.inserir(valor)
            elif operacao == 'remover':
                self.remover(valor)
            else:
                self.assertEqual(self.arvore.buscar(valor), valor in self.referencia)
                self.validar()


class TestesAVL(ContratoArvores):
    CLASSE = ArvoreAVL


class TestesRubroNegra(ContratoArvores):
    CLASSE = ArvoreRN


if __name__ == '__main__':
    unittest.main(verbosity=2)
