from operator import add, sub, mul, truediv


def verify_input(s: str) -> None:
    if not s:
        raise ValueError('Empty formula')
    elif not isinstance(s, str):
        raise ValueError('s needs to be a string')


def prefix_calc(s: str) -> float:
    verify_input(s)
    opdict = {'+': add, '-': sub, '*': mul, '/': truediv}
    stack = []
    last_seen_digit = False
    for token in s[::-1]:
        if token.isdigit():
            if last_seen_digit:
                last_token = stack.pop()
                stack.append(token + last_token)
            else:
                stack.append(token)
            last_seen_digit = True
        elif not token.isspace():
            try:
                token_1 = float(stack.pop())
                token_2 = float(stack.pop())
            except IndexError as e:
                raise ValueError(f'Malformatted input') from e

            try:
                stack.append(str(opdict[token](token_1, token_2)))
            except KeyError as e:
                raise ValueError(f'Unknown operator: {token}') from e
            last_seen_digit = False
        else:
            last_seen_digit = False

    if len(stack) > 1:
        raise ValueError(f'Malformatted input')
    else:
        return float(stack.pop())


def infix_to_prefix(s: str) -> str:
    stack = []
    prefix_s = ''
    last_seen_digit = False

    for token in s[::-1]:
        if token in ['+', '-', '*', '/']:
            while stack and stack[-1] != ')':
                prefix_s += ' ' + stack.pop()
            stack.append(token)
            last_seen_digit = False
        elif token == ')':  # opening bracket
            stack.append(token)
            last_seen_digit = False
        elif token == '(':  # closing bracket
            try:
                while stack[-1] != ')':
                    prefix_s += ' ' + stack.pop()
            except IndexError as e:
                raise ValueError(f'Malformatted input') from e
            stack.pop()
            last_seen_digit = False
        elif token.isdigit():
            if last_seen_digit:
                prefix_s += token
            else:
                prefix_s += ' ' + token
            last_seen_digit = True
        else:
            last_seen_digit = False

    while stack:
        prefix_s += ' ' + stack.pop()

    return prefix_s[1:][::-1]


def infix_calc(s: str) -> float:
    verify_input(s)
    prefix_s = infix_to_prefix(s)

    return prefix_calc(prefix_s)
