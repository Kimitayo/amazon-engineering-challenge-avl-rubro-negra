# Amazon Engineering Challenge — Árvores Balanceadas (AVL e Rubro-Negra)

**Disciplina:** IMD0039 — Estruturas de Dados Básicas II (UFRN)  
**Unidade:** II  
**Autor(a):** Clara Virgínia Nascimento Santos  
**Linguagem:** Python 3  

**Texto refeito com uso de IA**

## 1. Contexto e objetivo

Durante a Black Friday, um sistema logístico precisa registrar, consultar e remover identificadores de encomendas com eficiência. Uma árvore binária de busca comum pode ficar degenerada quando recebe valores ordenados, prejudicando o desempenho.

Este projeto implementa **duas árvores binárias de busca balanceadas, AVL e Rubro-Negra**, sem recorrer a bibliotecas prontas de balanceamento. O objetivo é demonstrar suas operações, verificar as propriedades de cada estrutura e comparar seus comportamentos sob as mesmas sequências de dados.

> **Escopo:** protótipo didático executado no terminal. Os identificadores de encomendas são representados por números inteiros; não há integração com sistemas reais da Amazon.

## 2. Funcionalidades

Para **ambas** as árvores, o sistema oferece:

- Inserção, remoção e busca de identificadores;
- Percurso **em ordem** (resultado crescente);
- Visualização textual da estrutura;
- Validação das propriedades de balanceamento;
- Estatísticas de altura e rotações;
- Tratamento de entradas inválidas, identificadores repetidos e elementos inexistentes;
- Comparação automática com conjuntos e operações idênticos.

A visualização da **Rubro-Negra** identifica as cores dos nós. A implementação também contabiliza recolorações.

### Decisões adotadas

- **Valores duplicados:** não são inseridos novamente.
- **Busca por valor ausente:** retorna `False`.
- **Remoção de valor ausente:** mantém a árvore inalterada.
- **Árvore vazia:** consultas, percursos e remoções são tratados sem erro.
- **Identificadores:** números inteiros, inclusive negativos, quando informados pelo usuário.
- **Altura:** convenção da implementação: árvore vazia = 0; nó isolado = 1.
- **Rotações:** contam-se rotações simples; uma rotação dupla da AVL contabiliza duas rotações simples.
- **Recolorações:** contam-se mudanças efetivas de cor na Rubro-Negra, separadamente das rotações.

## 3. Estruturas implementadas

### Árvore AVL

Mantém, para cada nó, o fator de balanceamento **FB = altura(esquerda) − altura(direita)** dentro de `{-1, 0, 1}`. Após inserções e remoções, atualiza alturas e aplica, quando necessário, rotações simples ou duplas (LL, RR, LR e RL).

### Árvore Rubro-Negra

É uma árvore binária de busca que mantém propriedades de coloração: cada nó é vermelho ou preto; a raiz e os nós sentinela `NIL` são pretos; nós vermelhos não possuem filhos vermelhos; e todos os caminhos de um nó até seus descendentes `NIL` contêm a mesma quantidade de nós pretos. As operações usam rotações e recolorações para preservar essas propriedades.

Em ambas as estruturas, busca, inserção e remoção possuem complexidade assintótica **O(log n)** quando as invariantes são mantidas.

## 4. Organização do projeto

```text
amazon-engineering-challenge/
├── main.py                   # Menu interativo e comparação no terminal
├── arvore_avl.py             # Implementação da árvore AVL
├── arvore_rubro_negra.py     # Implementação da árvore Rubro-Negra
├── comparar_arvores.py       # Experimentos e exportação CSV
├── resultados_comparacao.csv # Gerado ao executar a comparação
├── testes/
│   ├── teste_avl.py          # Testes específicos da AVL
│   ├── teste_rubro_negra.py  # Testes específicos da Rubro-Negra
│   └── test_arvores.py       # Testes comparativos das duas estruturas
└── README.md
```


## 5. Requisitos e execução

- Python 3 instalado e disponível no terminal;
- Nenhuma dependência externa é necessária: o projeto utiliza apenas a biblioteca padrão do Python.

Abra um terminal **na pasta principal do projeto**.

### Executar o programa interativo

```bash
python main.py
```

No menu principal, escolha:

```text
1 - Trabalhar com Árvore AVL
2 - Trabalhar com Árvore Rubro-Negra
3 - Comparar AVL x Rubro-Negra (testes automáticos)
0 - Sair
```

Nos menus das árvores, é possível inserir, remover, buscar, percorrer em ordem, visualizar, validar, consultar estatísticas e reiniciar a estrutura.

### Executar os testes separadamente

**AVL:**

```bash
python testes/teste_avl.py
```

**Rubro-Negra:**

```bash
python -m unittest discover -s testes -p "teste_rubro_negra.py" -v
```

**Testes comparativos:**

```bash
python -m unittest discover -s testes -p "test_arvores.py" -v
```

> Nos testes comparativos, oito testes da classe-base `ContratoArvores` são ignorados intencionalmente (`skipped`); os testes concretos das duas estruturas são executados normalmente.

### Gerar a tabela comparativa em CSV

```bash
python comparar_arvores.py
```

O script cria ou atualiza **`resultados_comparacao.csv`**, com dados como alturas após inserção e remoção, rotações acumuladas e recolorações da Rubro-Negra. O arquivo usa `;` como separador e pode ser aberto em programas de planilhas.

## 6. Metodologia de testes

Foram avaliados os seguintes casos:

1. Inserções crescentes, decrescentes e embaralhadas;
2. Busca de identificadores presentes e ausentes;
3. Inserção de duplicados;
4. Remoção de folhas, nós com um filho e nós com dois filhos;
5. Remoção de identificadores inexistentes;
6. Árvores vazias e com um único elemento;
7. Sequências de inserções e remoções, inclusive operações aleatórias reproduzíveis;
8. Verificação das propriedades de balanceamento e da ordenação do percurso em ordem.

Para a comparação, ambas as árvores recebem **os mesmos 100 identificadores** em cada cenário, na mesma ordem, e passam pelas mesmas remoções. O cenário embaralhado utiliza a **semente 2026**, permitindo reproduzir os experimentos.

### Resultado da execução dos testes

Resultados observados na execução local do projeto:

| Conjunto | Resultado |
|---|---|
| Testes específicos da AVL | Aprovados |
| Testes específicos da Rubro-Negra | **11 testes aprovados** |
| Testes comparativos | **16 testes aprovados**, 8 ignorados intencionalmente |

Esses resultados validam os cenários executados, mas não constituem prova formal de ausência de erros.

## 7. Resultados comparativos

A tabela abaixo apresenta **altura final e rotações acumuladas após inserções e remoções** para cada cenário. São resultados observados na execução local de `comparar_arvores.py`.

| Ordem de inserção | Altura AVL | Altura Rubro-Negra | Rotações AVL | Rotações Rubro-Negra |
|---|---:|---:|---:|---:|
| Crescente | 7 | 7 | 94 | 94 |
| Decrescente | 7 | 7 | 94 | 94 |
| Embaralhada (semente 2026) | 7 | 8 | 82 | 65 |

**Interpretação:**

- Nas inserções crescentes e decrescentes, as duas implementações terminaram com a mesma altura e a mesma contagem de rotações.
- No cenário embaralhado, a AVL terminou com altura **7**, enquanto a Rubro-Negra terminou com altura **8**.
- Nesse cenário, a Rubro-Negra realizou **17 rotações a menos** que a AVL (aproximadamente **20,7%** menos).
- A Rubro-Negra também pode realizar **recolorações**, que são ajustes diferentes de rotações e devem ser analisados separadamente no CSV.

**Limitação da comparação:** a contagem de rotações não mede, isoladamente, o tempo de execução. Os resultados dependem das sequências testadas e das implementações utilizadas. Não é correto concluir que uma estrutura sempre será mais rápida ou fará menos rotações.

## 8. Análise e recomendação técnica

A **AVL** impõe um balanceamento mais rígido, o que pode favorecer aplicações com muitas consultas e poucas modificações. Em contrapartida, manter esse equilíbrio pode exigir rotações adicionais.

A **Rubro-Negra** utiliza regras de cores e altura-preta, permitindo maior flexibilidade estrutural. Pode ser uma escolha interessante em sistemas com inserções e remoções frequentes, embora também realize rotações e recolorações.

**Recomendação para o cenário investigado:** considerando que o protótipo de logística envolve **inserções, buscas e remoções frequentes**, a **Rubro-Negra é uma candidata adequada**. No experimento embaralhado, ela realizou menos rotações, mantendo uma altura próxima à da AVL. Essa recomendação é **condicionada aos cenários testados**; para uma decisão de produção seriam necessários experimentos adicionais com cargas representativas, medições de tempo e memória e análise dos requisitos reais do sistema.

## 9. Referências

- CORMEN, Thomas H.; LEISERSON, Charles E.; RIVEST, Ronald L.; STEIN, Clifford. **Algoritmos: Teoria e Prática**. Material-base da disciplina; capítulos sobre árvores binárias de busca e árvores vermelho-pretas.
- **Trabalho da Unidade II — Amazon Engineering Challenge: Árvores Balanceadas (AVL e Rubro-Negra)**. Enunciado da atividade, IMD0039.


