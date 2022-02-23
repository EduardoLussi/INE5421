import sys
import auxfuncs

class GLC:
    '''
        Uma Gramática Livre de Contexto é uma quadrupla (N, T, P, S) onde:
            - N é o conjunto de símbolos não terminais
            - T é o conjunto de símbolos terminais (o alfabeto)
            - S é o símbolo inicial
            - P é o conjunto de regras de produção, tal que:
                P = { A ::= delta, onde A pertence a N
                    e delta é uma lista de listas de terminais e não-terminais }
                    (cada sublista de delta é uma lista ordenada que representa
                    uma produção)
    '''
    def __init__(self, N=[], T=[], S=None, P=dict(), name=''):
        self.N = N
        self.T = T
        self.S = S
        self.P = P
        
        self.name = name

    '''
        Retorna uma gramática equivalente, sem símbolos improdutívos
    '''
    def removeUnproductiveSymbols(self):
        markedTSymbols = []
        productions = dict()

        productionCount = 0

        while True:
            for nonTerminal, production in [(nonTerm, prod) 
                                                for nonTerm in self.N
                                                for prod in self.P[non-terminal]]:

                if productions[non-terminal] and production in productions[nonTerminal]:
                    break

                nonMarked = copy(production)
                for symbol in production:
                    # remove todas as ocorrências de symbol
                    if symbol in self.T:
                        if symbol not in markedTSymbols:
                            markedTSymbols.append(symbol)
                        continue
                    if symbol not in self.N or not productions[symbol]:
                        continue
                    nonMarked = list(filter(symbol.__ne__,nonMarked)) 

                if not nonMarked:
                    if not productions[nonTerminal]:
                        productions[nonTerminal] = []
                    productions[nonTerminal].append(production)

            currentProductionCount = dict_deep_length(productions)
            if currentProductionCount != productionCount:
                productionCount = currentProductionCount
            else:
                break

        return GLC(productions.keys(), markedTSymbols, self.S, productions, self.name)

