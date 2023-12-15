def task_D1(input_str):
    states = ["S0", "S1", "S2", "S3"]
    input_alphabet = ["0", "1", "Q"]
    output_alphabet = ["0", "1", "P", "N"]
    transition_table = {
        "S0": {"0": ("S0", "0"), "1": ("S1", "1"), "Q": ("S2", "P")},
        "S1": {"0": ("S1", "0"), "1": ("S0", "1"), "Q": ("S3", "N")},
        "S2": {"0": ("S2", "0"), "1": ("S3", "1"), "Q": ("S1", "P")},
        "S3": {"0": ("S3", "0"), "1": ("S2", "1"), "Q": ("S0", "N")}
    }
    current_state = "S0"
    current_output = "0"
    output_sequence = []

    for symbol in input_str:
        if symbol not in input_alphabet:
            raise ValueError(f"Неправильний символ вхідного алфавіту: {symbol}")

        next_state, output_symbol = transition_table[current_state][symbol]
        current_state = next_state
        current_output = output_symbol
        output_sequence.append(output_symbol)

    return output_sequence

example = "0011Q0100Q1"
print(f"Варіант 1: {example} - {''.join(task_D1(example))}\n")


def task_D19(input_str):
    states = ["S0", "S1", "S2"]
    alphabet = ["0", "1", "2"]
    transition_table = {
        "S0": {"0": "S0", "1": "S1", "2": "S2"},
        "S1": {"0": "S2", "1": "S0", "2": "S2"},
        "S2": {"0": "S1", "1": "S2", "2": "S0"}
    }
    current_state = "S0"

    for symbol in input_str:
        current_state = transition_table[current_state][symbol]

    if current_state == "S0":
        return 0
    elif current_state == "S1":
        return 1
    else:
        return 2

print("Варіант 19:")
input_string_1 = "001122"
print(f"Для {input_string_1} - {task_D19(input_string_1)}")

input_string_3 = "012012"
print(f"Для {input_string_3} - {task_D19(input_string_3)}\n")


def task_D25(input_str):
    states = ["S0", "S1", "S2"]
    input_alphabet = ["0", "1"]
    output_alphabet = ["0", "1", "2"]
    transition_table = {
        "S0": {"0": ("S0", "0"), "1": ("S1", "1")},
        "S1": {"0": ("S0", "0"), "1": ("S2", "2")},
        "S2": {"0": ("S0", "0"), "1": ("S1", "1")}
    }
    current_state = "S0"
    current_output = "0"
    output_sequence = []

    for symbol in input_str:
        if symbol not in input_alphabet:
            raise ValueError(f"Неправильний символ вхідного алфавіту: {symbol}")

        next_state, output_symbol = transition_table[current_state][symbol]
        current_state = next_state
        current_output = output_symbol
        output_sequence.append(output_symbol)

    return output_sequence

input_sequence = "1101101"
print(f"Варіант 25: {input_sequence} - {''.join(task_D25(input_sequence))}")