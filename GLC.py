import copy

from AF import AF


class GLC:
    """
        Uma Gramática Livre de Contexto é uma quadrupla (N, T, P, S) onde:
            - N é o conjunto de símbolos não terminais
            - T é o conjunto de símbolos terminais (o alfabeto)
            - S é o símbolo inicial
            - P é o conjunto de regras de produção, tal que:
                P = { A ::= delta, onde A pertence a N
                    e delta é uma lista de listas de terminais e não-terminais }
                    (cada sublista de delta é uma lista ordenada que representa
                    uma produção)
    """

    def __init__(self, N=None, T=None, S=None, P=None, name=''):
        self.N = N if N else list()
        self.T = T if T else list()
        self.S = S if S else list()
        self.P = P if P else list()

        self.name = name

        self._first = dict()
        self._follow = dict()

    def __str__(self):
        glc_str = ''
        for origin, productions in self.P.items():
            glc_str += f"{origin} ::= " + \
                       ' | '.join([' '.join(prod) for prod in productions]) + \
                       '\n'
        return glc_str

    def read_grammar(self, filename):
        """Importa gramática de arquivo"""
        with open(filename, 'r') as f:
            # nonterminals
            line = f.readline()
            non_terminals = []
            while True:
                line = f.readline().rstrip('\n')
                if line[0] == '#':
                    break
                non_terminals.append(line)
            # terminals
            terminals = []
            while True:
                line = f.readline().rstrip('\n')
                if line[0] == '#':
                    break
                terminals.append(line)
            if set(non_terminals).intersection(set(terminals)):
                raise ValueError('Algum símbolo aparece nas listas de terminais e não terminais')
            # start
            start = f.readline().rstrip('\n')
            # productions
            productions = {}
            line = f.readline()
            while True:
                line = f.readline().rstrip('\n')
                if line == '':
                    break
                line = line.split(" ::= ")
                origin = line[0]
                prods = [prod.split(' ') for prod in line[1].split("|") if prod]
                prods = [list(filter(lambda val: val != '', prod)) for prod in prods]
                productions[origin] = prods
            self.T = terminals
            self.S = start
            self.N = non_terminals
            self.P = productions

    def export(self, file_name):
        """Exporta gramática para arquivo"""
        with open(file_name, "w") as file:
            file.write("#nonterminals\n")
            for s in self.N:
                file.write(f"{s}\n")
            file.write("#terminals\n")
            for s in self.T:
                file.write(f"{s}\n")
            file.write("#start\n")
            file.write(f"{self.S}\n")
            file.write("#productions\n")
            file.write(str(self))

    def setFirst(self):
        """Calcula o conjunto first da gramática"""
        self._first.clear()
        debug = True

        for terminal in self.T:  # FIRST de um terminal é o próprio terminal
            self._first[terminal] = set([terminal])

        for nonTerminal in self.N:  # Definição dos first de cada não-terminal
            self._first[nonTerminal] = set()

        # 1. Se X ::= aY, a pertence à FIRST(X)
        for nonTerminal in self.N:
            for nonTerminalProduction in self.P[nonTerminal]:
                if nonTerminalProduction[0] in self.T:
                    if debug:
                        print(f"{nonTerminalProduction[0]} pertence à FIRST({nonTerminal})={self._first[nonTerminal]}")
                    self._first[nonTerminal].add(nonTerminalProduction[0])

        # 2. Se X ::= Y1 Y2...Yk, então FIRST(Y1) pertence à FIRST(X)
        finished = False
        while not finished:
            finished = True
            for nonTerminal in self.N:
                for nonTerminalProduction in self.P[nonTerminal]:
                    for symbol in nonTerminalProduction:
                        if symbol in self.N:
                            firstSymbol = self._first[symbol].copy()
                            if '&' in firstSymbol:
                                firstSymbol.remove('&')
                            if not firstSymbol.issubset(self._first[nonTerminal]):
                                if debug:
                                    print(
                                        f"FIRST({symbol})={self._first[symbol]} está contido em FIRST({nonTerminal})={self._first[nonTerminal]}")
                                self._first[nonTerminal] = self._first[nonTerminal].union(firstSymbol)
                                finished = False

                            if "&" not in self._first[symbol]:
                                break
                        else:
                            self._first[nonTerminal].add(symbol)
                            break
        if debug:
            print(self._first)

        return self._first

    def setFollow(self):
        """Calcula o conjunto follow dos não-terminais da gramática"""
        self._follow.clear()
        self.setFirst()
        debug = True

        if debug:
            print(f"FIRST={self._first}")

        for nonTerminal in self.N:  # Definição dos follows de cada não-terminal
            self._follow[nonTerminal] = set()
            if nonTerminal == self.S:
                self._follow[nonTerminal].add("$")

        finished = False
        while not finished:  # Enquanto houver alteração nos FOLLOWS
            finished = True
            # Para cada não-terminal nonTerminal
            for nonTerminal in self.N:
                # Para cada produção nonTerminalProduction de nonTerminal
                for nonTerminalProduction in self.P[nonTerminal]:
                    # 1. Se A ::= alfa B beta e beta != &, então adicione FIRST(beta) em FOLLOW(B)
                    # Para cada símbolo symbol da produção nonTerminalProduction
                    for i, symbol in enumerate(nonTerminalProduction[:-1]):
                        if symbol in self.N:  # Somente não-terminais possuem FOLLOW
                            for j in range(i + 1, len(nonTerminalProduction)):  # Verifica símbolos seguintes
                                print(self._first[nonTerminalProduction[j]])
                                firstNonTerminalProductionJ = self._first[nonTerminalProduction[j]]
                                if '&' in firstNonTerminalProductionJ:
                                    firstNonTerminalProductionJ.remove('&')
                                if not firstNonTerminalProductionJ.issubset(self._follow[symbol]):
                                    if debug:
                                        print(
                                            f"FIRST({nonTerminalProduction[j]})={self._first[nonTerminalProduction[j]]}"
                                            + f"está contido em FOLLOW({symbol})={self._follow[symbol]}")
                                    self._follow[symbol] = self._follow[symbol].union(firstNonTerminalProductionJ)
                                    finished = False
                                # Se & pertence ao FIRST do símbolo atual nonTerminalProduction[j] continua, senão, para
                                if "&" not in self._first[nonTerminalProduction[j]]:
                                    break
                    # 2. Se A ::= alfa B (ou A ::= alfa B beta, onde & pertence à FIRST(beta)),
                    # então adicione FOLLOW(A) em FOLLOW(B)
                    for i, symbol in enumerate(nonTerminalProduction[::-1]):  # Varre produção ao contrário
                        if symbol not in self.N:  # Se o símbolo for terminal, para
                            break

                        if not self._follow[nonTerminal].issubset(self._follow[symbol]):
                            if debug:
                                print(
                                    f"FOLLOW({nonTerminal})={self._follow[nonTerminal]}"
                                    + f"está contido em FOLLOW({symbol})={self._follow[symbol]}")
                            self._follow[symbol] = self._follow[symbol].union(self._follow[nonTerminal])
                            finished = False

                        # Se & pertence ao FIRST do símbolo atual nonTerminalProduction[j], continua, senão, para
                        if "&" not in self._first[nonTerminalProduction[i]]:
                            break

        if debug:
            print(f"FOLLOW={self._follow}")

        return self._follow

    def slrRecognizeSentence(self, sentence):
        """Reconhece sentença via implementação de um SLR(1)"""

        def setClosure(Item):
            """Retorna o closure (fechamento) de um conjunto de itens"""
            debug = False
            if debug:
                print("Calculating Closure...")
            i = 0
            while i < len(Item):  # Para cada não-terminal nonTerminal
                nonTerminal, productions = list(Item.items())[i]
                for production in productions:  # Para cada produção production de nonTerminal
                    if debug:
                        print(f"Looking at {nonTerminal} -> {production}")
                    pointIndex = production.index(".")  # Obtém índice de .

                    # Se o símbolo depois do ponto for um não-terminal
                    if pointIndex < len(production) - 1:
                        symbolAfterPoint = production[pointIndex + 1]
                        if symbolAfterPoint in self.N:

                            # Adiciona todas as produções desse símbolo no Item com . no início
                            if symbolAfterPoint not in Item:
                                Item[symbolAfterPoint] = []
                            for symbolAfterPointProduction in self.P[symbolAfterPoint]:
                                newProduction = symbolAfterPointProduction.copy()
                                newProduction.insert(0, ".")
                                if newProduction not in Item[symbolAfterPoint]:
                                    Item[symbolAfterPoint].append(newProduction)
                                    if debug:
                                        print(f"New Production: {symbolAfterPoint} -> {newProduction}")
                i += 1
            return Item

        def getGoto(Item):
            """Retorna autômato finito que representa função goto"""
            debug = False

            if debug:
                print("Calculating goto...")

            transitions = dict()
            for nonTerminal, productions in Item.items():  # Para cada não-terminal nonTerminal
                for production in productions:  # Para cada produção production de nonTerminal
                    if debug:
                        print(f"Looking at {nonTerminal} -> {production}")
                    pointIndex = production.index(".")  # Obtém índice de .
                    if pointIndex < len(production) - 1:  # Se . não é o último símbolo da produção
                        # Cria nova produção passando o ponto para frente, por exemplo: S' ::= .S -> S' ::= S.
                        newProduction = production.copy()
                        newProduction.remove('.')
                        newProduction.insert(pointIndex + 1, '.')

                        # Adiciona transição por símbolo depois do ponto
                        if newProduction[pointIndex] not in transitions.keys():
                            transitions[newProduction[pointIndex]] = dict()

                        if nonTerminal in transitions[newProduction[pointIndex]]:
                            if newProduction not in transitions[newProduction[pointIndex]][nonTerminal]:
                                transitions[newProduction[pointIndex]][nonTerminal].append(newProduction)
                        else:
                            transitions[newProduction[pointIndex]][nonTerminal] = [newProduction]
                        if debug:
                            print(f"New production for transition by {newProduction[pointIndex]}: {newProduction}")
            return transitions

        # 1. Criar autômato
        debug = False

        sigma = self.N.copy()
        sigma.extend(self.T.copy())
        sigma.append('$')
        af = AF(sigma=sigma, K=[], delta=[], s=None, F=[], name='')

        I = [{f"{self.S}'": [['.', self.S]]}]  # Cria conjunto de itens I com I0 contendo somente S' ::= .S
        af.s = "I0"  # Estado inicial é I0
        af.K.append("acc")
        af.F = ['acc']
        setClosure(I[0])
        for i, Ii in enumerate(I):
            af.K.append(f"I{i}")  # Insere estado Ii
            if debug:
                print(f"I{i}: {Ii}")
            goto = getGoto(Ii)  # Calcula Goto(Ii)
            if f"{self.S}'" in Ii and [self.S, "."] in Ii[f"{self.S}'"]:  # Estado final
                af.delta.append((f"I{i}", "$", "acc"))
            if debug:
                print(f"GOTO(I{i}): {goto}")
            # Cria novos itens I
            for symbol, newI in goto.items():  # Para cada novo I newI encontrado a partir de Ii
                setClosure(newI)  # Calcula Closure(newI)
                for j, Ij in enumerate(I):  # Verifica se newI já não existe em I
                    if len(Ij) == len(newI):  # Se o tamanho do Ij é igual ao novo I newI
                        for IjSymbol, IjSymbolProductions in Ij.items():  # Para cada símbolo IjSymbol em Ij
                            differentProductions = False
                            if IjSymbol in newI.keys():  # Se o símbolo está em newI
                                # Se a quantidade de produções de IjSymbol for igual em Ij e newI
                                if len(IjSymbolProductions) == len(newI[IjSymbol]):
                                    # Verifica se produções de IjSymbol são iguais as de newI por IjSymbol
                                    for IjSymbolProcutionsElement in IjSymbolProductions:
                                        # Encontrada produção diferente
                                        if not IjSymbolProcutionsElement in newI[IjSymbol]:
                                            differentProductions = True
                                            break
                                else:
                                    break
                            else:  # Se o símbolo não está em newI, newI != Ij
                                break
                            if differentProductions:
                                break
                        else:  # Ij é equivalente a newI
                            af.delta.append((f"I{i}", symbol, f"I{j}"))
                            if debug:
                                print(f"Found equivalent I{j}: {I[j]}")
                            break
                else:
                    af.delta.append((f"I{i}", symbol, f"I{len(I)}"))
                    I.append(newI)
        if debug:
            print("\n Autômato LR(0):")
            af.plot()
        # 2. Criar tabela SLR
        debug = False
        extendedGrammar = GLC(self.N.copy(), self.T.copy(), f"{self.S}'", self.P.copy())
        extendedGrammar.N.append(extendedGrammar.S)
        extendedGrammar.P[extendedGrammar.S] = [[self.S]]
        extendedGrammar.setFollow()

        SLRTable = []
        for i, Ii in enumerate(I):
            SLRTable.append(dict())
            # Shifts
            for terminal in self.T:
                terminalTransition = af.getTransition(f"I{i}", terminal)
                if len(terminalTransition):
                    SLRTable[i][terminal] = f"s{terminalTransition[0][1:]}"
            # Desvios
            for nonTerminal in self.N:
                nonTerminalTransition = af.getTransition(f"I{i}", nonTerminal)
                if len(nonTerminalTransition):
                    SLRTable[i][nonTerminal] = f"{nonTerminalTransition[0][1:]}"
            # Reduces
            for item, productions in Ii.items():
                if item == f"{self.S}'":  # Aceitação acc
                    if productions == [[self.S, "."]]:
                        SLRTable[i]["$"] = "acc"
                else:
                    for production in productions:
                        if production[-1] == '.':
                            productionWithoutPoint = production.copy()
                            productionWithoutPoint.remove('.')
                            for follow in extendedGrammar._follow[item]:
                                productionIndex = self.P[item].index(productionWithoutPoint)
                                SLRTable[i][follow] = f"r {item} {productionIndex}"
        if debug:
            print("Tabela SLR:")
            for i, line in enumerate(SLRTable):
                print(f"{i}: {line}")

        # 3. Reconhecimento da sentença
        debug = False

        sentence = sentence.split()
        sentence.append("$")

        def recognize(sentence):
            if debug:
                print(sentence)
            stack = [0]
            i = 0
            while True:
                symbol = sentence[i]
                action = SLRTable[stack[-1]][symbol]
                if debug:
                    print(sentence[i:], stack, action)
                if action == "acc":
                    return True
                if action[0] == "s":
                    stack.append(int(action[1:]))
                    i += 1
                elif action[0] == "r":  # Também verifica se redução corresponde
                    _, reduced, productionIndex = action.split()
                    production = self.P[reduced][int(productionIndex)]
                    for productionSymbol in production[::-1]:
                        # Procura produção que termina com .
                        foundSymbol = False
                        for _, stackISymbolProductions in I[stack[-1]].items():
                            for stackISymbolProduction in stackISymbolProductions:
                                if stackISymbolProduction[-1] == ".":
                                    # Valor antes do ponto precisa ser igual ao indicado por r
                                    if stackISymbolProduction[-2] != productionSymbol:
                                        if debug:
                                            print(f"Sentença não reconhecida. Falha em r {reduced} {productionIndex}")
                                        return False
                                    foundSymbol = True
                                    break
                            if foundSymbol:
                                break
                        stack.pop()
                    stack.append(int(SLRTable[stack[-1]][reduced]))

        try:
            return recognize(sentence)
        except Exception as err:
            if debug:
                print(f"Sentença não reconhecida. {err}")
            return False

    def removeUnproductiveSymbols(self):
        """Retorna uma gramática equivalente, sem símbolos improdutivos"""
        markedTSymbols = []
        productions = dict()

        def dict_deep_length(dic):
            l = 0
            for e in dic:
                if isinstance(e, list):
                    l += len(e)
                else:
                    l += 1
            return l

        productionCount = 0

        while True:
            for nonTerminal, production in [(nonTerm, prod)
                                            for nonTerm in self.N
                                            for prod in self.P[nonTerminal]]:

                if productions[nonTerminal] and production in productions[nonTerminal]:
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
                    nonMarked = list(filter(symbol.__ne__, nonMarked))

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

    def llRecognizeSentence(self, sentence):
        """Reconhece sentença via implementação de um LL(1)"""

        table = self.generateLLparseTable()
        stack = ["$", self.S]
        
        for symbol in sentence:
            while symbol != stack[-1]:
                if symbol not in table[stack[-1]]:
                    return False
                prod = table[stack[-1]][symbol]
                stack.pop()
                if prod == ["&"]:
                    continue
                else:
                    for p in reversed(prod):
                        stack.append(p)
            stack.pop()
        print (stack)
        return stack == ["$"]


    def generateLLparseTable(self):
        self.setFirst()
        self.setFollow()
        table = {}
            
        # itero sobre as produções de cada terminal da gramática
        for non_terminal, productions in self.P.items():
            table[non_terminal] = {}
            # itero sobre as produções do não terminal
            for alpha in productions:
                firsts = self._first[alpha[0]]
                print(f"{alpha[0]} -> {firsts}")
                for symbol in firsts:
                    if symbol in self.T:
                        if symbol == "&":
                            table[non_terminal]["$"] = alpha
                        else:
                            table[non_terminal][symbol] = alpha
                if '&' in firsts:
                    for symbol in self._follow[non_terminal]:
                        if symbol in self.T:
                            if symbol == "&":
                                table[non_terminal]["$"] = alpha
                            else:
                                table[non_terminal][symbol] = alpha
        return table

    def eliminateLeftRecursion(self):
        """Retorna uma gramática equivalente, eliminando recursão a esquerda"""

        def eliminateDirectLeftRecursion(nonTerminal, P=self.P):
            """ Utilitário para eliminação de recursão direta"""
            alphas = list()
            betas = list()
            ntDash = f"{nonTerminal}\'"
            for production in P[nonTerminal]:
                if production[0] is nonTerminal:
                    alphas.append(production[1:])
                elif production[0] == '&':
                    pass
                else:
                    betas.append(production)
            ntProductions = [beta.append(ntDash) for beta in betas]
            ntDashProductions = [alpha.append(ntDash) for alpha in alphas].append('&')

            return ntProductions, ntDashProductions, ntDash

        def eliminateEpsilonProductions(N, P):
            """Utilitário para eliminação de epsilon produções"""
            for nonTerminal in N:
                for production in P[nonTerminal]:
                    productionBag = list()
                    hasEpsilonProduction = False
                    if production[0] == '&':
                        hasEpsilonProduction = True
                    else:
                        productionBag.push(production)

        newN = list()
        newP = dict()

        # elimina recursoes diretas
        for nonTerminal in self.N:
            ntP, ntDashP, ntDash = eliminateDirectLeftRecursion(nonTerminal)
            newN.push(nonTerminal)
            newN.push(ntDash)
            newP[nonTerminal] = ntP
            newP[ntDash] = ntDashP

        # elimina &-producoes
        eliminateEpsilonProductions(newN, newP)

        # elimina recursoes indiretas
        newNewN = list()
        nonTerminalEnumeration = enumerate(newN)
        for (i, nonTerminali) in nonTerminalEnumeration:
            for nonTerminalj in [nonTerminalj for j, nonTermninalj in nonTerminalEnumeration if j < i]:
                for production in newP[nonTerminali]:
                    if production[0] is nonTerminalj:
                        newP[nonTerminali].remove(production)
                        for productionBeta in newP[nonTerminalj]:
                            newP[nonTerminali].append(productionBeta.append(production[1:]))
            (ntP, ntDashP, ntDash) = eliminateDirectLeftRecursion(nonTerminali, newP)
            newNewN.push(nonTerminali)
            newNewN.push(ntDash)
            newP[nonTerminal] = ntP
            newP[ntDash] = ntDashP
        newN = newNewN

        # elimina &-producoes
        eliminateEpsilonProductions(newN, newP)

        return GLC(newN, self.T, self.S, newP, self.name)

    """ ---------------- FATORAÇÃO ----------------- """

    def left_factoring(self, *, iters=1):
        """Fatoração de GLC"""
        while iters > 0:
            self.__remove_indirect_non_determinism()
            self.__remove_direct_non_determinism()
            iters -= 1

    def __remove_direct_non_determinism(self):
        """
        Encontra e remove determinismos diretos na gramática
        Para cada não-terminal, busca produções que comecem com o(s) mesmo(s) símbolo(s).
        Para cada produção salva, elimina não determinismo.
        """
        direct = {}
        for non_terminal in self.N:
            direct[non_terminal] = []
            productions = self.P[non_terminal]
            for i, prod1 in enumerate(productions):
                for _, prod2 in enumerate(productions[i + 1:]):
                    # avaliamos se os primeiros símbolos dos dois fatores são iguais.
                    prefix = []
                    for p1, p2 in zip(prod1, prod2):
                        if p1 != p2:
                            break
                        prefix.append(p1)
                    if prefix and prefix not in direct[non_terminal]:
                        direct[non_terminal].append(prefix)

        def test_prefixing(substring1, substring2):
            for sub1, sub2 in zip(substring1, substring2):
                if sub1 != sub2:
                    return False
            return True

        for non_terminal, prefixes in direct.items():
            if not prefixes:
                continue
            productions = list()
            for i, prefix in enumerate(prefixes):
                new_symbol = f"{non_terminal}'{i}"
                self.N.append(new_symbol)
                if prefix + [new_symbol] not in productions:
                    productions.append(prefix + [new_symbol])
                prod_list = list()
                for production in self.P[non_terminal]:
                    if not test_prefixing(prefix, production):
                        continue
                    prod = production[len(prefix):]
                    if not prod:  # para produções "vazias", colocamos &
                        prod = ['&']
                    if prod not in prod_list:
                        prod_list.append(prod)
                self.P[new_symbol] = prod_list

            for production in self.P[non_terminal]:
                prefixed = False
                for prefix in prefixes:
                    if not prefixed and test_prefixing(prefix, production):
                        prefixed = True
                if not prefixed and production not in productions:
                    productions.append(production)
            self.P[non_terminal] = productions

    def __remove_indirect_non_determinism(self):
        """
        Remove não determinismos indiretos, por substituição.

        Normalmente, se faria a substituição somente dos não-terminais que fossem
        gerar o não determinismo.
        Neste caso, não fazemos esta busca, optando-se por este algoritmo mais simples,
        que realiza a substituição não recursiva de todos os terminais. Se houver algum
        determinismo direto, ele pode ser eliminado pelo algoritmo que remove os diretos.
        """
        non_terminals = self.N
        derived = copy.deepcopy(self)
        for origin, productions in self.P.items():
            for production in productions:
                changed = False
                for i, symbol in enumerate(production):
                    if symbol in non_terminals:
                        if symbol == origin:
                            continue
                        if production in productions:
                            derived.P[origin].remove(production)
                        for prod in self.P[symbol][:]:
                            replaced = production[:i] + prod + production[i + 1:]
                            if replaced not in productions:
                                derived.P[origin].append(replaced)
                                changed = True
                    if changed:
                        break
        self.P = derived.P
