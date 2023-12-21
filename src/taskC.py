operations = ("^", "*", "/", "+", "-")

possible_termVar_pairs = {'a': 'A', 'b': 'B',
                          'c': 'C', '0': 'Z', '1': 'O', '2': 'T'}
possible_vars = ['S', 'F', 'R']


class Language:
    language = {}
    arguments = {}
    variables = []
    terminals = []

    def __init__(self, *args) -> None:
        if len(args) == 1:
            self.dict_to_lang(args[0])
            return
        else:
            fillable = [self.language, self.arguments,
                        self.variables, self.terminals]
            for arg_ind in range(len(args)):
                fillable[arg_ind] = args[arg_ind]

    def lang_to_dict(self) -> dict:
        return {'language': self.language, 'arguments': self.arguments, 'variables': self.variables, 'terminals': self.terminals}

    def dict_to_lang(self, dictionary: dict) -> None:
        self.language = dictionary['language']
        self.arguments = dictionary['arguments']
        self.variables = dictionary['variables']
        self.terminals = dictionary['terminals']


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


# знайти індекс в terms/vars мови для конкретного повторення степеня
def find_index_of_occurence(simple_language: dict, term: str, occur_ind: int, arr: str, direction: int = 1) -> int:
    if direction == 1:
        temp_vars = simple_language[arr]
        for i in range(occur_ind):
            temp_vars[temp_vars.index(term)] = ''
        return temp_vars.index(term)
    if direction == -1:
        temp_vars = simple_language[arr][:occur_ind]
        return temp_vars.count(term)


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
    recursion_pow = str(eval(recursion_pow))
    return recursion_pow


def merge_languages(main_productionMultiplicity: dict, added_productionMultiplicity: dict, name_higher: str or None = None, index_add: int = 0) -> dict:
    if len(added_productionMultiplicity) == 1:
        return {**main_productionMultiplicity, **added_productionMultiplicity}
    elif name_higher:
        main_productionMultiplicity[name_higher][
            index_add] = f'{added_productionMultiplicity.pop("add_higher")}{list(added_productionMultiplicity.items())[0][0]}'
        print({**main_productionMultiplicity, **added_productionMultiplicity})
        return {**main_productionMultiplicity, **added_productionMultiplicity}


def first_power_check(simple_language: dict, recursion_pow: list, variable_name: str, recursion_term: str) -> dict:
    first_pow = pow_at_first_arg(simple_language, recursion_pow)
    if first_pow == '0':
        shift = 0
        while first_pow == '0':
            shift += 1
            first_pow = pow_at_first_arg(
                simple_language, recursion_pow, shift)
        if first_pow == '1':
            return {'add_higher': '', variable_name: [f'{recursion_term}{variable_name}', 'λ']}
        else:
            return {'add_higher': '', variable_name: [f'{recursion_term}^({first_pow}){variable_name}', 'λ']}

    elif first_pow == '1':
        return {'add_higher': 'recursion_term', variable_name: [f'{recursion_term}{variable_name}', 'λ']}
    else:
        return {'add_higher': f'{recursion_term}^{first_pow}', variable_name: [f'{recursion_term}^{first_pow}{variable_name}', 'λ']}


def create_rules(simple_language: dict, variable_name: str = None) -> dict:
    productionMultiplicity = {}
    if len(simple_language['terminals']) == 1:
        recursion_term = simple_language['terminals'][0]
        recursion_pow = simple_language['language'][recursion_term][0]

        if not variable_name:
            if recursion_term in possible_termVar_pairs:
                variable_name = possible_termVar_pairs[recursion_term]
            else:
                variable_name = possible_vars.pop(0)

        return first_power_check(simple_language, recursion_pow, variable_name, recursion_term)

    temp_rule = [''] * len(simple_language['terminals'])

    print(simple_language['language'].items())
    for terminal, powers in simple_language['language'].items():
        for pow_ind in range(len(powers)):
            # якщо степінь без n/m
            if not isinstance(powers[pow_ind], list):
                if powers[pow_ind] != '1':
                    temp_rule[find_index_of_occurence(
                        simple_language, terminal, pow_ind, 'terminals')] = f'{terminal}^{powers[pow_ind]}'
                elif powers[pow_ind] == '1':
                    temp_rule[find_index_of_occurence(
                        simple_language, terminal, pow_ind, 'terminals')] = f'{terminal}'

    # записати "дірки" (місця, де степіь має в собі n або m)
    holes_indxs = []
    temp_rule_reduced_holes = []
    for i in range(len(temp_rule)):
        if temp_rule[i] == '':
            if holes_indxs == []:
                holes_indxs.append([])
            holes_indxs[-1].append(i)
            continue
        try:
            if holes_indxs[-1] != []:
                temp_rule_reduced_holes.append('')
                raise IndexError
        except IndexError:
            holes_indxs.append([])

        temp_rule_reduced_holes.append(temp_rule[i])
    if holes_indxs[-1] == []:
        holes_indxs = holes_indxs[:-1]
    else:
        temp_rule_reduced_holes.append('')

    if not variable_name:
        variable_name = possible_vars.pop(0)

    productionMultiplicity = {variable_name: temp_rule_reduced_holes}

    if len(holes_indxs) == 1:
        termPower_couples = {}

        for hole_el_ind in holes_indxs[0]:
            current_term = simple_language['terminals'][hole_el_ind]
            current_power = simple_language['language'][current_term][find_index_of_occurence(
                simple_language, current_term, hole_el_ind, 'terminals', -1)]
            termPower_couples[current_term] = current_power

        powers = list(termPower_couples.values())
        if (powers.count('n') and not powers.count('m')) or (powers.count('m') and not powers.count('n')):
            for power in powers:
                term = simple_language['terminals'][powers.index(power)]
                first_power_check(simple_language, power,
                                  variable_name, term)
        else:
            pass

    # пройтися по "дірках", де є степіні n або m
    for hole in holes_indxs:
        adding_lang = {'language': {
        }, 'arguments': simple_language['arguments'], 'variables': simple_language['variables'], 'terminals': []}
        for hole_el_ind in hole:
            current_term = simple_language['terminals'][hole_el_ind]
            current_power = simple_language['language'][current_term][find_index_of_occurence(
                simple_language, current_term, hole_el_ind, 'terminals', -1)]
            adding_lang['language'][current_term] = [current_power]
            adding_lang['terminals'].append(current_term)
        productionMultiplicity = merge_languages(
            productionMultiplicity, create_rules(adding_lang), variable_name, holes_indxs.index(hole))

    print(simple_language)
    return productionMultiplicity


"""
if len(simple_language['terminals']) == 1:
        recursion_ind = temp_rule.index('')
        recursion_term = simple_language['terminals'][recursion_ind]
        recursion_pow = simple_language['language'][recursion_term][find_index_of_occurence(
            simple_language, recursion_term, recursion_ind, 'terminals')]
        simple_language['terminals'].pop(
            recursion_ind)
        simple_language['variables'].append(poss_vars.pop(0))
        temp_rule[recursion_ind] = simple_language['variables'][-1]
        productionMultiplicity['S'] = temp_rule

        temp_rule = [''] * 2
        temp_rule[0] = simple_language['variables'][-1]

        recursion_pow = pow_at_first_arg(simple_language, recursion_pow)
        temp_rule[1] = f'{recursion_term}^'"""

if __name__ == '__main__':
    v1 = simplify_brackets('L(G) = {2^(2n)1 | n >= 0}')
    v19 = simplify_brackets('L(G) = {a^(2n+1)1^(2n)2^(m) | n, m >= 1}')
    v24 = simplify_brackets('L(G) = {(01)^(n)(12)^(n^(2)) | n >= 1}')
    v25 = simplify_brackets('L(G) = {1^(2)2^(n)0^(2n) | n >= 1}')
    print(create_rules(v1))
    print(create_rules(v25))
    # print(f'{v1}\n\n{v19}\n\n{v24}\n\n{v25}')


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
