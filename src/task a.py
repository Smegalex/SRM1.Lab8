class Noda:
    left = None
    central = None
    right = None

    def __init__(self, central):
        self.central = central

    def __init__(self, left, central, right):
        self.left = left
        self.central = central
        self.right = right


def orsOpening(statement: str) -> list:
    statement = statement.split("=")
    statement = statement[1]
    statement = statement.split("|")
    return statement


print(orsOpening("<E>::=(<E>)|<E>+<E>|<E>*<E>|<V>|<C>"))
# <E>::=(<E>)|<E>+<E>|<E>*<E>|<V>|<C>
# <V>::=x|y
# <C>::=1|2
