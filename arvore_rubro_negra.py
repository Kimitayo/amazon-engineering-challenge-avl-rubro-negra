VERMELHO = "VERMELHO"
PRETO = "PRETO"

# Classe nó da rubro negra
class NoRN:
    def __init__(self, valor, cor=VERMELHO):
        self.valor = valor
        self.cor = cor
        self.esquerda = None
        self.direita = None
        self.pai = None

# Classe árvore rubro negra
class ArvoreRN:
    def __init__(self):
        self.NIL = NoRN(None, PRETO)
        self.NIL.esquerda = self.NIL
        self.NIL.direita = self.NIL
        self.NIL.pai = self.NIL
        self.raiz = self.NIL
        self.total_rotacoes = 0
        self.total_recoloracoes = 0

    def _definir_cor(self, no, cor):
        if no is self.NIL:
            return
        if no.cor != cor:
            no.cor = cor
            self.total_recoloracoes += 1

    # ROTAÇÃO
    # Rotação a esquerda RR
    def rotacao_esquerda(self, no):
        nova_raiz = no.direita
        no.direita = nova_raiz.esquerda
        if nova_raiz.esquerda is not self.NIL:
            nova_raiz.esquerda.pai = no
        nova_raiz.pai = no.pai
        if no.pai is self.NIL:
            self.raiz = nova_raiz
        elif no is no.pai.esquerda:
            no.pai.esquerda = nova_raiz
        else:
            no.pai.direita = nova_raiz
        nova_raiz.esquerda = no
        no.pai = nova_raiz
        self.total_rotacoes += 1

    # Rotação a direita LL
    def rotacao_direita(self, no):
        nova_raiz = no.esquerda
        no.esquerda = nova_raiz.direita
        if nova_raiz.direita is not self.NIL:
            nova_raiz.direita.pai = no
        nova_raiz.pai = no.pai
        if no.pai is self.NIL:
            self.raiz = nova_raiz
        elif no is no.pai.direita:
            no.pai.direita = nova_raiz
        else:
            no.pai.esquerda = nova_raiz
        nova_raiz.direita = no
        no.pai = nova_raiz
        self.total_rotacoes += 1

    # Inserção
    def inserir(self, valor):
        pai = self.NIL
        atual = self.raiz
        while atual is not self.NIL:
            pai = atual
            if valor < atual.valor:
                atual = atual.esquerda
            elif valor > atual.valor:
                atual = atual.direita
            else:
                return False  # Não insere duplicados

        novo = NoRN(valor, VERMELHO)
        novo.esquerda = self.NIL
        novo.direita = self.NIL
        novo.pai = pai

        if pai is self.NIL:
            self.raiz = novo
        elif valor < pai.valor:
            pai.esquerda = novo
        else:
            pai.direita = novo

        self._corrigir_insercao(novo)
        return True

    def _corrigir_insercao(self, no):
        while no.pai.cor == VERMELHO:
            if no.pai is no.pai.pai.esquerda:
                tio = no.pai.pai.direita
                if tio.cor == VERMELHO:
                    self._definir_cor(no.pai, PRETO)
                    self._definir_cor(tio, PRETO)
                    self._definir_cor(no.pai.pai, VERMELHO)
                    no = no.pai.pai
                else:
                    if no is no.pai.direita:
                        no = no.pai
                        self.rotacao_esquerda(no)
                    self._definir_cor(no.pai, PRETO)
                    self._definir_cor(no.pai.pai, VERMELHO)
                    self.rotacao_direita(no.pai.pai)
            else:
                tio = no.pai.pai.esquerda
                if tio.cor == VERMELHO:
                    self._definir_cor(no.pai, PRETO)
                    self._definir_cor(tio, PRETO)
                    self._definir_cor(no.pai.pai, VERMELHO)
                    no = no.pai.pai
                else:
                    if no is no.pai.esquerda:
                        no = no.pai
                        self.rotacao_direita(no)
                    self._definir_cor(no.pai, PRETO)
                    self._definir_cor(no.pai.pai, VERMELHO)
                    self.rotacao_esquerda(no.pai.pai)
        self._definir_cor(self.raiz, PRETO)

    # Busca
    def _encontrar_no(self, valor):
        atual = self.raiz
        while atual is not self.NIL:
            if valor == atual.valor:
                return atual
            if valor < atual.valor:
                atual = atual.esquerda
            else:
                atual = atual.direita
        return self.NIL

    def buscar(self, valor):
        return self._encontrar_no(valor) is not self.NIL

    def encontrar_menor(self, no):
        if no is self.NIL:
            return self.NIL
        while no.esquerda is not self.NIL:
            no = no.esquerda
        return no

    def _transplantar(self, antigo, novo):
        if antigo.pai is self.NIL:
            self.raiz = novo
        elif antigo is antigo.pai.esquerda:
            antigo.pai.esquerda = novo
        else:
            antigo.pai.direita = novo
        # O pai do NIL também é atualizado -> necessário na correção da remoção
        novo.pai = antigo.pai

    # Remoção
    def remover(self, valor):
        alvo = self._encontrar_no(valor)
        if alvo is self.NIL:
            return False

        substituido = alvo
        cor_original = substituido.cor

        if alvo.esquerda is self.NIL:
            filho = alvo.direita
            self._transplantar(alvo, alvo.direita)
        elif alvo.direita is self.NIL:
            filho = alvo.esquerda
            self._transplantar(alvo, alvo.esquerda)
        else:
            substituido = self.encontrar_menor(alvo.direita)
            cor_original = substituido.cor
            filho = substituido.direita
            if substituido.pai is alvo:
                filho.pai = substituido
            else:
                self._transplantar(substituido, substituido.direita)
                substituido.direita = alvo.direita
                substituido.direita.pai = substituido
            self._transplantar(alvo, substituido)
            substituido.esquerda = alvo.esquerda
            substituido.esquerda.pai = substituido
            self._definir_cor(substituido, alvo.cor)

        if cor_original == PRETO:
            self._corrigir_remocao(filho)
        return True

    def _corrigir_remocao(self, no):
        while no is not self.raiz and no.cor == PRETO:
            if no is no.pai.esquerda:
                irmao = no.pai.direita
                if irmao.cor == VERMELHO:
                    self._definir_cor(irmao, PRETO)
                    self._definir_cor(no.pai, VERMELHO)
                    self.rotacao_esquerda(no.pai)
                    irmao = no.pai.direita
                if irmao.esquerda.cor == PRETO and irmao.direita.cor == PRETO:
                    self._definir_cor(irmao, VERMELHO)
                    no = no.pai
                else:
                    if irmao.direita.cor == PRETO:
                        self._definir_cor(irmao.esquerda, PRETO)
                        self._definir_cor(irmao, VERMELHO)
                        self.rotacao_direita(irmao)
                        irmao = no.pai.direita
                    self._definir_cor(irmao, no.pai.cor)
                    self._definir_cor(no.pai, PRETO)
                    self._definir_cor(irmao.direita, PRETO)
                    self.rotacao_esquerda(no.pai)
                    no = self.raiz
            else:
                irmao = no.pai.esquerda
                if irmao.cor == VERMELHO:
                    self._definir_cor(irmao, PRETO)
                    self._definir_cor(no.pai, VERMELHO)
                    self.rotacao_direita(no.pai)
                    irmao = no.pai.esquerda
                if irmao.direita.cor == PRETO and irmao.esquerda.cor == PRETO:
                    self._definir_cor(irmao, VERMELHO)
                    no = no.pai
                else:
                    if irmao.esquerda.cor == PRETO:
                        self._definir_cor(irmao.direita, PRETO)
                        self._definir_cor(irmao, VERMELHO)
                        self.rotacao_esquerda(irmao)
                        irmao = no.pai.esquerda
                    self._definir_cor(irmao, no.pai.cor)
                    self._definir_cor(no.pai, PRETO)
                    self._definir_cor(irmao.esquerda, PRETO)
                    self.rotacao_direita(no.pai)
                    no = self.raiz
        self._definir_cor(no, PRETO)

    # Percurso em ordem
    def percurso_em_ordem(self):
        elementos = []

        def percorrer(no):
            if no is self.NIL:
                return
            percorrer(no.esquerda)
            elementos.append(no.valor)
            percorrer(no.direita)

        percorrer(self.raiz)
        return elementos

    # Visualização - Feita com IA
    def visualizar(self):
        if self.raiz is self.NIL:
            print("A árvore está vazia.")
            return

        def desenhar(no, prefixo, ultimo, lado=""):
            if no is self.NIL:
                return
            conector = "└── " if ultimo else "├── "
            cor = "P" if no.cor == PRETO else "V"
            print(f"{prefixo}{conector}{lado}{no.valor} ({cor})")
            novo_prefixo = prefixo + ("    " if ultimo else "│   ")
            filhos = []
            if no.esquerda is not self.NIL:
                filhos.append(("E: ", no.esquerda))
            if no.direita is not self.NIL:
                filhos.append(("D: ", no.direita))
            for indice, (rotulo, filho) in enumerate(filhos):
                desenhar(filho, novo_prefixo, indice == len(filhos) - 1, rotulo)

        desenhar(self.raiz, "", True)

    def obter_altura(self, no=None):
        # Sem argumento, retorna a altura da árvore toda
        if no is None:
            no = self.raiz
        if no is self.NIL:
            return 0
        return 1 + max(self.obter_altura(no.esquerda), self.obter_altura(no.direita))

    # Estatistica pra comparar com a AVL
    def obter_estatisticas(self):
        return {
            "altura": self.obter_altura(),
            "rotacoes": self.total_rotacoes,
            "recoloracoes": self.total_recoloracoes,
        }

    def validar_rn(self):
        """Retorna (válida, mensagem), verificando regras e referências."""
        if self.NIL.cor != PRETO:
            return False, "O nó NIL não é preto"
        if self.raiz is self.NIL:
            return True, "Árvore Rubro-Negra válida"
        if self.raiz.pai is not self.NIL:
            return False, "A raiz possui pai incorreto"
        if self.raiz.cor != PRETO:
            return False, "A raiz não é preta"

        def verificar(no, minimo, maximo):
            if no is self.NIL:
                return True, 1, "OK"
            if no is None:
                return False, 0, "Referência None encontrada no lugar de NIL"
            if minimo is not None and no.valor <= minimo:
                return False, 0, f"Ordenação incorreta no nó {no.valor}"
            if maximo is not None and no.valor >= maximo:
                return False, 0, f"Ordenação incorreta no nó {no.valor}"
            if no.cor not in (VERMELHO, PRETO):
                return False, 0, f"Cor inválida no nó {no.valor}"
            if no.esquerda is None or no.direita is None:
                return False, 0, f"Filho None no nó {no.valor}"
            if no.esquerda is not self.NIL and no.esquerda.pai is not no:
                return False, 0, f"Pai incorreto do filho esquerdo de {no.valor}"
            if no.direita is not self.NIL and no.direita.pai is not no:
                return False, 0, f"Pai incorreto do filho direito de {no.valor}"
            if no.cor == VERMELHO and (
                no.esquerda.cor == VERMELHO or no.direita.cor == VERMELHO
            ):
                return False, 0, f"Dois nós vermelhos consecutivos em {no.valor}"
            ok_e, negros_e, mensagem = verificar(no.esquerda, minimo, no.valor)
            if not ok_e:
                return False, 0, mensagem
            ok_d, negros_d, mensagem = verificar(no.direita, no.valor, maximo)
            if not ok_d:
                return False, 0, mensagem
            if negros_e != negros_d:
                return False, 0, f"Altura negra diferente no nó {no.valor}"
            return True, negros_e + (no.cor == PRETO), "OK"

        valida, _, mensagem = verificar(self.raiz, None, None)
        if valida:
            return True, "Árvore Rubro-Negra válida"
        return False, mensagem


# Nome alternativo para facilitar a identificação da estrutura
ArvoreRubroNegra = ArvoreRN
