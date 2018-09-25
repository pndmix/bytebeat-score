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
    operator = {
        "+": (lambda a, b: a + b),
        "-": (lambda a, b: a - b),
        "*": (lambda a, b: a * b),
        "/": (lambda a, b: a // b if b > 0 else 0),
        "%": (lambda a, b: a % b if b > 0 else 0),
        ">": (lambda a, b: a >> b),
        "<": (lambda a, b: a << b),
        "&": (lambda a, b: a & b),
        "|": (lambda a, b: a | b),
        "^": (lambda a, b: a ^ b),
    }
    stack = []
    characters = formula.replace("t", str(arg)).replace(">>", ">").replace("<<", "<")
    for c in characters.split():
        if c not in operator.keys():
            stack.append(int(c))
        else:
            y = stack.pop()
            x = stack.pop()
            stack.append(operator[c](x, y))
    return stack[0]


# formula notation dictionary
notation = {
    "infix":   (lambda f, t: infix(f, t)),
    "postfix": (lambda f, t: postfix(f, t)),
}
