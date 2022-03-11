# Manipulação de Linguagens Regulares e Linguagens Livres de Contexto

UFSC - INE (Departamento de Informática e Estatística) - 2022

### Integrantes do Grupo
  * Eduardo Lussi
  * Paulo Arthur
  * Pedro Aquino
  * Pedro Queiroz

## Detalhes de Implementação

Implementado em Python 3. Para abrir o programa, basta executar "python Main.py" no terminal.

O código está bem documentado e detalhes dos algoritmos podem ser encontrados lá.

### Estrutura do Autômato: AF.py

Um autômato finito é uma quíntupla (K, sigma, delta, s, F) onde:

  - K é o conjunto de estados (strings)

  - sigma é o conjunto de símbolos de entrada (strings)

  - delta é a função de transição (tripla (estado, símbolo, próximo estado))

  - s é o estado inicial (string)

  - F é o conjunto de estados finais (strings)

### Estrutura Tree: Tree.py

Tree é uma árvore sintática utilizada na conversão ER -> AFD.

### Estrutura de Gramática: GLC.py

Uma Gramática Livre de Contexto é uma quadrupla (N, T, P, S) onde:

  - N é o conjunto de símbolos não terminais
  
  - T é o conjunto de símbolos terminais (o alfabeto)
  
  - S é o símbolo inicial
  
  - P é o conjunto de regras de produção, tal que:
    
    P = { A ::= delta, onde A pertence a N e delta é uma lista de listas de terminais e não-terminais } (cada sublista de delta é uma lista ordenada que representa uma produção)
    
    Ex: P = {'S': [['S', 'or', 'A'], ['A']], 'A': [['A', 'and', 'B'], ['B']], ...}

## Entrada de dados

### Autômatos

Os autômatos são inseridos em arquivos de texto localizados na pasta "testes", eles seguem o padrão adotado pelo simulador do site <https://ivanzuzak.info/noam/webapps/fsm_simulator/>. Esse padrão é de fácil compreensão e já existem vários exemplos prontos na pasta "testes".

### Expressões regulares

Expressões regulares são denotadas da seguinte forma:

"|": ou
 
".": contatenação
 
"*": fecho

Ex: (a|b)*.a.b.b

### Gramáticas

As gramáticas são inseridas em arquivos de texto localizados na pasta "testes", eles seguem um padrão bastante simples e intuitivo. Há vários exemplos prontos na pasta "testes", basta seguir o padrão.

### Sentenças

As sentenças são inseridas com espaços entre os terminais.

Ex: not ( true or false ) and true