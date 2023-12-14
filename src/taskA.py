from simplifyStatement import simplify_arythmetic_statement, operations


class Node:
    left = None
    central = None
    right = None
    face = None

    def __init__(self, left, central, right, face: str) -> None:
        self.left = left
        self.central = central
        self.right = right
        self.face = face

    def add_face(self, face: str) -> None:
        self.face = face

    def add_next(self, value) -> None:
        if self.left == None:
            self.left = value
        elif self.right == None:
            self.right = value

    def add_central(self, central) -> None:
        self.central = central

    def toString(self) -> str:
        elmnts = [self.left, self.central, self.right]
        for el_ind in range(len(elmnts)):
            if isinstance(elmnts[el_ind], Node):
                elmnts[el_ind] = elmnts[el_ind].toString()
        elmnts.append(self.face)
        return elmnts

    def print(self, padding="") -> None:
        left = ""
        central = ""
        right = ""

        nodesCount = {"left": False, "central": False, "right": False}
        if isinstance(self.left, Node):
            left = self.left.face
            nodesCount["left"] = True
        elif self.left:
            left = self.left

        if isinstance(self.central, Node):
            central = self.central.face
            nodesCount["central"] = True
        elif self.central:
            central = self.central

        if isinstance(self.right, Node):
            right = self.right.face
            nodesCount["right"] = True
        elif self.right:
            right = self.right

        print(padding, f"{left} {central} {right} \n")

        padding = padding + " ".ljust(5, " ")
        for key, el in nodesCount.items():
            if el:
                match key:
                    case "left":
                        print(padding, "left:")
                        self.left.print(padding)
                        continue
                    case "central":
                        print(padding, "central:")
                        self.central.print(padding)
                        continue
                    case "right":
                        print(padding, "right:")
                        self.right.print(padding)
                        continue


def orsOpening(statement: str) -> list:
    statement = statement.split("=")
    statement = statement[1]
    statement = statement.split("|")
    return statement


def nodeForming(simple_statement, E, V, C, face='E'):
    nodeFinal = Node(None, None, None, face)
    if face == 'V' or face == 'C':
        nodeFinal.add_central(simple_statement)
        return nodeFinal

    for el in simple_statement:
        if isinstance(el, list):
            nodeFinal.add_next(Node('(', nodeForming(el, E, V, C), ')', 'E'))
            continue
        if el in operations:
            nodeFinal.add_central(el)
            continue
        if el in V:
            nodeFinal.add_next(Node(None,
                                    nodeForming(el, E, V, C, 'V'), None, 'E'))
            continue
        if el in C:
            nodeFinal.add_next(Node(None,
                                    nodeForming(el, E, V, C, 'C'), None, 'E'))
            continue

    return nodeFinal


if __name__ == "__main__":
    E = orsOpening("<E>::=(<E>)|<E>+<E>|<E>*<E>|<V>|<C>")
    V = orsOpening("<V>::=x|y")
    C = orsOpening("<C>::=1|2")

    v1 = simplify_arythmetic_statement("x+(y+y)*y")
    v19 = simplify_arythmetic_statement("x+(y+y)*y")
    v25 = simplify_arythmetic_statement("2*y+2*(x+y+1)+x")

    finalNodeV1 = nodeForming(v1, E, V, C)
    finalNodeV19 = nodeForming(v19, E, V, C)
    finalNodeV25 = nodeForming(v25, E, V, C)
    finalNodeV1.print()
    print("-".ljust(100, "-"))
    finalNodeV19.print()
    print("-".ljust(100, "-"))
    print(v25)
    finalNodeV25.print()


# print(orsOpening("<E>::=(<E>)|<E>+<E>|<E>*<E>|<V>|<C>"))
# <E>::=(<E>)|<E>+<E>|<E>*<E>|<V>|<C>
# <V>::=x|y
# <C>::=1|2
