import numpy as np

#1

def task_D1():
    states = ["S0", "S1", "S2", "S3", "S4"]
    input_alphabet = {0, 1, 'Q'}
    output_alphabet = {0, 1, 'P', 'N'}
    initial_state = "S0"

    def transition_function(state, symbol):
        if symbol == 'Q':
            count_ones = count_1(state)
            return 'P' if count_ones % 2 == 0 else 'N'
        elif symbol == 0 or symbol == 1:
            return state
        else:
            raise ValueError("Invalid input symbol")

    def count_1(state):
        return sum(int(bit) for bit in state[1:])

    def build_state_table(states, input_alphabet):
        res = []
        for state in states:
            row = [state]
            for symbol in input_alphabet:
                next_state = transition_function(state, symbol)
                row.extend([next_state])
            res.append(row)
        return np.array(res)

    print("  Стан     0   1   Q")
    print(build_state_table(states, input_alphabet))


task_D1()


#19

def task_D19():
    states = ["S0", "S1", "S2", "S3", "S4"]
    alphabet = ["0", "1", "2"]
    accepting_states = ["S0", "S2", "S4"]

    delta = {
        "S0": {"0": "S1", "1": "S4", "2": "S4"},
        "S1": {"0": "S2", "1": "S4", "2": "S4"},
        "S2": {"0": "S3", "1": "S4", "2": "S4"},
        "S3": {"0": "S3", "1": "S3", "2": "S3"},
        "S4": {"0": "S4", "1": "S4", "2": "S4"},
    }

    def DFA(input_string):
        current_state = "S0"
        for symbol in input_string:
            if symbol not in alphabet:
                return "Invalid input symbol"
            current_state = delta[current_state][symbol]

        return current_state

    def process_input(input_string):
        result = DFA(input_string)
        if result in accepting_states:
            return "0"
        elif result == "S1":
            return "1"
        else:
            return "2"

    def build_state_table():
        res = []
        for state in states:
            row = [state]
            for symbol in alphabet:
                row.append(delta[state][symbol])
            res.append(row)
        return np.array(res)

    print("\nDFA_19:")
    print("  Стан    0   1   2")
    print(build_state_table())


task_D19()





#25

def task_D25():
    alphabet = [0, 1]
    states = ["S0", "S1", "S2", "S3", "S4"]

    def DFA(state):
        res = []
        k = 0
        for i in state:
            res.append(i)
            if k < len(state) - 1 and state[k] == "S1" and state[k + 1] == "S1":
                res.append("2")
            else:
                res.append(state[0])
            if k == len(state) - 1:
                res.append("-")
            else:
                res.append(state[k + 1])
            k += 1
        res = np.array(res).reshape(len(state), 3)
        return res

    print("\nDFA_25:")
    print("  Стан   0   1")
    print(DFA(states))


task_D25()



