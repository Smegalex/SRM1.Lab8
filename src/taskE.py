E1 = [['S0', 'S1', '0'],
      ['S0', 'S0', '1'],
      ['S1', '', '0'],
      ['S1', 'S1', '1'],
      ['S1', 'S2', '1'],
      ['S2', 'S2', '0'],
      ['S2', '', '1']]

E19 = [['S0', 'S0', '0'],
       ['S0', 'S2', '1'],
       ['S1', '', '0'],
       ['S1', '', '1'],
       ['S2', 'S1', '0'],
       ['S2', 'S2', '1']]

E25 = [['S0', 'S1', '0'],
       ['S0', 'S2', '0'],
       ['S0', '', '1'],
       ['S1', 'S1', '0'],
       ['S1', 'S2', '1'],
       ['S2', '', '0'],
       ['S2', 'S2', '1']]


def task_E(transition_list):
    interminal_variables = {'S0': 'S', 'S1': 'A', 'S2': 'B'}

    def generate_grammar():
        grammar = []
        for i in range(len(transition_list)):
            start_str = interminal_variables.get(transition_list[i][0])
            end_str = interminal_variables.get(transition_list[i][1], '')
            if end_str == '':
                grammar.append(f"{start_str} -> {transition_list[i][2]}")
            else:
                grammar.append(f"{start_str} -> {transition_list[i][2]}{end_str}")
        return grammar

    grammar = generate_grammar()

    print("P: {", ", ".join(grammar), "}")


task_E(E1)
task_E(E19)
task_E(E25)
