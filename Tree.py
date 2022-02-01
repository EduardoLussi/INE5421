class Node:
    def __init__(self, name="", children=[]):
        self.name = name
        self.children = children

        self._nullable = None
        self._firstpos = None
        self._lastpos = None
        self.followpos = set()

    def plot(self):
        print(self.toString())

    def toString(self):
        if len(self.children) == 0:
            return f"{self.name}"
        elif len(self.children) == 1:
            return f"{self.name} > ({self.children[0].toString()})"
        else:
            return f"{self.name} > ({self.children[0].toString()}, {self.children[1].toString()})"

    @staticmethod
    def getTree(regex):
        """
        Constrói árvore sintática da expressão regular.
        O algoritmo procura por cada operador na ordem | > . > * para separar
        os filhos da esquerda e da direita e construir a árvore recursivamente
        a partir deles.
        """

        def searchOperator(operator):
            """
            Procura por operador e retorna parte esquerda e direita.
            """
            left, right = "", ""
            parentesis = 0
            for i in range(len(regex) - 1, -1, -1):  # Varre ER da direita para esquerda
                # Verifica se encontrou o operador fora de qualquer parentesis
                if regex[i] == operator and parentesis == 0:
                    left = regex[:i]
                    return left, right[::-1]

                # Contagem de parentesis
                if regex[i] == ")":
                    parentesis += 1
                elif regex[i] == "(":
                    parentesis -= 1

                right += regex[i]

            return left, right[::-1]

        left, right = searchOperator("|")  # Procura por operador |
        if left != "":
            # Retorna nó | com filhos da esquerda e direita calculados recursivamente
            return Node("|", [Node.getTree(left), Node.getTree(right)])

        left, right = searchOperator(".")  # Procura por operador .
        if left != "":
            # Retorna nó . com filhos da esquerda e direita calculados recursivamente
            return Node(".", [Node.getTree(left), Node.getTree(right)])

        left, right = searchOperator("*")  # Procura por operador *
        if left != "":
            # Retorna nó * com filho calculado recursivamente
            return Node("*", [Node.getTree(left)])

        # Verifica se a expressão é algo entre parentesis
        if regex[0] == "(" and regex[-1] == ")":
            # Calcula recursivamente a árvore da expressão entre parentesis
            return Node.getTree(regex[1:-1])

        return Node(regex)  # Nó não possui operadores, então é final

    def isNullable(self):
        """
        Retorna se nó é nullable.
        Realiza cálculo somente se necessário.
        """
        if self._nullable is not None:  # Verifica de nullable já foi calculado
            return self._nullable

        # Calcula nullable
        if self.name == "&" or self.name == "*":
            self._nullable = True
        elif self.name == "|":
            self._nullable = (
                self.children[0].isNullable() or self.children[1].isNullable()
            )
        elif self.name == ".":
            self._nullable = (
                self.children[0].isNullable() and self.children[1].isNullable()
            )
        else:
            self._nullable = False

        return self._nullable

    def getFirstpos(self):
        """
        Retorna firstpos do nó.
        Realiza cálculo somente se necessário.
        """
        if self._firstpos is not None:  # Verifica de firstpos já foi calculado
            return self._firstpos

        # Calcula firstpos
        if self.name == "&":
            self._firstpos = set()
        elif self.name == "|":
            self._firstpos = (
                self.children[0].getFirstpos().union(self.children[1].getFirstpos())
            )
        elif self.name == ".":
            if self.children[0].isNullable():
                self._firstpos = (
                    self.children[0].getFirstpos().union(self.children[1].getFirstpos())
                )
            else:
                self._firstpos = self.children[0].getFirstpos()
        elif self.name == "*":
            self._firstpos = self.children[0].getFirstpos()
        else:
            self._firstpos = set([self])

        return self._firstpos

    def getLastpos(self):
        """
        Retorna lastpos do nó.
        Realiza cálculo somente se necessário.
        """
        if self._lastpos is not None:  # Verifica de lastpos já foi calculado
            return self._lastpos

        # Calcula lastpos
        if self.name == "&":
            self._lastpos = set()
        elif self.name == "|":
            self._lastpos = (
                self.children[0].getLastpos().union(self.children[1].getLastpos())
            )
        elif self.name == ".":
            if self.children[1].isNullable():
                self._lastpos = (
                    self.children[0].getLastpos().union(self.children[1].getLastpos())
                )
            else:
                self._lastpos = self.children[1].getLastpos()
        elif self.name == "*":
            self._lastpos = self.children[0].getLastpos()
        else:
            self._lastpos = set([self])

        return self._lastpos

    def calculateFollowpos(self):
        """
        Calcula followpos da árvore.
        """
        for (
            children
        ) in self.children:  # Faz busca em profundidade para calcular followpos
            children.calculateFollowpos()

        if self.name == ".":  # Se n é um nó-concatenação
            for i in self.children[
                0
            ].getLastpos():  # Para cada posição i em lastpos(c1)
                # Todas as posições em firstpos(c2) estão em followpos(i)
                i.followpos = i.followpos.union(self.children[1].getFirstpos())
        elif self.name == "*":  # Se n é um nó-asterisco
            for i in self.getLastpos():  # e i é uma posição em lastpos(n)
                # Todas as posições em firstpos(n) estão em followpos(i)
                i.followpos = i.followpos.union(self.getFirstpos())
