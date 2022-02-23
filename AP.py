import sys

class AP:
    '''
        Um autômato de pilja é uma sextupla (K, sigma, gama, delta, s, F) onde:
            - K é o conjunto de estados
            - sigma é o conjunto de símbolos de entrada
            - gama é o conjunto de símbolos da pilha
            - delta é a função de transição
            - s é o estado inicial
            - F é o conjunto de estados finais
    '''
    def __init__(self, K=[], sigma=[], gama=[], delta=[], s=None, F=[], name=''):
        self.K = K
        self.sigma = sigma
        self.gama = gama
        self.delta = delta
        self.s = s
        self.F = F

        self.name = name

    '''
        Retorna transição de "state" por "sigmaSymbol"
        com "gamaSymbol no topo da lista
    '''
    def getTransition(self, state, sigmaSymbol, gamaSymbol):
        transition = []
        for t in self.delta:
            if t[0] == state and t[1] == sigmaSymbol and t[2] == gama:
                transition.append(t[3])
        return transition

    '''
        Retorna uma tupla (estado, gamaSymbol) que transitam para 
        "state" por "sigmaSymbol", aonde gamaSymbol é o símbolo da
        pilha que leva à transição.
    '''
    def getReverseTransition(self, state, sigmaSymbol, gamaSymbol):
        transition = []
        for t in self.delta:
            if t[3][0] == state and t[1] == sigmaSymbol:
                transition.append(tuple(t[0], t[2]))
        return transition

 
