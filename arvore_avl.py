# Classe para o nó
class NoAVL:
    def __init__(self, valor):
        self.valor = valor
        self.esquerda = None
        self.direita = None
        self.altura = 1

# Classe para a árvore avl
class ArvoreAVL:
    def __init__(self):
        self.raiz = None
        self.total_rotacoes = 0 # vai servir pra comparação com a rubro negra

    # Função para altura de um nó -> antes de calcular a altura de um nó
    def obter_altura(self, no):
        if no is None:
            return 0

        return no.altura

    # Cálculo do fator de balanceamento
    ## altura arvore esquerda - altura arvore direita
    def fator_balanceamento(self, no):
        if no is None:
            return 0

        altura_esquerda = self.obter_altura(no.esquerda)
        altura_direita = self.obter_altura(no.direita)

        return altura_esquerda - altura_direita

    # Função para atualizar a altura de um nó
    def atualizar_altura(self, no):
        if no is None:
            return

        altura_esquerda = self.obter_altura(no.esquerda)
        altura_direita = self.obter_altura(no.direita)

        no.altura = 1 + max(altura_esquerda, altura_direita)


    # BALANCEAMENTO

    # Rotação simples
    # Rotação a direita LL
    def rotacao_direita(self, no):
        nova_raiz = no.esquerda
        subarvore_temporaria = nova_raiz.direita

        nova_raiz.direita = no
        no.esquerda = subarvore_temporaria

        self.atualizar_altura(no)
        self.atualizar_altura(nova_raiz)

        # Registra uma rotação simples
        self.total_rotacoes += 1

        return nova_raiz

    # Rotação a esquerda RR
    def rotacao_esquerda(self, no):
        nova_raiz = no.direita
        subarvore_temporaria = nova_raiz.esquerda

        nova_raiz.esquerda = no
        no.direita = subarvore_temporaria

        self.atualizar_altura(no)
        self.atualizar_altura(nova_raiz)

        # Registra uma rotação simples
        self.total_rotacoes += 1

        return nova_raiz

    # Rotação dupla
    # Rotação a esquerda direita LR
    def rotacao_esquerda_direita(self, no):
        no.esquerda = self.rotacao_esquerda(no.esquerda)

        return self.rotacao_direita(no)

    # Rotação a direita esquerda RL
    def rotacao_direita_esquerda(self, no):
        no.direita = self.rotacao_direita(no.direita)

        return self.rotacao_esquerda(no)

    
    # Fazer o rebalanceamento de um nó
    def rebalancear(self, no):
        if no is None:
            return None

        # Atualiza a altura do nó
        self.atualizar_altura(no)

        # Calcula o fator de balanceamento
        fb = self.fator_balanceamento(no)

        # Desequilíbrio para a esquerda
        if fb > 1:

            # Caso LL
            if self.fator_balanceamento(no.esquerda) >= 0:
                return self.rotacao_direita(no)

            # Caso LR
            else:
                return self.rotacao_esquerda_direita(no)

        # Desequilíbrio para a direita
        if fb < -1:

            # Caso RR
            if self.fator_balanceamento(no.direita) <= 0:
                return self.rotacao_esquerda(no)

            # Caso RL
            else:
                return self.rotacao_direita_esquerda(no)

        # Se estiver balanceado -> não precisa de rotação
        return no

    # Função de inserção
    def inserir(self, valor):
        self.raiz = self._inserir_recursivo(self.raiz, valor)


    def _inserir_recursivo(self, no, valor):

        # Caso base: encontramos uma posição vazia
        if no is None:
            return NoAVL(valor)

        # Se o valor for menor, seguimos pela esquerda
        if valor < no.valor:
            no.esquerda = self._inserir_recursivo(no.esquerda, valor)

        # Se o valor for maior, seguimos pela direita
        elif valor > no.valor:
            no.direita = self._inserir_recursivo(no.direita, valor)

        # Se o valor já existir, não inserimos novamente
        else:
            return no

        # Atualiza a altura e corrige possíveis desequilíbrios
        return self.rebalancear(no)


    # Função de busca
    def buscar(self, valor):
        return self._buscar_recursivo(self.raiz, valor)


    def _buscar_recursivo(self, no, valor):

        # Caso base: chegamos a uma posição vazia
        if no is None:
            return False

        # Encontramos o valor
        if valor == no.valor:
            return True

        # O valor procurado é menor
        if valor < no.valor:
            return self._buscar_recursivo(no.esquerda, valor)

        # O valor procurado é maior
        return self._buscar_recursivo(no.direita, valor)

    # Função de percurso em ordem -> pra saber qual nó visitar primeiro, definir um percurso
    def percurso_em_ordem(self):
        elementos = []
        self._percurso_em_ordem_recursivo(self.raiz, elementos)
        return elementos


    def _percurso_em_ordem_recursivo(self, no, elementos):
        if no is None:
            return

        # 1. Percorre a subarvore esquerda
        self._percurso_em_ordem_recursivo(no.esquerda, elementos)

        # 2. Registra o valor do nó atual
        elementos.append(no.valor)

        # 3. Percorre a subarvore direita
        self._percurso_em_ordem_recursivo(no.direita, elementos)


    # Método de visualização (feito totalmente com uso de IA)
    def visualizar(self):
        if self.raiz is None:
            print("A árvore está vazia.")
            return

        self._visualizar_recursivo(self.raiz, "", True)


    def _visualizar_recursivo(self, no, prefixo, ultimo, lado=""):
        if no is None:
            return

        # Escolhe o símbolo que será exibido
        conector = "└── " if ultimo else "├── "

        # Calcula as informações do nó
        altura = self.obter_altura(no)
        fb = self.fator_balanceamento(no)

        # Exibe o nó atual
        print(f"{prefixo}{conector}{lado}{no.valor} (h={altura}, FB={fb})")

        # Monta o prefixo para os próximos níveis
        novo_prefixo = prefixo + ("    " if ultimo else "│   ")

        # Identifica os filhos existentes
        filhos = []

        if no.esquerda is not None:
            filhos.append(("E: ", no.esquerda))

        if no.direita is not None:
            filhos.append(("D: ", no.direita))

        # Exibe recursivamente os filhos
        for indice, (lado_filho, filho) in enumerate(filhos):
            eh_ultimo = indice == len(filhos) - 1

            self._visualizar_recursivo(
                filho,
                novo_prefixo,
                eh_ultimo,
                lado_filho
            )


    # Função de remoção de nó
    def encontrar_menor(self, no):
        atual = no

        while atual.esquerda is not None:
            atual = atual.esquerda

        return atual


    def remover(self, valor):
        self.raiz = self._remover_recursivo(self.raiz, valor)


    def _remover_recursivo(self, no, valor):

        # Caso 1: valor não encontrado
        if no is None:
            return None

        # Procura o valor na subárvore esquerda
        if valor < no.valor:
            no.esquerda = self._remover_recursivo(no.esquerda, valor)

        # Procura o valor na subárvore direita
        elif valor > no.valor:
            no.direita = self._remover_recursivo(no.direita, valor)

        # Encontramos o nó que deve ser removido
        else:

            # Nó sem filho esquerdo
            if no.esquerda is None:
                return no.direita

            # Nó sem filho direito
            if no.direita is None:
                return no.esquerda

            # Nó com dois filhos
            sucessor = self.encontrar_menor(no.direita)

            # Substitui o valor pelo sucessor
            no.valor = sucessor.valor

            # Remove o sucessor original
            no.direita = self._remover_recursivo(
                no.direita,
                sucessor.valor
            )

        # Atualiza a altura e rebalanceia a subárvore
        return self.rebalancear(no)


    # Função de validação da árvore AVL -> Feita totalmente com uso de IA
    def validar_avl(self):
        valida, _, mensagem = self._validar_avl_recursivo(
            self.raiz,
            None,
            None
        )

        return valida, mensagem


    def _validar_avl_recursivo(self, no, minimo, maximo):

        # Caso base: uma subárvore vazia é válida
        if no is None:
            return True, 0, "Subárvore válida"

        # Verifica a propriedade da árvore binária de busca
        if minimo is not None and no.valor <= minimo:
            return False, 0, f"Erro de ordenação no nó {no.valor}"

        if maximo is not None and no.valor >= maximo:
            return False, 0, f"Erro de ordenação no nó {no.valor}"

        # Valida a subárvore esquerda
        esquerda_valida, altura_esquerda, mensagem = (
            self._validar_avl_recursivo(
                no.esquerda,
                minimo,
                no.valor
            )
        )

        if not esquerda_valida:
            return False, 0, mensagem

        # Valida a subárvore direita
        direita_valida, altura_direita, mensagem = (
            self._validar_avl_recursivo(
                no.direita,
                no.valor,
                maximo
            )
        )

        if not direita_valida:
            return False, 0, mensagem

        # Calcula a altura real do nó
        altura_calculada = 1 + max(
            altura_esquerda,
            altura_direita
        )

        # Verifica se a altura armazenada está correta
        if no.altura != altura_calculada:
            return (
                False,
                altura_calculada,
                f"Altura incorreta no nó {no.valor}"
            )

        # Calcula o fator de balanceamento real
        fb = altura_esquerda - altura_direita

        # Verifica a propriedade AVL
        if abs(fb) > 1:
            return (
                False,
                altura_calculada,
                f"Desbalanceamento no nó {no.valor}: FB={fb}"
            )

        return True, altura_calculada, "Árvore AVL válida"


    # Função para obter estatísticas da árvore  -> servirá para comparação com a rubro negra
    def obter_estatisticas(self):
        return {
            "altura": self.obter_altura(self.raiz),
            "rotacoes": self.total_rotacoes
        }