import re


def str_to_list(str_exp):
    li_ch = re.split(r'\s*([()+*/-])\s*', str_exp)
    li_ch = list(filter((lambda el: el != ''), li_ch))
    li_zn = ['(', ')', '+', '*', '/', '-']
    li_ch = list(map((lambda el: float(el) if el not in li_zn else el), li_ch))

    if li_ch[0] == '-' and isinstance(li_ch[1], float):
        li_ch[1] = -li_ch[1]
        li_ch.pop(0)

    li_zn = ['(', '+', '*', '/', '-']
    size = len(li_ch)
    j = 2  # ?3
    while j < size:
        if isinstance(li_ch[j], float) and li_ch[j - 1] == '-':
            if li_ch[j - 2] in li_zn:
                li_ch[j] = - li_ch[j]
                li_ch.pop(j - 1)
                size -= 1
                j -= 1
        j += 1

    return li_ch


def operation(math_operation, x, y):
    if math_operation == "+":
        return x + y
    elif math_operation == "-":
        return x - y
    elif math_operation == "/":
        return x / y
    elif math_operation == "*":
        return x * y

def calc(li_ch):
    while len(li_ch) > 1:
        while "(" in li_ch:
            r_index = (len(li_ch) - 1) - list(reversed(li_ch)).index("(")
            ind = li_ch.index(")")
            li_ch.pop(r_index)
            li_ch.pop(ind - 1)
            li_ch[r_index] = calc(li_ch[r_index:ind - 1])
            del li_ch[r_index + 1:ind - 1]

        while "/" in li_ch or "*" in li_ch:
            for el in li_ch:
                if el == '*' or el == '/':
                    res_i = li_ch.index(el)
                    li_ch[res_i - 1] = operation(el, li_ch[res_i - 1], li_ch[res_i + 1])
                    del li_ch[res_i:res_i + 2]

        while "+" in li_ch or "-" in li_ch:
            for el in li_ch:
                if el == '+' or el == '-':
                    res_i = li_ch.index(el)
                    li_ch[res_i - 1] = operation(el, li_ch[res_i - 1], li_ch[res_i + 1])
                    del li_ch[res_i:res_i + 2]
    return li_ch[0]


def calc_rational(data):
    li_ch = str_to_list(data)
    return calc(li_ch)
