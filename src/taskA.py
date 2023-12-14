from simplifyStatement import simplify_arythmetic_statement, operations


class Node:
    left = None
    central = None
    right = None
    face = None

    def add_face(self, face: str) -> None:
        self.face = face

    def add_next(self, value) -> None:
        if self.left == None:
            self.left = value
        elif self.right == None:
            self.right = value

    def add_central(self, central) -> None:
        self.central = central

    def __init__(self) -> None:
        pass

    def __init__(self, central) -> None:
        self.central = central

    def __init__(self, left, central, right) -> None:
        self.left = left
        self.central = central
        self.right = right


def orsOpening(statement: str) -> list:
    statement = statement.split("=")
    statement = statement[1]
    statement = statement.split("|")
    return statement


def nodeForming(simple_statement, E, V, C):
    nodeFinal = Node()
    for el in simple_statement:
        if isinstance(el, list):
            nodeFinal.add_next(Node("(", nodeForming(el, E, V, C), ")"))
            continue
        if el in operations:
            nodeFinal.add_central(el)
            continue
        if el in V:
            nodeFinal.add_next(el)
            continue
        if el in C:
            nodeFinal.add_next(el)
            continue


if __name__ == "__main__":
    E = orsOpening("<E>::=(<E>)|<E>+<E>|<E>*<E>|<V>|<C>")
    V = orsOpening("<V>::=x|y")
    C = orsOpening("<C>::=1|2")

    v1 = "x+(y+y)*y"
    v19 = "x+(y+y)*y"
    v25 = "2*y+2*(x+y+1)+x"
    print(simplify_arythmetic_statement(v1))


# print(orsOpening("<E>::=(<E>)|<E>+<E>|<E>*<E>|<V>|<C>"))
# <E>::=(<E>)|<E>+<E>|<E>*<E>|<V>|<C>
# <V>::=x|y
# <C>::=1|2
