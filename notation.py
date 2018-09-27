# formula operators
operator = {
    # mathematical
    "+": (lambda a, b: a + b),
    "-": (lambda a, b: a - b),
    "*": (lambda a, b: a * b),
    "**": (lambda a, b: a ** b),
    "/": (lambda a, b: a // b if b > 0 else 0),
    "%": (lambda a, b: a % b if b > 0 else 0),
    # bitwise
    ">>": (lambda a, b: a >> b),
    "<<": (lambda a, b: a << b),
    "&": (lambda a, b: a & b),
    "|": (lambda a, b: a | b),
    "^": (lambda a, b: a ^ b),
    # relational
    "<": (lambda a, b: a < b),
    "<=": (lambda a, b: a <= b),
    ">": (lambda a, b: a > b),
    ">=": (lambda a, b: a >= b),
    "!=": (lambda a, b: a != b),
    "==": (lambda a, b: a == b),
}


def infix(formula: str, arg: int):
    """
    evaluation of infix expression
    :param formula: bytebeat formula
    :param arg:     time argument
    :return: int:
        computation result
    """
    characters = formula.replace("t", str(arg)).replace("/", "//")
    try:
        return eval(characters)
    except ZeroDivisionError:
        return 0


def postfix(formula: str, arg: int):
    """
    evaluation of postfix expression
    :param formula: bytebeat formula
    :param arg:     time argument
    :return: int:
        computation result
    """
    global operator
    stack = list()
    characters = formula.replace("t", str(arg))
    for c in characters.split():
        if c not in operator.keys():
            stack.append(int(c))
        else:
            y = stack.pop()
            x = stack.pop()
            stack.append(operator[c](x, y))
    return stack[0]
