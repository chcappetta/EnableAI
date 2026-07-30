def modulo(x,y):
    return x%y

def division(x,y):
    return x/y

def multiplication(x,y):
    return x*y

def addition(x,y):
    return x+y

def subtraction(x,y):
    return x-y

def full_calc(ai_name, user_name, args):
    """
    Non-interactive wrapper for the calculator.
    If `args` is provided and looks like: "3 + 4" it will compute the result.
    Otherwise, returns a usage message (interactive mode is not supported in the TUI).
    """
    if args and args.strip():
        try:
            parts = args.split()
            if len(parts) == 3:
                x = int(parts[0])
                op = parts[1]
                y = int(parts[2])
                res = quick_math(x, op, y)
                return f"{ai_name}: {x}{op}{y} = {res}"
            else:
                return f"{ai_name}: Usage (non-interactive): /calc x op y  (e.g. /calc 3 + 4). For simple expressions use /math x op y."
        except Exception as e:
            return f"{ai_name}: Error parsing expression: {e}"
    else:
        return f"{ai_name}: Interactive calculator not available in this UI. Use /math x op y."


def quick_math(x,op,y):

    if op == "+":
        return addition(x, y)
    if op == "-":
        return subtraction(x, y)
    if op == "*":
        return multiplication(x, y)
    if op == "/":
        return division(x, y)
    if op == "%":
        return modulo(x, y)
    return None

def quick_calc(ai_name, user_name, args):
    parts = args.split()
    if len(parts) < 3:
        return f"{ai_name}: Usage: /math x op y (e.g. /math 3 + 4)"
    try:
        x = int(parts[0])
        op = parts[1]
        y = int(parts[2])
        return(f"{ai_name}: {x}{op}{y} = {quick_math(x,op,y)}")
    except Exception as e:
        return f"{ai_name}: Error parsing expression: {e}"
