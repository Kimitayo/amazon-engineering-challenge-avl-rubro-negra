from pathlib import Path
import sys

# Vai ser usado "assert" para validar os testes

# Para importar os arquivos da pasta principal do projeto
pasta_projeto = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(pasta_projeto))

from arvore_avl import ArvoreAVL


def teste_insercao():

    arvore = ArvoreAVL()

    valores = [50, 30, 70, 20, 40]

    for valor in valores:
        arvore.inserir(valor)

    resultado = arvore.percurso_em_ordem()

    assert resultado == [20, 30, 40, 50, 70], \
        "Erro: os valores não foram inseridos corretamente"

    valida, mensagem = arvore.validar_avl()

    assert valida, mensagem

    print("Teste de inserção: APROVADO")


teste_insercao()


# Testando diferentes ordens de inserção
def teste_ordens_insercao():

    casos = {
        "Crescente": [10, 20, 30, 40, 50],
        "Decrescente": [50, 40, 30, 20, 10],
        "Aleatória": [30, 10, 50, 20, 40]
    }

    for nome, valores in casos.items():

        arvore = ArvoreAVL()

        for valor in valores:
            arvore.inserir(valor)

            valida, mensagem = arvore.validar_avl()

            assert valida, (
                f"Erro na inserção {valor}, "
                f"caso {nome}: {mensagem}"
            )

        esperado = sorted(valores)

        assert arvore.percurso_em_ordem() == esperado, \
            f"Erro na ordenação do caso {nome}"

        print(f"Inserção {nome}: APROVADA")


# Testando a busca
def teste_busca():

    arvore = ArvoreAVL()

    valores = [50, 30, 70, 20, 40]

    for valor in valores:
        arvore.inserir(valor)

    # Elementos existentes
    assert arvore.buscar(50) is True
    assert arvore.buscar(20) is True
    assert arvore.buscar(70) is True

    # Elementos inexistentes
    assert arvore.buscar(100) is False
    assert arvore.buscar(999) is False

    print("Teste de busca: APROVADO")


def teste_duplicados():

    arvore = ArvoreAVL()

    arvore.inserir(50)
    arvore.inserir(30)
    arvore.inserir(50)
    arvore.inserir(30)

    esperado = [30, 50]

    assert arvore.percurso_em_ordem() == esperado, \
        "Erro: a árvore permitiu valores duplicados"

    valida, mensagem = arvore.validar_avl()

    assert valida, mensagem

    print("Teste de duplicados: APROVADO")


# Teste de remoção
def teste_remocao():

    arvore = ArvoreAVL()

    valores = [50, 30, 70, 20, 40, 60, 80]

    for valor in valores:
        arvore.inserir(valor)

    # Remove um nó folha
    arvore.remover(20)

    assert arvore.buscar(20) is False
    assert arvore.validar_avl()[0] is True

    # Remove um nó com um filho
    arvore.remover(30)

    assert arvore.buscar(30) is False
    assert arvore.validar_avl()[0] is True

    # Remove um nó com dois filhos
    arvore.remover(50)

    assert arvore.buscar(50) is False
    assert arvore.validar_avl()[0] is True

    # Remove um elemento inexistente
    arvore.remover(999)

    assert arvore.validar_avl()[0] is True

    # Verifica os elementos restantes
    esperado = [40, 60, 70, 80]

    assert arvore.percurso_em_ordem() == esperado, \
        "Erro: os elementos restantes estão incorretos"

    print("Teste de remoção: APROVADO")


# Testano árvores vazias
def teste_arvore_vazia():

    arvore = ArvoreAVL()

    # Busca em árvore vazia
    assert arvore.buscar(50) is False

    # Percurso em árvore vazia
    assert arvore.percurso_em_ordem() == []

    # Remoção em árvore vazia
    arvore.remover(50)

    assert arvore.raiz is None

    # Validação de árvore vazia
    valida, mensagem = arvore.validar_avl()

    assert valida, mensagem

    # Insere e remove o único elemento
    arvore.inserir(100)

    assert arvore.buscar(100) is True

    arvore.remover(100)

    assert arvore.raiz is None

    print("Teste de árvore vazia: APROVADO")




# TESTES
if __name__ == "__main__":
    teste_insercao()
    teste_ordens_insercao()
    teste_busca()
    teste_duplicados()
    teste_remocao()
    teste_arvore_vazia()

    print("\nTODOS OS TESTES FORAM APROVADOS!")