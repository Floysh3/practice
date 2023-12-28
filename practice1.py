
OPZ = []
OPZ_stack = []

def E():
    global index
    if not T():
        return False
    if not E_():
        return False
    return True

def E_():
    global index
    if index >= len(expression):
        return True
    if expression[index] == '+' or expression[index] == '-':
        symb = expression[index]
        index += 1
        if not T():
            return False
        OPZ.append(symb)
        if not E_():
            return False
        return True
    return True

def T():
    global index
    if not F():
        return False
    if not T_():
        return False
    return True

def T_():
    global index
    if index >= len(expression):
        return True
    if expression[index] == '*' or expression[index] == '/':
        symbol = expression[index]
        index += 1
        if not F():
            return False
        OPZ.append(symbol)
        if not T_():
            return False
        return True
    return True

def F():
    global index
    if index >= len(expression):
        return False
    if '0' <= expression[index] <= '9':
        OPZ.append(expression[index])
        index += 1
        return True
    if expression[index] == '(':
        index += 1
        if not E():
            return False
        if expression[index] != ')':
            return False
        index += 1
        return True
    return False

def OPZ_evaluation():
    global OPZ_stack, OPZ
    for i in range(len(OPZ)):
        if '0' <= OPZ[i] <= '9':
            OPZ_stack.append(int(OPZ[i]))
        elif OPZ[i] in ['+', '-', '*', '/']:
            b = OPZ_stack.pop()
            a = OPZ_stack.pop()
            if OPZ[i] == '+':
                OPZ_stack.append(a + b)
            elif OPZ[i] == '-':
                OPZ_stack.append(a - b)
            elif OPZ[i] == '*':
                OPZ_stack.append(a * b)
            elif OPZ[i] == '/':
                OPZ_stack.append(a / b)
    if len(OPZ_stack) != 1:
        print("error")
    return OPZ_stack[0]

expression = input()
index = 0
try:
    if not E():
        raise Exception
    if index != len(expression):
        raise Exception
except:
    print("error")
else:
    print(OPZ_evaluation())