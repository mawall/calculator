from operator import add, sub, mul, truediv

opdict = {'+': add, '-': sub, '*': mul, '/': truediv}


def verify_input(s: str) -> None:
    if not s:
        raise ValueError('Empty expression')
    elif not isinstance(s, str):
        raise ValueError('s needs to be a string')


def pop_operand_from_stack(stack: list) -> float:
    try:
        operand = float(stack.pop())
    except IndexError as e:
        raise ValueError(f'Malformatted input') from e

    return operand


def apply_operator_to_one_operand_on_stack(operator: str,
                                           operand_1: float,
                                           stack: list) -> None:
    operand_2 = pop_operand_from_stack(stack)
    try:
        stack.append(str(opdict[operator](operand_1, operand_2)))
    except KeyError as e:
        raise ValueError(f'Unknown operator: {operator}') from e


def apply_operator_to_two_operands_on_stack(operator: str, stack: list) -> None:
    operand_1 = pop_operand_from_stack(stack)
    apply_operator_to_one_operand_on_stack(operator, operand_1, stack)


def calculate_prefix(s: str) -> float:
    """ Prefix Calculator: Shunting-yard Implementation
    Time Complexity: O(N)
    Space Complexity: O(1) expected case - operators frequently encountered
                      O(N) worst case - operators all at beginning of expression
    """
    verify_input(s)
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
            apply_operator_to_two_operands_on_stack(token, stack)
            last_seen_digit = False
        else:
            last_seen_digit = False

    if len(stack) > 1:
        raise ValueError(f'Malformatted input')
    else:
        return float(stack.pop())


def calculate_infix(s: str) -> float:
    """Infix Calculator: Shunting-yard Implementation
    Time Complexity: O(N)
    Space Complexity: O(1) expected case
                      O(N) worst case - deeply nested brackets
    """
    verify_input(s)
    operator_stack = []
    result_stack = []
    last_seen_digit = False

    for token in s[::-1]:
        if token.isdigit():
            if operator_stack and operator_stack[-1] in opdict:
                operator = operator_stack.pop()
                apply_operator_to_one_operand_on_stack(operator,
                                                       float(token),
                                                       result_stack)
            elif last_seen_digit:
                last_token = result_stack.pop()
                result_stack.append(token + last_token)
            else:
                result_stack.append(token)
            last_seen_digit = True
        elif token == '(':
            if operator_stack and operator_stack[-1] == ')':
                operator_stack.pop()
            elif len(operator_stack) >= 2 \
                    and operator_stack[-1] in opdict \
                    and operator_stack[-2] == ')':
                operator = operator_stack.pop()
                apply_operator_to_two_operands_on_stack(operator, result_stack)
                operator_stack.pop()
            else:
                raise ValueError(f'Malformatted input')
            last_seen_digit = False
        elif not token.isspace():
            operator_stack.append(token)
            last_seen_digit = False
        else:
            last_seen_digit = False

    if operator_stack or len(result_stack) > 1:
        raise ValueError(f'Malformatted input')
    else:
        return float(result_stack.pop())
