# Manipulação de Linguagens Regulares e Linguagens Livres de Contexto

UFSC - INE (Departamento de Informática e Estatística) - <data>

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

## Entrada de dados

### Autômatos
Os autômatos são inseridos em arquivos de texto localizados na pasta "AFs", eles seguem o padrão adotado pelo simulador do site <https://ivanzuzak.info/noam/webapps/fsm_simulator/>.

### Expressões regulares

Expressões regulares são denotadas da seguinte forma:

"|": ou
 
".": contatenação
 
"*": fecho

Ex: (a|b)*.a.b.b
