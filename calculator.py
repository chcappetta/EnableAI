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

def full_calc(ai_name, user_name, blank):
    blank=""
    print(f"Welcome to Simple Calculator. Enter Exit to return to {ai_name}.")
    while True:
        print()
        func = input(f"Choose a function: +,-,*,/,% : ")
        if func.lower() == "exit":
            return("Exiting Calculator...")
        if func == "+":
            num1 = input("What is your first number? ")
            num2 = input("And the second? ")
            print()
            print(f"{num1} + {num2} = {addition(int(num1),int(num2))}")
            continue
        if func == "-":
            num1 = input("What is your first number? ")
            num2 = input("And the second? ")
            print()
            print(f"{num1} - {num2} = {subtraction(int(num1),int(num2))}")
            continue
        if func == "*":
            num1 = input("What is your first number? ")
            num2 = input("And the second? ")
            print()
            print(f"{num1} * {num2} = {multiplication(int(num1),int(num2))}")
            continue
        if func == "/":
            num1 = input("What is your first number? ")
            num2 = input("And the second? ")
            print()
            print(f"{num1} / {num2} = {division(int(num1),int(num2))}")
            continue
        if func == "%":
            num1 = input("What is your first number? ")
            num2 = input("And the second? ")
            print()
            print(f"{num1} % {num2} = {modulo(int(num1),int(num2))}")
            continue

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
        x= int(parts[0])
        op= parts[1]
        y= int(parts[2])
        return(f"{ai_name}: {x}{op}{y} = {quick_math(x,op,y)}")
