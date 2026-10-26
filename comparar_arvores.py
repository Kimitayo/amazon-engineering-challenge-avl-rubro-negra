# Gera resultados comparáveis em resultados_comparacao.csv.

import csv
import random
from pathlib import Path
from arvore_avl import ArvoreAVL
from arvore_rubro_negra import ArvoreRN


def executar(classe, insercoes, remocoes):
    arvore = classe()
    for valor in insercoes:
        arvore.inserir(valor)
    apos_insercao = dict(arvore.obter_estatisticas())
    for valor in remocoes:
        arvore.remover(valor)
    apos_remocao = dict(arvore.obter_estatisticas())
    if isinstance(arvore, ArvoreAVL):
        valido, mensagem = arvore.validar_avl()
    else:
        valido, mensagem = arvore.validar_rn()
    assert valido, mensagem
    assert arvore.percurso_em_ordem() == sorted(set(insercoes) - set(remocoes))
    return apos_insercao, apos_remocao


def main():
    n = 100
    aleatoria = list(range(1, n + 1))
    random.Random(2026).shuffle(aleatoria)
    cenarios = {
        'Crescente': list(range(1, n + 1)),
        'Decrescente': list(range(n, 0, -1)),
        'Embaralhada (semente 2026)': aleatoria,
    }
    registros = []
    for nome, insercoes in cenarios.items():
        remocoes = insercoes[::3]  # exatamente as mesmas remoções nas duas árvores
        for tipo, classe in [('AVL', ArvoreAVL), ('Rubro-Negra', ArvoreRN)]:
            insercao, remocao = executar(classe, insercoes, remocoes)
            registros.append({
                'cenario': nome, 'arvore': tipo,
                'n_inseridos': len(insercoes), 'n_removidos': len(remocoes),
                'altura_apos_insercao': insercao['altura'],
                'rotacoes_apos_insercao': insercao['rotacoes'],
                'altura_final': remocao['altura'],
                'rotacoes_total': remocao['rotacoes'],
                'rotacoes_na_remocao': remocao['rotacoes'] - insercao['rotacoes'],
                'recoloracoes_total': remocao.get('recoloracoes', 'N/A'),
            })

    # Feito com IA
    destino = Path(__file__).resolve().parent / 'resultados_comparacao.csv'
    with destino.open('w', newline='', encoding='utf-8-sig') as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=list(registros[0]), delimiter=';')
        escritor.writeheader()
        escritor.writerows(registros)
    for linha in registros:
        print(f"{linha['cenario']:<29} {linha['arvore']:<12} "
              f"altura={linha['altura_final']:<3} rotações={linha['rotacoes_total']}")
    print(f'\nArquivo gerado: {destino.name}')


if __name__ == '__main__':
    main()
