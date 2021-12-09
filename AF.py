class AF:
    '''
        Um autômato finito é uma quíntupla (K, sigma, delta, s, F) onde:
            - K é o conjunto de estados
            - sigma é o conjunto de símbolos de entrada
            - delta é a função de transição
            - s é o estado inicial
            - F é o conjunto de estados finais
    '''
    def __init__(self, K=[], sigma=[], delta=[], s=None, F=[]):
        self.K = K
        self.sigma = sigma
        self.delta = delta
        self.s = s
        self.F = F

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
        s = f"{'{'}{self.s}{'}'}"
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
