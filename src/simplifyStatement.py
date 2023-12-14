operations = ("^", "*", "/", "+", "-")


def standartise_statement(statement):
    return statement.replace(" ", "").replace("÷", "/").replace(":", "/").replace("×", "*").replace("·", "*").replace("−", "-")


def doubling_arrays_remove(statement: list, prev=None) -> list:
    if len(statement) == 1 and isinstance(statement, list):
        statement = statement[0]
    if prev == 'list' and len(statement) == 1 and isinstance(statement[0], list):
        return ["doubling"]

    # elif prev == '' and len(statement)==1 and isinstance(statement[0], list):
    #    return ["doubling"]
    for i in range(len(statement)):
        if isinstance(statement[i], list):
            doubling_check = doubling_arrays_remove(statement[i], prev='list')
            if doubling_check == ["doubling"]:
                statement[i] = statement[i][0]
    return statement


def separated_numbers_connect(statement: list) -> list:
    final_statement = []
    for i in range(len(statement)):
        if isinstance(statement[i], list):
            final_statement.append(separated_numbers_connect(statement[i]))
            continue
        if statement[i] in operations:
            final_statement.append(statement[i])
            continue
        if i > 0:
            if final_statement[i-1] not in operations:
                final_statement[i-1] += statement[i]
                final_statement.append("")
                continue
        final_statement.append(statement[i])
    final_statement = list(filter(None, final_statement))
    return final_statement


def brackets_simplifying(statement: str) -> list:
    transformed_statement = []
    brackets_embeddedness = 0
    statement_embeddedness = transformed_statement
    for i in range(len(statement)):
        if statement[i] == "(":
            brackets_embeddedness += 1
            statement_embeddedness.append([])

            statement_embeddedness = transformed_statement
            for j in range(brackets_embeddedness):
                statement_embeddedness = statement_embeddedness[-1]
        elif statement[i] == ")":
            brackets_embeddedness += -1

            statement_embeddedness = transformed_statement
            for j in range(brackets_embeddedness):
                statement_embeddedness = statement_embeddedness[-1]
        else:
            statement_embeddedness.append(statement[i])
    transformed_statement = separated_numbers_connect(transformed_statement)
    return transformed_statement


def brackets_enclosing(statement: list) -> list:
    operation_chroniches = {}
    if len(statement) == 3:
        for i in range(len(statement)):
            if isinstance(statement[i], list):
                statement[i] = brackets_enclosing(statement[i])
        statement = doubling_arrays_remove(statement)
        return statement
    else:
        for i in range(len(statement)):
            if isinstance(statement[i], list):
                statement[i] = brackets_enclosing(statement[i])
                continue
            if statement[i] in operations:
                operation_chroniches[i] = statement[i]
        for ind in range(len(list(operation_chroniches.keys()))):
            for oper in operations:
                while list(operation_chroniches.values()).count(oper):
                    ind = list(operation_chroniches.keys())[
                        list(operation_chroniches.values()).index(oper)]
                    for j in reversed(range(0, ind)):
                        if statement[j] == "":
                            continue
                        for k in range(ind+1, len(statement)):
                            if statement[k] == "":
                                continue
                            statement[ind] = list(
                                filter(None, statement[j:k+1]))
                            statement[j] = ""
                            statement[k] = ""
                            break
                        break

                    operation_chroniches.pop(ind)
            statement = list(filter(None, statement))
    statement = list(filter(None, statement))
    statement = doubling_arrays_remove(statement)
    return statement


def simplify_arythmetic_statement(statement):
    statement = standartise_statement(statement)
    if "(" in statement:
        statement = brackets_simplifying(statement)
    statement = brackets_enclosing(statement)
    statement = doubling_arrays_remove(statement)
    return statement
