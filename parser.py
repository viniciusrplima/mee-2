
def prod(rules, proc = lambda a,s: a): 
    return { 
        "rules": rules,
        "proc": proc
    }


def add(t, s):
    a = s.pop()
    b = s.pop()
    s.append(b + a)

def minus(t, s):
    a = s.pop()
    b = s.pop()
    s.append(b - a)

def multiply(t, s):
    a = s.pop()
    b = s.pop()
    s.append(b * a)

def divide(t, s):
    a = s.pop()
    b = s.pop()
    s.append(b / a)

def power(t, s):
    a = s.pop()
    b = s.pop()
    s.append(b ** a)


lang = {
    "S": [prod(["E"])], 
    "E": [prod(["T", "D"])], 
    "D": [
        prod(["+", "T", "D"], add), 
        prod(["-", "T", "D"], minus), 
        prod([])
    ],
    "T": [prod(["P", "R"])], 
    "R": [
        prod(["*", "P", "R"], multiply), 
        prod(["/", "P", "R"], divide), 
        prod([])
    ], 
    "P": [prod(["F", "Q"])], 
    "Q": [
        prod(["^", "F", "Q"], power), 
        prod([])
    ], 
    "F": [
        prod(["(", "E", ")"]), 
        prod(["C"])
    ],
    "C": [prod(["."], lambda a,s: s.append(a[0]))]
}


def parse(message, lang):
    message = message.replace(' ', '')
    stack = []
    done, tree, idx = make_tree("S", 0, stack, message, lang)

    if not done or idx < len(message)-1:
        raise Exception("syntax error")
    else:
        return stack[0]


def is_terminal(token, lang):
    return token not in lang.keys()


def make_tree(non_terminal, index, stack, message, lang):
    if is_terminal(non_terminal, lang):
        raise Exception(f'{non_terminal} is not a non-terminal')
    for production in lang[non_terminal]:
        done, tree, idx = try_production(
            production['rules'], 
            index, 
            stack, 
            message, 
            lang
        )

        if done:
            production['proc'](tree, stack)
            return True, tree, idx

    return False, None, None


def try_production(production, index, stack, message, lang):
    childs = []
    for term in production:
        if is_terminal(term, lang):
            if index >= len(message):
                return False, None, None
            elif term == message[index]:
                childs.append(message[index])
                index += 1
            elif term == '.':
                childs.append(int(message[index]))
                index += 1
            else:
                return False, None, None
        else:
            done, tree, idx = make_tree(term, index, stack, message, lang)
            if not done: return False, None, None
            if type(tree) is not list: childs.append(tree)
            elif len(tree) == 1: childs.append(tree[0])
            elif len(tree) > 0: childs.append(tree)
            index = idx
    return True, childs, index


message = input()
print(parse(message, lang))