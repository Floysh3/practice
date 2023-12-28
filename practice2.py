data = "(0+1)*011(0+1)*"
position = 0

# Класс для состояния НКА
class State:
    currentNumber = 0
    states = []  # глобальный список всех вершин

    def __init__(self):
        self.name = State.currentNumber  # в качестве имени присваиваем порядковый номер
        State.states.append(self)  # сохраняем новую вершину в глобальном списке вершин (для отладки)
        State.currentNumber += 1
        self.edges = {}  # ребра храним в хеш-таблице:
        # ключ - символ, значение - список вершин, в которые ведут ребра, помеченные этим символом

    def addEdge(self, symbol, state):  # метод добавления ребра с меткой symbol, ведущего в вершину state
        if (not (symbol in self.edges)):
            self.edges[symbol] = []
        self.edges[symbol].append(state)

    def __repr__(self):
        return (str(self.name))

    def __str__(self):
        return (str(self.name))

    def printEdges(self):  # печатаем содержимое вершины
        for symbol in self.edges:
            print("\t'" + symbol + "': " + str(self.edges[symbol]))


# функция печати НКА: выводит все вершины,
# созданные на текущий момент, и их ребра
def printStates():
    for state in State.states:
        print("State " + str(state))
        state.printEdges()
    print()


# мини-класс для хранения НКА - хранит только начальное и конечное состояния НКА
class NSM:
    def __init__(self, start, stop):
        self.startState = start
        self.stopState = stop

    def __repr__(self):
        return ("Start state is " + str(self.startState) + ", end state is " + str(self.stopState))

    def __getitem__(self, key):
        if key < len(State.states):
            return State.states[key]


# БАЗИС: создаем НКА для символа
def makeSymbolNSM(symbol):
    start = State()
    stop = State()
    start.addEdge(symbol, stop)
    return NSM(start, stop)


# ИНДУКЦИЯ: создаем автомат для регулярного выражения И
def makeAndNSM(leftNSM, rightNSM):
    for symbol in rightNSM.startState.edges:
        for state in rightNSM.startState.edges[symbol]:
            leftNSM.stopState.addEdge(symbol, state)
    return NSM(leftNSM.startState, rightNSM.stopState)


# ИНДУКЦИЯ: создаем автомат для регулярного выражения ИЛИ
def makeOrNSM(leftNSM, rightNSM):
    start = State()
    stop = State()
    start.addEdge('epsilon', leftNSM.startState)
    start.addEdge('epsilon', rightNSM.startState)
    leftNSM.stopState.addEdge('epsilon', stop)
    rightNSM.stopState.addEdge('epsilon', stop)
    return NSM(start, stop)


# ИНДУКЦИЯ: создаем автомат для регулярного выражения *
def makeClosureNSM(cNSM):
    start = State()
    stop = State()
    cNSM.stopState.addEdge('epsilon', cNSM.startState)
    start.addEdge('epsilon', cNSM.startState)
    start.addEdge('epsilon', stop)
    cNSM.stopState.addEdge('epsilon', stop)
    return NSM(start, stop)

def S():
    q = T()
    if q is None:
        return None

    p = S_(q)
    if p is None:
        return None

    return p

def S_(r):
    global position
    if position >= len(data):
        return r
    if data[position] not in ["0", "1", "(", ")", "+", "*"]:
        return None
    if data[position] == "+":
        position += 1
        q = T()
        if q is None:
            return None

        return S_(makeOrNSM(r,q))

    return r


def T():
    q = F()
    if q is None:
        return None

    p = T_(q)
    if p is None:
        return None

    return p

def T_(r):
    global position
    if position >= len(data):
        return r
    if data[position] not in ["0", "1", "(", ")", "+", "*"]:
        return None
    if data[position] in ["(", "0", "1"]:
        q = F()
        if q is None:
            return None

        p = T_(makeAndNSM(r,q))
        return p

    return r

def F():
    global position
    if position >= len(data):
        return None
    if data[position] not in ["0", "1", "(", ")", "+", "*"]:
        return None

    if data[position] in ["0", "1"]:
        q = makeSymbolNSM(data[position])
        position += 1
        return F_(q)

    if data[position] == "(":
        position += 1
        q = S()
        if q is None:
            return None
        if position >= len(data) or data[position] != ")":
            return None
        position += 1

        return F_(q)

    return None

def F_(q):
    global position
    if position >= len(data):
        return q

    if data[position] not in ["0", "1", "(", ")", "+", "*"]:
        return None

    if data[position] == "*":
        position += 1
        return makeClosureNSM(q)
    return q


def eClosure(T):
    stack = []
    e_closure = T[:]
    for i in T:
        stack.append(i)

    while stack != []:
        t = stack.pop(-1)
        if 'epsilon' in t.edges:
            for u in t.edges['epsilon']:
                if u not in e_closure:
                    e_closure.append(u)
                    stack.append(u)

    return e_closure

def emulate(NSM, word):
    position = 0
    S = eClosure([NSM.startState])
    while position < len(word):
        next = []
        for s in S:
            if word[position] in s.edges:
                for i in s.edges[word[position]]:
                    next.append(i)
        position +=1

        S = eClosure(next)

    for i in S:
        if i == NSM.stopState:
            return True

    return False

NSM = S()
if NSM is None or (position != len(data)):
    raise Exception('error')
else:
    print(emulate(NSM, "011010")) # проверяем принадлежит ли слово "011010" языку,
                                        # заданному регулярным выражением в переменной data
