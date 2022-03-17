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
        self.P = P if P else dict()

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
        debug = False

        for terminal in self.T:  # FIRST de um terminal é o próprio terminal
            self._first[terminal] = {terminal}

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
        debug = False

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

                nonMarked = copy.copy(production)
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

    def llRecognizeSentence(self, sentence, show_steps=False):
        """Reconhece sentença via implementação de um analisador LL(1)"""
        table = self.generateLLparseTable()
        if show_steps:
            from pandas import DataFrame
            print(f"\nMostrando passos para o reconhecimento da sentença {' '.join(sentence)} com a gramática:")
            print(self)
            print('Conjuntos FIRST')
            for symbol, firsts in self._first.items():
                print(f'FIRST({symbol}) = {firsts}')

            print('Conjuntos FOLLOW')
            for symbol, follow in self._follow.items():
                print(f'FOLLOW({symbol}) = {follow}')

            print('\nTabela de transição LL(1)')
            print(DataFrame(table).transpose().fillna('-'))
            print()

        stack = ["$", self.S]
        sentence += '$'  # adiciona fim da leitura
        i = 0
        symbol = sentence[i]
        while stack != ['$'] and i < len(sentence):
            if show_steps:
                print(f'Cabeçote: {symbol}; Pilha: {stack}')
            if stack[-1] in self.T:
                if i + 1 < len(sentence):
                    i += 1
                symbol = sentence[i]
                stack.pop()
                continue
            if symbol not in table[stack[-1]]:
                break
            prod = table[stack[-1]][symbol]
            stack.pop()
            if prod == ["&"]:
                continue
            elif prod:
                for p in reversed(prod):
                    stack.append(p)
        output = 'aceita' if stack == ["$"] else 'rejeita'
        if show_steps:
            print(f'Cabeçote: {symbol}; Pilha: {stack}')
            print(f'\n{output} sentença')
        return stack == ["$"]

    def generateLLparseTable(self):
        """Gera tabela de parse LL(1)"""
        self.setFirst()
        self.setFollow()
        table = {}
        # itero sobre as produções de cada terminal da gramática
        for non_terminal, productions in self.P.items():
            table[non_terminal] = {}
            # itero sobre as produções do não terminal
            for alpha in productions:
                firsts = self._first[alpha[0]]
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

        hasEpsilonProduction = False

        def eliminateEpsilonProductions(N, P):
            nonlocal hasEpsilonProduction
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

    def left_factoring(self, *, iters=10):
        """Fatoração de GLC"""
        #podemos comçear removendo determinismos diretos, para facilitar o trabalho
        self.__remove_direct_non_determinism()
        print(self)
        while iters > 0 and self.__remove_indirect_non_determinism():
            print(self)
            self.__remove_direct_non_determinism()
            print(self)
            iters -= 1

    def __remove_direct_non_determinism(self):
        productions = self.P
        new_productions = {}
        for non_terminal in productions:
            new_productions[non_terminal] = []
            prefixes = []
            for prod1 in productions[non_terminal]:
                if not prefixes:
                    prefixes.append(prod1)
                    continue
                found_pref = False
                prefix = []
                for i, prod2 in enumerate(prefixes):
                    for p1, p2 in zip(prod1, prod2):
                        if p1 != p2:
                            break
                        prefix.append(p1)
                    if prefix and prefix not in prefixes:
                        prefixes[i] = prefix
                        found_pref = True
                if not found_pref:
                    prefixes.append(prod1)
            for i, pref in enumerate(prefixes):
                prod_aux = []
                for prod in productions[non_terminal]:
                    # testamos se a produção começa com o prefixo salvo em pref
                    if len(pref) <= len(prod) and pref == prod[:len(pref)]:
                        prod_aux.append(prod)
                if len(prod_aux) > 1:
                    new_symbol = non_terminal + (i+1)*"'"
                    self.N.append(new_symbol)
                    new_prod = pref + [new_symbol]
                    if new_prod not in new_productions[non_terminal]:
                        new_productions[non_terminal].append(new_prod)
                    new_productions[new_symbol] = []
                    for p in prod_aux:
                        p = p[len(pref):]
                        p = p if len(p) > 0 else ['&']
                        new_productions[new_symbol].append(p)
                else:
                    new_productions[non_terminal].append(pref)
        self.P = new_productions

    def derive(self, prod):
        """Gera lista de cadeias derivadas da produção"""
        if not prod:
            return [[]]
        prod_ = prod[0]
        if prod_ in self.T:
            return [[prod_] + derivation for derivation in self.derive(prod[1:])]
        elif prod_ in self.P:
            out = []
            derivations = self.derive(prod[1:])
            for p in self.P[prod_]:
                if p == ['&']:
                    out += derivations
                else:
                    if derivations:
                        out += [p + deriv for deriv in derivations]
                    else:
                        out += p
            return out

    def __remove_indirect_non_determinism(self):
        """ Identifica e remove os indeterminismos indiretos utilizando os conjuntos FIRST"""

        def get_firsts_chain(chain):
            """Helper para atualizar e buscar o first do primeiro simbolo da cadeia"""
            self.setFirst()
            return list(self._first[chain[0]])

        changed = False
        # busca não-determinismos indiretos e os elimina
        for s in self.P:
            aux = []
            worrisome = set()
            for prod in self.P[s]:
                firsts = get_firsts_chain(prod)
                # faz a intersecção com o first de uma produção salva
                for a in aux:
                    if len(set(firsts).intersection(a[1])) > 0:
                        worrisome.add(tuple(prod))
                        worrisome.add(tuple(a[0]))
                        changed = True
                for i, symbol in enumerate(prod[:-1]):
                    if symbol in self.N and '&' in self._first[symbol]:
                        if len(self._first[symbol].intersection(get_firsts_chain(prod[i + 1:]))) > 0:
                            worrisome.add(prod)
                            changed = True
                aux.append((prod, firsts))
            for prod in worrisome:
                self.P[s].remove(list(prod))
            for prod in worrisome:
                derivations = self.derive(list(prod))
                for d in derivations:
                    if d not in self.P[s]:  # precisamos deste if por estarmos usando lists e não sets
                        self.P[s].append(d)
        # remove nõa-determinismos diretos pre-existentes e criados pela derivação
        return changed
