from re import S
from Tree import Node

class AF:
    '''
        Um autômato finito é uma quíntupla (K, sigma, delta, s, F) onde:
            - K é o conjunto de estados
            - sigma é o conjunto de símbolos de entrada
            - delta é a função de transição
            - s é o estado inicial
            - F é o conjunto de estados finais
    '''
    def __init__(self, K=[], sigma=[], delta=[], s=None, F=[], name=''):
        self.K = K
        self.sigma = sigma
        self.delta = delta
        self.s = s
        self.F = F

        self.name = name

    '''
        Retorna transição de "state" por "symbol"
    '''
    def getTransition(self, state, symbol):
        transition = []
        for t in self.delta:
            if t[0] == state and t[1] == symbol:
                transition.append(t[2])
        return transition

    '''
        Reconhecimento de sentença pelo AF
    '''
    def compute(self, input):
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
            if (state in self.F):
                return True
        return False

    '''
        Imprime autômato
    '''
    def plot(self):
        text = 'δ'
        for symbol in self.sigma:   # Primeira linha
            text += '|' + symbol
        text += '\n'

        for state in self.K:    # Cria demais linhas
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
            columnSizes.append(maxColumnSize+2)
        
        # Cria texto de impressão final com espaçamentos dinâmicos
        text = ''
        for line in textLines:
            for i, val in enumerate(line):
                textVal = val
                for j in range(columnSizes[i]-len(textVal)):
                    if j % 2 == 0:
                        textVal = textVal + ' '
                    else:
                        textVal = ' ' + textVal
                text += textVal + '|'
            text = text[:-1] + '\n'

        print(text)

    # Retorna transições por epsilon a partir de "state"
    def getEpsilonTransition(self, state):
        for k in state:
            epsilonTransition = self.getTransition(k, '&')
            for t in epsilonTransition:
                if t not in state:
                    state.append(t)
        return state

    '''
        A partir de "self", retorna um AFD equivalente
    '''
    def getAFD(self):
        K = [[self.s]]
        sigma = self.sigma.copy()

        if '&' in sigma:    # Remove epsilon
            sigma.remove('&')

        delta = []
        s = f"{'{'}"
        for state in self.getEpsilonTransition([self.s]):
            s += f"{state}, "
        s = s[:-2] + f"{'}'}"
        F = []

        # Obtém transições por epsilon para o estado inicial
        K[0] = self.getEpsilonTransition(K[0])

        for k in K: # A cada novo estado
            for symbol in self.sigma:   # Para cada símbolo do alfabeto
                if symbol == '&':
                    continue

                newState = []
                for state in k: # Para cada transição do símbolo
                    for t in self.getTransition(state, symbol): # Calcula o novo estado
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
                
                for k0 in K:    # Insere novo estado se ele ainda não existir
                    if set(newState) == set(k0):
                        break
                    if k0 == K[-1]:
                        K.append(newState)
        
        for k in K: # Define estados finais
            for f in self.F:
                if f in k:
                    F.append(k)
                    break

        for i, k in enumerate(K):   # Converte estados para string
            K[i] = str(k).replace("'", '').replace('[', '{').replace(']', '}')

        for i, f in enumerate(F):   # Converte estados finais para string
            F[i] = str(f).replace("'", '').replace('[', '{').replace(']', '}')

        return AF(K, sigma, delta, s, F)

    '''
        Lê os dados do AF a partir de um arquivo
    '''
    def readData(self, file_name):
        with open(file_name) as f:
            #states
            line = f.readline()
            states = []
            while True:
                line = f.readline().rstrip('\n')
                if line[0] == '#':
                    break
                states.append(line)
            self.K = states

            #initial
            self.s = f.readline().rstrip('\n')

            #accepting
            f.readline()
            accepStates = []
            while True:
                line = f.readline().rstrip('\n')
                if line[0] == '#':
                    break
                accepStates.append(line)
            self.F = accepStates

            #alphabet
            alphabet = []
            while True:
                line = f.readline().rstrip('\n')
                if line[0] == '#':
                    break
                alphabet.append(line)
            self.sigma = alphabet

            #transitions
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

    '''
        Cria autômato a partir de expressão regular
    '''
    def readRegex(self, regex):
        regex = f"({regex}).#"
        tree = Node.getTree(regex)   # Obtém árvore sintática
        tree.calculateFollowpos()   # Calcula followpos dos nós

        # Inicializa Dstates contendo somente o estado desmarcado firstpos(root)
        Dstates = [tree.getFirstpos()]
        S = [tree.getFirstpos()]
        Dtran = []
        allSymbols = set()
        unmarked = [tree.getFirstpos()]
        while len(unmarked) != 0:   # Enquanto houver um símbolo desmarcado S em Dstates
            S = unmarked.pop(0) # Marque S

            # Cria lista de símbolos
            symbols = set()
            for a in S:
                symbols = symbols.union(set([a.name]))
            
            allSymbols = allSymbols.union(symbols)

            for a in symbols:   # Para cada símbolo de entrada a
                U = set()   # Seja U,
                for p in S: # para cada p em S
                    if p.name == a: # que corresponde a a,
                        U = U.union(p.followpos)    # a união de followpos(p)
                if U not in Dstates: # Se U não está em Dstates
                    Dstates.append(U)   # Adicione U como estado desmarcado de Dstates
                    unmarked.append(U)
                if (S, a, U) not in Dtran:  # Insere transição
                    Dtran.append((S, a, U))

        for transition in Dtran:    # Remove estado morto de #
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

    '''
        Exporta o Autômato para um arquivo
    '''
    def exportAF(self, file_name):
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