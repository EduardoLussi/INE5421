# Manipulação de Linguagens Regulares e Linguagens Livres de Contexto

UFSC - INE (Departamento de Informática e Estatística) - <data>

### Integrantes do Grupo
  * Eduardo Lussi
  * Paulo Arthur
  * Pedro Aquino
  * Pedro Queiroz

## Detalhes de Implementação

Implementado em Python 3.

## Entrada de dados

### Autômatos
Os autômatos são inseridos em arquivos de texto localizados na pasta "AFs", eles seguem o padrão adotado pelo simulador do site <https://ivanzuzak.info/noam/webapps/fsm_simulator/>.

### Expressões regulares

Expressões regulares são denotadas da seguinte forma:

"|": ou
".": contatenação
"*": fecho

Ex: (a|b)*.a.b.b
