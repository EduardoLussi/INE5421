import sys
from itertools import product

from Tree import Node


class AF:
    """
        Um autômato finito é uma quíntupla (K, sigma, delta, s, F) onde:
            - K é o conjunto de estados
            - sigma é o conjunto de símbolos de entrada
            - delta é a função de transição
            - s é o estado inicial
            - F é o conjunto de estados finais
    """

    def __init__(self, K=[], sigma=[], delta=[], s=None, F=[], name=''):
        self.K = K
        self.sigma = sigma
        self.delta = delta
        self.s = s
        self.F = F

        self.name = name

    def getTransition(self, state, symbol):
        """Retorna transição de "state" por 'symbol'"""
        transition = []
        for t in self.delta:
            if t[0] == state and t[1] == symbol:
                transition.append(t[2])
        return transition

    def getReverseTransition(self, state, symbol):
        """Retorna estados que transitam para 'state' por 'symbol'"""
        transition = []
        for t in self.delta:
            if t[2] == state and t[1] == symbol:
                transition.append(t[0])
        return transition

    def compute(self, input):
        """Reconhecimento de sentença pelo AF"""
        entrada = input
        currentStates = []
        currentStates.append(self.s)
        currentStates.extend(self.getEpsilonTransition(currentStates))
        while len(entrada) > 0:
            symbol = entrada[0]
            entrada = entrada[1:]
            nextStates = []
            for state in currentStates:
                transition = self.getTransition(state, symbol)
                transition.extend(self.getEpsilonTransition(transition))
                nextStates.extend(transition)
            currentStates = nextStates
        for state in currentStates:
            if state in self.F:
                return True
        return False

    def plot(self):
        """Imprime autômato"""
        text = 'δ'
        for symbol in self.sigma:  # Primeira linha
            text += '|' + symbol
        text += '\n'

        for state in self.K:  # Cria demais linhas
            strState = ''
            if state == self.s:
                strState += '>'
            if state in self.F:
                strState += '*'
            strState += state

            text += strState
            for symbol in self.sigma:
                transition = self.getTransition(state, symbol)
                strTransition = str(transition).replace("'", '').strip()
                strTransition = strTransition.replace('[', '{').replace(']', '}')
                if len(transition) == 0:
                    text += '|-'
                elif len(transition) == 1:
                    text += '|' + strTransition[1:-1]
                else:
                    text += "|" + strTransition
            text += '\n'

        # Obtém lista de elementos em cada linha e cada coluna
        textLines = text.split('\n')[:-1]
        for i, line in enumerate(textLines):
            textLines[i] = line.split('|')

        # Obtém tamanhos máximos de cada coluna
        columnSizes = []
        for i in range(len(textLines[0])):
            maxColumnSize = 0
            for line in textLines:
                if len(line[i]) > maxColumnSize:
                    maxColumnSize = len(line[i])
            columnSizes.append(maxColumnSize + 2)

        # Cria texto de impressão final com espaçamentos dinâmicos
        text = ''
        for line in textLines:
            for i, val in enumerate(line):
                textVal = val
                for j in range(columnSizes[i] - len(textVal)):
                    if j % 2 == 0:
                        textVal = textVal + ' '
                    else:
                        textVal = ' ' + textVal
                text += textVal + '|'
            text = text[:-1] + '\n'

        print(text)

    def getEpsilonTransition(self, state):
        """Retorna transições por epsilon a partir de 'state'"""
        for k in state:
            epsilonTransition = self.getTransition(k, '&')
            for t in epsilonTransition:
                if t not in state:
                    state.append(t)
        return state

    def getAFD(self):
        """A partir de "self", retorna um AFD equivalente"""
        # Verifica se autômato já é determinístico
        if '&' not in self.sigma:
            breakFor = False
            for state in self.K:
                for s in self.sigma:
                    if len(self.getTransition(state, s)) > 1:
                        breakFor = True
                        break
                if breakFor:
                    break
        if breakFor is False:
            return self

        K = [[self.s]]
        sigma = self.sigma.copy()

        if '&' in sigma:  # Remove epsilon
            sigma.remove('&')

        delta = []
        s = f"{'{'}"
        for state in self.getEpsilonTransition([self.s]):
            s += f"{state}, "
        s = s[:-2] + f"{'}'}"
        F = []

        # Obtém transições por epsilon para o estado inicial
        K[0] = self.getEpsilonTransition(K[0])

        for k in K:  # A cada novo estado
            for symbol in self.sigma:  # Para cada símbolo do alfabeto
                if symbol == '&':
                    continue

                newState = []
                for state in k:  # Para cada transição do símbolo
                    for t in self.getTransition(state, symbol):  # Calcula o novo estado
                        if t not in newState:
                            newState.append(t)

                # Obtém transições por epsilon para o novo estado
                newState = self.getEpsilonTransition(newState)

                if not len(newState):
                    continue

                # Insere transição convertida para string
                strk = str(k).replace("'", '').replace('[', '{').replace(']', '}')
                strNewState = str(newState).replace("'", '').replace('[', '{').replace(']', '}')
                delta.append((strk, symbol, strNewState))

                for k0 in K:  # Insere novo estado se ele ainda não existir
                    if set(newState) == set(k0):
                        break
                    if k0 == K[-1]:
                        K.append(newState)

        for k in K:  # Define estados finais
            for f in self.F:
                if f in k:
                    F.append(k)
                    break

        for i, k in enumerate(K):  # Converte estados para string
            K[i] = str(k).replace("'", '').replace('[', '{').replace(']', '}')

        for i, f in enumerate(F):  # Converte estados finais para string
            F[i] = str(f).replace("'", '').replace('[', '{').replace(']', '}')

        return AF(K, sigma, delta, s, F)

    def readData(self, file_name):
        """Lê os dados do AF a partir de um arquivo"""
        with open(file_name) as f:
            # states
            line = f.readline()
            states = []
            while True:
                line = f.readline().rstrip('\n')
                if line[0] == '#':
                    break
                states.append(line)
            self.K = states

            # initial
            self.s = f.readline().rstrip('\n')

            # accepting
            f.readline()
            accepStates = []
            while True:
                line = f.readline().rstrip('\n')
                if line[0] == '#':
                    break
                accepStates.append(line)
            self.F = accepStates

            # alphabet
            alphabet = []
            while True:
                line = f.readline().rstrip('\n')
                if line[0] == '#':
                    break
                alphabet.append(line)
            self.sigma = alphabet

            # transitions
            fileDelta = []
            while True:
                line = f.readline().rstrip('\n')
                if line == '':
                    break
                line = line.split(":")
                state = line[0]
                line = line[1].split(">")
                elem = line[0]
                nxtState = line[1]
                fileDelta.append((state, elem, nxtState))
            self.delta = fileDelta

    def minimize(self):
        """A partir de "self", retorna um AF minimizado equivalente"""
        print("Autômato original:")
        self.plot()

        # Determiniza o autômato
        AFD = self.getAFD()

        # print("states before minimization: ", AFD.K)

        # Elimina estados inalcancaveis
        unreachableStates = AFD.K.copy()
        unreachableStates.remove(AFD.s)
        nextStates = [AFD.s]
        while nextStates:
            currentState = nextStates.pop()
            for symbol in AFD.sigma:
                for s in AFD.getTransition(currentState, symbol):
                    if s in unreachableStates:
                        unreachableStates.remove(s)
                        nextStates.append(s)
        reachableStates = list(set(AFD.K.copy()).difference(set(unreachableStates)))
        # print("reachableStates: {0}".format(reachableStates))

        # Elimina estados mortos
        aliveStates = AFD.F.copy()
        nextStates = aliveStates.copy()
        while nextStates:
            currentState = nextStates.pop()
            for symbol in AFD.sigma:
                for s in AFD.getReverseTransition(currentState, symbol):
                    if s not in aliveStates:
                        aliveStates.append(s)
                        nextStates.append(s)
        aliveAndReachableStates = list(set(aliveStates).intersection(set(reachableStates)))
        # print("aliveAndReachableStates: {0}".format(aliveAndReachableStates))

        # Constroi classes de equivalencia
        '''
        Definicao:
        Um conjunto de estados pertencem a memsa classe de equivalencia se
        para cada simbolo, a transicao de cada estado do conjunto pelo simbolo
        resulta a elementos de uma mesma classe de equivalencia.

        Algoritmo: ToExplain
        '''
        eqClasses = [set(aliveAndReachableStates).difference(set(AFD.F)), \
                     set(AFD.F).intersection(set(aliveAndReachableStates))]
        while True:
            newEqClasses = []
            subdivisions = [[[] for col in range(len(eqClasses))] for col in range(len(AFD.sigma))]
            for idxsymb, symbol in enumerate(AFD.sigma):
                for state in aliveAndReachableStates:
                    target = AFD.getTransition(state, symbol)
                    if len(target) == 0:
                        continue
                    target = target[0]
                    for idxclss, eqClass in enumerate(eqClasses):
                        if target in eqClass:
                            subdivisions[idxsymb][idxclss].append(state)
                            break
                    else:
                        print("Minimization: something went wrong with equivalence class construction.",
                              file=sys.stderr)
            subdivisionsIterator = iter(subdivisions)
            comulativeEqClasses = next(subdivisionsIterator)
            for symbolGroup in subdivisionsIterator:
                newComulativeEqClasses = [set(partialEqClassA).intersection(set(partialEqClassB)) \
                                          for partialEqClassA in symbolGroup for partialEqClassB in comulativeEqClasses \
                                          if set(partialEqClassA).intersection(set(partialEqClassB))]
                comulativeEqClasses = newComulativeEqClasses

            if len(comulativeEqClasses) - len(eqClasses) == 0:
                eqClasses = comulativeEqClasses
                break
            else:
                eqClasses = comulativeEqClasses

        # print("Eq Classes: {0}".format(eqClasses))
        # Constroi Automato
        newK = [str(eqClass) for eqClass in eqClasses]
        newS = ""
        for eqClass in eqClasses:
            if AFD.s in eqClass:
                newS = str(eqClass)
                break
        newF = [str(eqClassWithF) for f in set(AFD.F).intersection(set(aliveAndReachableStates)) \
                for eqClassWithF in eqClasses if f in eqClassWithF]
        newDelta = []
        for eqClass in eqClasses:
            for symbol in AFD.sigma:
                target = AFD.getTransition(list(eqClass)[0], symbol)[0]
                for otherEqClass in eqClasses:
                    if target in otherEqClass:
                        transition = [str(eqClass), symbol, str(otherEqClass)]
                        newDelta.append(transition)
                        break

        # Formatação dos nomes dos estados
        for n in [newK, newF]:
            for i, k in enumerate(n):
                n[i] = str(k).replace("'", "").replace('"', "")
        for delta in newDelta:
            for i, k in enumerate(delta):
                delta[i] = str(k).replace("'", "").replace('"', "")
        newS = str(newS).replace("'", "").replace('"', "")

        return AF(newK, self.sigma, newDelta, newS, newF)

    def readRegex(self, regex):
        """Cria autômato a partir de expressão regular"""
        regex = f"({regex}).#"
        tree = Node.getTree(regex)  # Obtém árvore sintática
        tree.calculateFollowpos()  # Calcula followpos dos nós

        # Inicializa Dstates contendo somente o estado desmarcado firstpos(root)
        Dstates = [tree.getFirstpos()]
        S = [tree.getFirstpos()]
        Dtran = []
        allSymbols = set()
        unmarked = [tree.getFirstpos()]
        while len(unmarked) != 0:  # Enquanto houver um símbolo desmarcado S em Dstates
            S = unmarked.pop(0)  # Marque S

            # Cria lista de símbolos
            symbols = set()
            for a in S:
                symbols = symbols.union(set([a.name]))

            allSymbols = allSymbols.union(symbols)

            for a in symbols:  # Para cada símbolo de entrada a
                U = set()  # Seja U,
                for p in S:  # para cada p em S
                    if p.name == a:  # que corresponde a a,
                        U = U.union(p.followpos)  # a união de followpos(p)
                if U not in Dstates:  # Se U não está em Dstates
                    Dstates.append(U)  # Adicione U como estado desmarcado de Dstates
                    unmarked.append(U)
                if (S, a, U) not in Dtran:  # Insere transição
                    Dtran.append((S, a, U))

        for transition in Dtran:  # Remove estado morto de #
            state, symbol, next = transition
            if symbol == '#':
                Dstates.remove(next)
                break

        # Criar autômato com estados renomeados
        self.K = [f"q{i}" for i in range(len(Dstates))]
        self.S = self.K[0]
        self.delta = []
        self.F = []

        for transition in Dtran:
            state, symbol, next = transition

            strState = self.K[Dstates.index(state)]
            if symbol == '#':
                if strState not in self.F:
                    self.F.append(strState)
            else:
                newTransition = (strState, symbol, self.K[Dstates.index(next)])
                self.delta.append(newTransition)
        self.sigma = list(allSymbols)
        self.sigma.remove('#')

        self = self.getAFD()

    def exportAF(self, file_name):
        """Exporta o Autômato para um arquivo"""
        file = open(file_name, "w")
        file.write("#states\n")
        for state in self.K:
            file.write(f"{state}\n")
        file.write("#initial\n")
        file.write(f"{self.s}\n")
        file.write("#accepting\n")
        for acept in self.F:
            file.write(f"{acept}\n")
        file.write("#alphabet\n")
        for alph in self.sigma:
            file.write(f"{alph}\n")
        file.write("#transitions")
        for delta in self.delta:
            file.write("\n")
            file.write(f"{delta[0]}:{delta[1]}>{delta[2]}")
        file.close()


"""Operações sobre AFs"""


def cartesian_product(af1, af2, fully_explicit=True):
    """
    Calcula o produto cartesiano de dois autômatos finitos.
    Método auxiliar para os algoritmos de construção da união e interseção
    de AFDs por produto cartesiano (Sipser, 1.25).
    Presume-se que os AFs de entrada (af1 e af2) sejam determinísticos.
    """

    # Atualiza nomes de estados, para garantir que não haverão estados com nomes repetidos
    if len(set(af1.K).intersection(set(af2.K))) > 0:
        print('AFDs têm estados com nomes iguais. Renomeando estados.')
        common_names = True
        af1_K = [state + '_1' for state in af1.K]
        af2_K = [state + '_2' for state in af2.K]
        af1_F = [state + '_1' for state in af1.F]
        af2_F = [state + '_2' for state in af2.F]
        s = (af1.s + '_1', af2.s + '_2')
    else:
        common_names = False
        af1_K = af1.K
        af2_K = af2.K
        af1_F = af1.F
        af2_F = af2.F
        s = (af1.s, af2.s)

    # Se alguma transição para o morto não for explícita, temos que explicitá-la.
    if not fully_explicit:
        af1_K.append('dead_1')
        af2_K.append('dead_2')

    # Cria conjunto de valores de entrada
    sigma = list(set(i for i in af1.sigma + af2.sigma))
    # Cria conjunto de estados possíveis de serem usados
    union_k = list(product(af1_K, af2_K))

    # Define transições
    delta = []
    for q1, q2 in union_k:
        for symbol in sigma:
            try:
                if common_names:
                    t1 = af1.getTransition(q1[:-2], symbol)
                    t2 = af2.getTransition(q2[:-2], symbol)
                else:
                    t1 = af1.getTransition(q1, symbol)
                    t2 = af2.getTransition(q2, symbol)
                # se len > 1, o autômato não é determinístico; se
                assert (len(t1) <= 1 and len(t2) <= 1)
            except AssertionError:
                print("Ao menos um FA de entrada não era determinístico.")
                print("Use algoritmo de determinização antes de continuar :)")
            # direcionamos para o morto as transições que não forem explícitas
            if not t1:
                t1 = ['dead_1']
            if not t2:
                t2 = ['dead_2']
            transition = (t1[0] + '_1', t2[0] +
                          '_2') if common_names else (t1[0], t2[0])
            delta.append(((q1, q2), symbol, transition))
    af_prod = AF(union_k, sigma, delta, s)
    return af1_F, af2_F, af1_K, af2_K, af_prod


def format_product(af: AF):
    """Formatador para tuplas usadas no produto cartesiano"""

    def merge_tuples(x): return '{' + f'{x[0]},{x[1]}' + '}'

    af.K = list(map(merge_tuples, af.K))
    af.F = list(map(merge_tuples, af.F))
    af.s = merge_tuples(af.s)
    delta = list(zip(*af.delta))
    delta[0] = list(map(merge_tuples, delta[0]))
    delta[2] = list(map(merge_tuples, delta[2]))
    af.delta = list(zip(*delta))


def union(af1: AF, af2: AF) -> AF:
    """Utiliza o produto cartesiano para gerar a união de dois AFDs"""
    af1_F, af2_F, af1_K, af2_K, af_prod = cartesian_product(af1, af2)
    final_union = list(set(product(af1_F, af2_K)) | set(product(af1_K, af2_F)))
    af_prod.F = final_union
    # Remover estados inalcançáveis -> usar o `minimize` aqui
    format_product(af_prod)
    return af_prod


def intersection(af1: AF, af2: AF) -> AF:
    """Utiliza o produto cartesiano para gerar a interseção de dois AFDs"""
    af1_F, af2_F, af1_K, af2_K, af_prod = cartesian_product(af1, af2)
    final_intersection = list(product(af1_F, af2_F))
    af_prod.F = final_intersection
    # Remover estados inalcançáveis -> usar `minimize` aqui
    format_product(af_prod)
    return af_prod
