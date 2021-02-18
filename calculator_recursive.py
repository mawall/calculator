from operator import add, sub, mul, truediv


def verify_input(s):
    if not s:
        raise ValueError('Empty expression')
    elif not isinstance(s, str):
        raise ValueError('s needs to be a string')


# Prefix Calculator
# -----------------

def solve_prefix_base_case(tokens: list, opdict: dict):
    if not tokens[-2].isdigit() or not tokens[-1].isdigit():
        raise ValueError(f'Malformatted input: {" ".join(tokens)}')
    try:
        return opdict[tokens[-3]](int(tokens[-2]), int(tokens[-1]))
    except KeyError:
        raise ValueError(f'Unknown operator: {tokens[-3]}')


def prefix_recursion(tokens: list, opdict: dict) -> float:
    if len(tokens) == 1 and tokens[0].isdigit():
        return int(tokens[0])
    elif len(tokens) == 3:
        return solve_prefix_base_case(tokens, opdict)
    elif len(tokens) >= 3 and tokens[0] in opdict.keys() and tokens[-3] in opdict.keys():
        return opdict[tokens[0]](prefix_recursion(tokens[1:-3], opdict),
                                 solve_prefix_base_case(tokens[-3:], opdict))
    elif len(tokens) >= 3 and tokens[0] in opdict.keys() and tokens[-1].isdigit():
        return opdict[tokens[0]](int(tokens[-1]),
                                 prefix_recursion(tokens[1:-1], opdict))
    else:
        raise ValueError(f'Malformatted input: {" ".join(tokens)}')


def prefix_calc(s: str) -> float:
    """ Prefix Calculator Recursive Implementation
    Time: O(N)
    Space: O(N) - potentially O(1)

    I assume this could be implemented in O(1) space complexity by using pointers to
    the first, last and last but two non-whitespace characters of the string s at the
    respective recursion level instead of using .split().
    """
    opdict = {'+': add, '-': sub, '*': mul, '/': truediv}
    verify_input(s)
    tokens = s.split()

    return prefix_recursion(tokens, opdict)


# Infix Calculator
# ----------------

def solve_infix_base_case(tokens: list, opdict: dict):
    if not tokens[-3].isdigit() or not tokens[-1].isdigit():
        raise ValueError(f'Malformatted input: {" ".join(tokens)}')
    try:
        return opdict[tokens[-2]](int(tokens[-3]), int(tokens[-1]))
    except KeyError:
        raise ValueError(f'Unknown operator: {tokens[-2]}')


def get_mid_operator_index(tokens):
    open_brackets = 0

    for i, token in enumerate(tokens):
        if token == '(':
            open_brackets += 1
        elif token == ')':
            open_brackets -= 1
        if open_brackets < 0:
            raise ValueError('Unmatched closing bracket')
        elif open_brackets == 0:
            return i + 1

    raise ValueError('Unmatched opening bracket')


def infix_recursion(tokens: list, opdict: dict) -> float:
    if not (tokens[0] == '(' and tokens[-1] == ')'):
        raise ValueError('Malformatted input: missing bracket/s')
    tokens = tokens[1:-1]

    if len(tokens) == 1 and tokens[0].isdigit():
        return int(tokens[0])
    elif len(tokens) == 3:
        return solve_infix_base_case(tokens, opdict)
    elif len(tokens) >= 3 and tokens[0].isdigit() and tokens[1] in opdict.keys():
        return opdict[tokens[1]](int(tokens[0]),
                                 infix_recursion(tokens[2:], opdict))
    elif len(tokens) >= 3 and tokens[-2] in opdict.keys() and tokens[-1].isdigit():
        return opdict[tokens[-2]](infix_recursion(tokens[:-2], opdict),
                                  int(tokens[-1]))
    elif len(tokens) >= 3 and tokens[0] == '(' and tokens[-1] == ')':
        op_i = get_mid_operator_index(tokens)
        if op_i == len(tokens):
            return infix_recursion(tokens, opdict)
        else:
            return opdict[tokens[op_i]](infix_recursion(tokens[:op_i], opdict),
                                        infix_recursion(tokens[op_i+1:], opdict))
    else:
        raise ValueError(f'Malformatted input: {" ".join(tokens)}')


def infix_calc(s: str) -> float:
    """ Infix Calculator Recursive Implementation
    Time: O(N)
    Space: O(N) - potentially O(1)

    Similar to prefix_calc above, I assume this could be implemented in O(1) space
    complexity by using pointers to the first, second, last and next to last
    non-whitespace characters of the string s at the respective recursion level
    instead of using .split().
    """
    opdict = {'+': add, '-': sub, '*': mul, '/': truediv}
    verify_input(s)
    tokens = s.split()

    return infix_recursion(tokens, opdict)
