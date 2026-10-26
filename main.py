import random
from time import perf_counter

from arvore_avl import ArvoreAVL
from arvore_rubro_negra import ArvoreRN


TIPOS = {"1": ("AVL", ArvoreAVL), "2": ("Rubro-Negra", ArvoreRN)}

# VALIDACAO DE PROMPT
# Solicita um inteiro, sem encerrar o programa diante de entradas inválidas
def ler_inteiro(mensagem):
    while True:
        entrada = input(mensagem).strip()
        try:
            return int(entrada)
        except ValueError:
            print("Entrada inválida!")

# Se a opção escolhida é valida
def ler_opcao(mensagem, validas):
    while True:
        opcao = input(mensagem).strip()
        if opcao in validas:
            return opcao
        print("Opção inválida! Escolha uma das opções apresentadas.")

# Validar o tipo de arvore
def validar(arvore):
    if isinstance(arvore, ArvoreAVL):
        return arvore.validar_avl()
    return arvore.validar_rn()

# Utiliza as funções de estatística de arvore_avl.py e arvore_rubro_negra.py
def altura(arvore):
    return arvore.obter_estatisticas()["altura"]


def mostrar_estatisticas(arvore):
    dados = arvore.obter_estatisticas()
    print(f"Quantidade de elementos: {len(arvore.percurso_em_ordem())}")
    print(f"Altura: {dados['altura']}")
    print(f"Rotações simples acumuladas: {dados['rotacoes']}")
    if "recoloracoes" in dados:
        print(f"Recolorações acumuladas: {dados['recoloracoes']}")


# MENU
def menu_arvore(nome, arvore):
    while True:
        print(f"\n{'=' * 58}")
        print(f"ÁRVORE {nome.upper()}")
        print("1 - Inserir identificador")
        print("2 - Remover identificador")
        print("3 - Buscar identificador")
        print("4 - Percurso em ordem (crescente)")
        print("5 - Visualizar estrutura")
        print("6 - Estatísticas (altura e ajustes)")
        print("7 - Validar propriedades de balanceamento")
        print("8 - Inserir vários identificadores")
        print("9 - Limpar árvore (criar nova)")
        print("0 - Voltar ao menu principal")
        opcao = ler_opcao("Escolha: ", set("0123456789"))

        if opcao == "0":
            return arvore
        if opcao == "1":
            valor = ler_inteiro("Identificador a inserir: ")
            if arvore.buscar(valor):
                print(f"O identificador {valor} já existe; duplicados são ignorados.")
            else:
                arvore.inserir(valor)
                print(f"Identificador {valor} inserido.")
        elif opcao == "2":
            valor = ler_inteiro("Identificador a remover: ")
            if not arvore.buscar(valor):
                print(f"Identificador {valor} não encontrado; nada foi removido.")
            else:
                arvore.remover(valor)
                print(f"Identificador {valor} removido.")
        elif opcao == "3":
            valor = ler_inteiro("Identificador a buscar: ")
            print("Encontrado." if arvore.buscar(valor) else "Não encontrado.")
        elif opcao == "4":
            valores = arvore.percurso_em_ordem()
            print("Valores em ordem crescente:", valores if valores else "árvore vazia")
        elif opcao == "5":
            print("Legenda: E = esquerda; D = direita; P = preto; V = vermelho.")
            arvore.visualizar()
        elif opcao == "6":
            mostrar_estatisticas(arvore)
        elif opcao == "7":
            correta, mensagem = validar(arvore)
            print(("APROVADA: " if correta else "FALHA: ") + mensagem)
        elif opcao == "8":
            texto = input("Digite inteiros separados por espaço ou vírgula: ").strip()
            partes = texto.replace(",", " ").split()
            if not partes:
                print("Nenhum identificador informado.")
                continue
            try:
                valores = [int(parte) for parte in partes]
            except ValueError:
                print("Lista inválida: utilize apenas números inteiros.")
                continue
            inseridos = 0
            for valor in valores:
                if not arvore.buscar(valor):
                    arvore.inserir(valor)
                    inseridos += 1
            print(f"Inseridos: {inseridos}; repetidos ignorados: {len(valores) - inseridos}.")
        elif opcao == "9":
            confirma = ler_opcao("Apagar os dados desta árvore? (s/n): ", {"s", "n"})
            if confirma == "s":
                arvore = type(arvore)()
                print("Árvore reiniciada.")


# Testar casos
def criar_cenarios():
    base = list(range(1, 101))
    aleatorios = base.copy()
    random.Random(2026).shuffle(aleatorios)
    return {
        "Crescente (100)": base,
        "Decrescente (100)": list(reversed(base)),
        "Embaralhada (100, semente 2026)": aleatorios,
    }


def executar_cenario(classe, valores): # CODIGO FEITO COM IA
    arvore = classe()
    esperados = set()
    inicio = perf_counter()

    for valor in valores:
        arvore.inserir(valor)
        esperados.add(valor)
        correta, mensagem = validar(arvore)
        if not correta:
            raise AssertionError(f"Após inserir {valor}: {mensagem}")

    # Verifica busca existente, busca ausente e tentativa de duplicação
    for valor in valores:
        assert arvore.buscar(valor), f"Busca falhou para {valor}"
    assert not arvore.buscar(999999), "Busca de ausente retornou verdadeiro"
    arvore.inserir(valores[0])
    correta, mensagem = validar(arvore)
    assert correta, mensagem
    assert arvore.percurso_em_ordem() == sorted(esperados), "Duplicado ou ordem incorreta"

    # Mesma sequência de remoções em ambas as árvores -> inclui remoção ausente
    removidos = valores[::4]
    for valor in removidos:
        arvore.remover(valor)
        esperados.remove(valor)
        correta, mensagem = validar(arvore)
        if not correta:
            raise AssertionError(f"Após remover {valor}: {mensagem}")
        assert not arvore.buscar(valor), f"Valor {valor} ainda existe após remoção"
    arvore.remover(999999)
    correta, mensagem = validar(arvore)
    assert correta, mensagem
    assert arvore.percurso_em_ordem() == sorted(esperados), "Elementos finais incorretos"

    duracao_ms = (perf_counter() - inicio) * 1000
    return arvore.obter_estatisticas(), len(esperados), duracao_ms


def comparacao_automatica(): # CODIGO FEITO COM IA
    print("\n" + "=" * 76)
    print("COMPARAÇÃO AUTOMÁTICA: AVL x RUBRO-NEGRA")
    print("Mesmo conjunto, mesma ordem de inserção e mesma ordem de remoção.")
    print("100 inserções, buscas, 1 duplicata, 25 remoções e 1 remoção ausente.")
    print("Cada árvore começa vazia; semente aleatória fixa: 2026.")
    print("=" * 76)

    for nome, valores in criar_cenarios().items():
        print(f"\nCENÁRIO: {nome}")
        print(f"{'Estrutura':<16} {'Nós':>5} {'Altura':>7} {'Rotações':>10} {'Recolorações':>15} {'Tempo(ms)*':>12}")
        print("-" * 76)
        for rotulo, classe in (("AVL", ArvoreAVL), ("Rubro-Negra", ArvoreRN)):
            try:
                dados, quantidade, tempo = executar_cenario(classe, valores)
                recoloracoes = str(dados.get("recoloracoes", "—"))
                print(
                    f"{rotulo:<16} {quantidade:>5} {dados['altura']:>7} "
                    f"{dados['rotacoes']:>10} {recoloracoes:>15} {tempo:>12.3f}"
                )
            except (AssertionError, Exception) as erro:
                print(f"{rotulo:<16} FALHA: {erro}")
        print("-" * 76)


# menu inicial
def menu_principal():
    arvores = {"1": ArvoreAVL(), "2": ArvoreRN()}
    while True:
        print("\n" + "=" * 58)
        print("AMAZON ENGINEERING CHALLENGE - ÁRVORES BALANCEADAS")
        print("1 - Trabalhar com Árvore AVL")
        print("2 - Trabalhar com Árvore Rubro-Negra")
        print("3 - Comparar AVL x Rubro-Negra (testes automáticos)")
        print("0 - Sair")
        opcao = ler_opcao("Escolha: ", {"0", "1", "2", "3"})
        if opcao == "0":
            print("Programa encerrado. Até mais!")
            break
        if opcao == "3":
            comparacao_automatica()
        else:
            nome, _ = TIPOS[opcao]
            arvores[opcao] = menu_arvore(nome, arvores[opcao])


if __name__ == "__main__":
    try:
        menu_principal()
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma encerrado.")
