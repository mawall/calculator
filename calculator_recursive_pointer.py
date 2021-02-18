from operator import add, sub, mul, truediv
from calculator import verify_input


def prefix_recursion(s, i, opdict):
    if i >= len(s):
        raise ValueError(f'Malformatted input')

    while s[i].isspace():
        i += 1
    token = s[i]

    if token.isdigit():
        j = i + 1
        while j < len(s) and s[j].isdigit():
            j += 1
        return float(s[i:j+1]), j
    else:
        try:
            operator = opdict[token]
        except KeyError as e:
            raise ValueError(f'Unknown operator: {token}') from e
        operand_1, i = prefix_recursion(s, i+1, opdict)
        operand_2, i = prefix_recursion(s, i+1, opdict)
        return operator(operand_1, operand_2), i


def prefix_calc(s):
    """ Prefix Calculator Recursive Pointer Implementation
    Time: O(N)
    Space: O(1)
    """
    verify_input(s)
    opdict = {'+': add, '-': sub, '*': mul, '/': truediv}
    result, i = prefix_recursion(s, 0, opdict)

    if not s[i:] or s[i:].isspace():
        return result
    else:
        raise ValueError(f'Malformatted input')