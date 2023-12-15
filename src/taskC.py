possible_termVar_pairs = {'a': 'A', 'b': 'B', 'c': 'C'}
possible_vars = ['F', 'R']


def brackets_end_index(statement: list, brackets_ignor: int) -> int:
    for k in range(len(statement)):
        if statement[k] == '(':
            brackets_ignor += 1
        if statement[k] == ')':
            brackets_ignor += -1
            if brackets_ignor == 0:
                return k


def simplify_brackets(language: str) -> dict:
    variables = ['S']
    terminals = []
    final_dict = {'language': {}, 'arguments': {}}
    language = language[language.index(
        '{')+1:language.index('}')].replace(' ', '').split('|')
    language[1] = language[1].split('>=')

    if ',' in language[1][0]:
        language[1][0] = language[1][0].split(',')
    for arg in language[1][0]:
        final_dict['arguments'][arg] = language[1][1]

    language[0] = list(language[0])
    for char_ind in range(len(language[0])):
        if char_ind == len(language[0]):
            break
        if language[0][char_ind] == ' ':
            continue
        try:
            destination = final_dict['language'][language[0][char_ind]]
        except KeyError:
            final_dict['language'][language[0][char_ind]] = []
            destination = final_dict['language'][language[0][char_ind]]
        if char_ind == len(language[0])-1 and char_ind != ' ':
            terminals.append(language[0][char_ind])
            variables.append(terminals[-1])
            destination.append('1')
            break

        if language[0][char_ind+1] == '^':
            terminals.append(language[0][char_ind])
            variables.append(terminals[-1])
            power = language[0][language[0].index('(')+1:]

            pow_end_ind = brackets_end_index(power, 1)
            power = power[:pow_end_ind]

            first_bracket = language[0].index('(')
            language[0][first_bracket:first_bracket +
                        pow_end_ind+2] = ''.ljust(len(language[0][first_bracket:first_bracket+pow_end_ind+2]))

            destination.append(power)
            language[0][char_ind+1] = ' '
        elif language[0][char_ind] == '(':

            bracketed = language[0][char_ind+1:]
            end_ind = brackets_end_index(bracketed, 1)
            bracketed = bracketed[:end_ind]
            language[0][char_ind:char_ind +
                        end_ind+2] = ''.ljust(len(language[0][char_ind:char_ind+end_ind+2]))
            if language[0][char_ind+end_ind+2] == '^':
                del final_dict['language']['(']
                power = language[0][language[0].index('(')+1:]

                pow_end_ind = brackets_end_index(power, 1)
                power = power[:pow_end_ind]

                first_bracket = language[0].index('(')
                language[0][first_bracket:first_bracket +
                            pow_end_ind+2] = ''.ljust(len(language[0][first_bracket:first_bracket+pow_end_ind+2]))
                for terminal in bracketed:
                    try:
                        destination = final_dict['language'][terminal]
                    except KeyError:
                        final_dict['language'][terminal] = []
                        destination = final_dict['language'][terminal]

                    terminals.append(terminal)
                    variables.append(terminals[-1])

                    destination.append(power)
                language[0][char_ind+end_ind+2] = ' '

        else:
            terminals.append(language[0][char_ind])
            variables.append(terminals[-1])
            destination.append('1')

        language[0][char_ind] = ' '
    final_dict['variables'] = variables
    final_dict['terminals'] = terminals
    return final_dict


def create_rules(simple_language: dict) -> dict:
    productionMultiplicity = {}
    if list(simple_language['language'].items()).count(['1']):
        pass


if __name__ == '__main__':
    v1 = simplify_brackets('L(G) = {2^(2n)1 | n >= 0}')
    v19 = simplify_brackets('L(G) = {a^(2n+1)1^(2n)2^(m) | n, m >= 1}')
    v24 = simplify_brackets('L(G) = {(01)^(n)(12)^(n^(2)) | n >= 1}')
    v25 = simplify_brackets('L(G) = {1^(2)2^(n)0^(2n) | n >= 1}')

    print(f'{v1}\n\n{v19}\n\n{v24}\n\n{v25}')


# G = {V, T, S, P}
# S - constant
# V - variables (N, nonterminals, and T, terminals)
# T - terminals
# P - rules
# λ - empty

# v1 : L(G) = {2^(2n)1 | n >= 0}
# P = {S -> F1;
#      F -> λ;
#      F -> 2^(2)F }

# v19: L(G) = {a^(2n+1)1^(2n)2^(m) | n, m >= 1}
# v24: L(G) = {(01)^(n)(12)^(n^(2)) | n >= 1}
# v25: L(G) = {1^(2)2^(n)0^(2n) | n >= 1}
