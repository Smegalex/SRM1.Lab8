operations = ("^", "*", "/", "+", "-")

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
            try:
                power = int(''.join(power))
                power = str(power)
            except ValueError:
                pass
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
    final_dict = power_simplification(final_dict)
    return final_dict


def power_simplification(simple_language: dict) -> dict:
    for terminal, powers in simple_language['language'].items():
        for pow_ind in range(len(powers)):
            power = ''.join(powers[pow_ind])
            if power.count('+'):
                split_power = power.split('+')
                destination = simple_language['language'][terminal]

                if len(split_power[0]) > 1:
                    destination[pow_ind] = list(split_power[0])
                elif len(split_power[0]) == 1:
                    destination[pow_ind] = split_power[0]

                simple_language['variables'].insert(
                    find_index_of_occurence(simple_language, terminal, pow_ind, 'variables'), terminal)
                simple_language['terminals'] = simple_language['variables'][1:]

                if len(split_power[1]) > 1:
                    destination.insert(pow_ind+1, list(split_power[1]))
                elif len(split_power[1]) == 1:
                    destination.insert(pow_ind+1, split_power[1])
    return simple_language


def find_index_of_occurence(simple_language: dict, terminal: str, occur_ind: int, arr: str) -> int:
    temp_vars = simple_language[arr]
    for i in range(occur_ind):
        temp_vars[temp_vars.index(terminal)] = ''
    return temp_vars.index(terminal)


def pow_at_first_arg(simple_language: dict, recursion_pow: list, shift: int = 0) -> str:
    recursion_pow = ''.join(recursion_pow)
    if recursion_pow.count('n'):
        recursion_pow = recursion_pow.replace(
            'n', str(int(simple_language['arguments']['n'])+shift))
    elif recursion_pow.count('m'):
        recursion_pow.replace(
            'm', str(int(simple_language['arguments']['m'])+shift))
    recursion_pow = list(recursion_pow)
    stop = False
    while True:
        for i in range(1, len(recursion_pow)):
            if recursion_pow[i-1] not in operations and recursion_pow[i] not in operations:
                recursion_pow.insert(i, '*')
                break
            if i == len(recursion_pow)-1:
                stop = True
        if stop:
            break
    recursion_pow = ''.join(recursion_pow)
    recursion_pow = eval(recursion_pow)
    return recursion_pow


def create_rules(simple_language: dict, poss_vars: list = possible_vars) -> dict:
    productionMultiplicity = {}
    temp_rule = [''] * len(simple_language['terminals'])
    for terminal, powers in simple_language['language'].items():
        for pow_ind in range(len(powers)):
            if not isinstance(powers[pow_ind], list):
                if powers[pow_ind] != '1':
                    temp_rule[find_index_of_occurence(
                        simple_language, terminal, pow_ind, 'terminals')] = f'{terminal}^{powers[pow_ind]}'
                elif powers[pow_ind] == '1':
                    temp_rule[find_index_of_occurence(
                        simple_language, terminal, pow_ind, 'terminals')] = f'{terminal}'
    if temp_rule.count('') == 1:
        recursion_ind = temp_rule.index('')
        recursion_term = simple_language['terminals'][recursion_ind]
        recursion_pow = simple_language['language'][recursion_term][find_index_of_occurence(
            simple_language, recursion_term, recursion_ind, 'terminals')]
        simple_language['variables'].append(poss_vars.pop(0))
        temp_rule[recursion_ind] = simple_language['variables'][-1]
        productionMultiplicity['S'] = temp_rule

        temp_rule = [''] * 2
        temp_rule[0] = simple_language['variables'][-1]

        recursion_pow = pow_at_first_arg(simple_language, recursion_pow)
        temp_rule[1] = f'{recursion_term}^'


if __name__ == '__main__':
    v1 = simplify_brackets('L(G) = {2^(2n)1 | n >= 0}')
    v19 = simplify_brackets('L(G) = {a^(2n+1)1^(2n)2^(m) | n, m >= 1}')
    v24 = simplify_brackets('L(G) = {(01)^(n)(12)^(n^(2)) | n >= 1}')
    v25 = simplify_brackets('L(G) = {1^(2)2^(n)0^(2n) | n >= 1}')
    create_rules(v1)
    # print(f'{v1}\n\n{v19}\n\n{v24}\n\n{v25}')

    print("v1 : L(G) = {2^(2n)1 | n >= 0}\n", "P = {S -> F1;\n",
          "     F -> 2^(2)F;\n", "     F -> λ }\n\n")
    print("v19: L(G) = {a^(2n+1)1^(2n)2^(m) | n, m >= 1}\n", "P = {S -> a^(2)Fa1^(2)R2;\n",
          "     F -> a^(2)FO^(2);\n", "     O^(2)a -> aO^(2);\n", "     aO^(2) -> a1^(2);\n",
          "     F -> λ;\n", "     R -> R2;\n", "     R -> λ }\n\n")
    print("v25: L(G) = {1^(2)2^(n)0^(2n) | n >= 1}\n", "P = {S -> 1^(2)2F0^(2);\n",
          "     F -> 2F0^(2);\n", "     F -> λ }\n")


# G = {V, T, S, P}
# S - constant
# V - variables (N, nonterminals, and T, terminals)
# T - terminals
# P - rules
# λ - empty

# v1 : L(G) = {2^(2n)1 | n >= 0}
# P = {S -> F1;
#      F -> 2^(2)F;
#      F -> λ }

# v19: L(G) = {a^(2n+1)1^(2n)2^(m) | n, m >= 1}
# P = {S -> a^(2)Fa1^(2)R2;
#      F -> a^(2)FO^(2);
#      O^(2)a -> aO^(2);
#      aO^(2) -> a1^(2);
#      F -> λ;
#      R -> R2;
#      R -> λ }

# v24: L(G) = {(01)^(n)(12)^(n^(2)) | n >= 1}
# v25: L(G) = {1^(2)2^(n)0^(2n) | n >= 1}
# P = {S -> 1^(2)2F0^(2);
#      F -> 2F0^(2);
#      F -> λ }
