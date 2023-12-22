
grammar = {
    'V': {'0', '1', 'S', 'A', 'B'},
    'T': {'0', '1'},
    'S': 'S',
    'P': {
        'S': ['101A'],
        'A': ['1A', '0']
    }
}

def generate_language(start_symbol, production_rules, depth):
    if depth == 0:
        return [start_symbol]

    generated_strings = []
    for rule in production_rules.get(start_symbol, [start_symbol]):
        generated_strings.extend(generate_language(rule, production_rules, depth - 1))
    return generated_strings

generated_language = generate_language(grammar['S'], grammar['P'], 3)

print(Fore.GREEN + "1. Мова, породжена граматикою G:")
for string in generated_language:
    print(string)

def get_grammar_type(grammar):
    if all(any(len(production) >= len(lhs) and lhs in production for production in productions) for lhs, productions in grammar['P'].items()):
        return f"Контекстно-залежна граматика"

    if all(all((symbol in grammar['V'] or symbol == 'ε') for symbol in production) for productions in grammar['P'].values() for production in productions):
        return f"Контекстно-вільна граматика"

    if all(all((len(symbol) == 1 and (symbol in grammar['V'] or symbol in grammar['T'])) or symbol == 'ε' for symbol in production) for productions in grammar['P'].values() for production in productions):
        return f"Регулярна граматика"

    return f"Не визначено"


print("2. Тип граматики:")
print(f"{get_grammar_type(grammar)}")


def build_nfa1(grammar):
    nfa_diagram = {}
    nfa_table = {state: {symbol: set() for symbol in grammar['T'].union({'ε'})} for state in grammar['V']}

    for state, productions in grammar['P'].items():
        for production in productions:
            symbol = production[0]
            if len(production) > 1:
                next_state = production[1:]
                if state not in nfa_diagram:
                    nfa_diagram[state] = {}
                if symbol not in nfa_diagram[state]:
                    nfa_diagram[state][symbol] = set()
                nfa_diagram[state][symbol].add(next_state)

                nfa_table[state][symbol].add(next_state)
            else:
                nfa_table[state][symbol].add('ε')

    return nfa_diagram, nfa_table

def print_nfa_diagram(nfa_diagram):
    print("Діаграма NFA:")
    for state, transitions in nfa_diagram.items():
        print(f"{state}: {transitions}")

def print_nfa_table(nfa_table):
    print("\nТаблиця NFA:")
    header = "+---+" + "+".join(["-----" for _ in nfa_table['S']]) + "+"
    print(header)
    print("|   | " + " | ".join(nfa_table['S'].keys()) + " |")
    print(header)

    for state, transitions in nfa_table.items():
        print(f"| {state} | " + " | ".join([" ".join(sorted(dest)) if dest else '-' for dest in transitions.values()]) + " |")
        print(header)  


nfa_diagram, nfa_table = build_nfa1(grammar)
print_nfa_diagram(nfa_diagram)
print_nfa_table(nfa_table)
