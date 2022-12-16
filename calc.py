from re_calc import calc_rational
from complex_calc import calc_compl


def check_data(data):
    li_char = ['(', ')', '+', '*', '/', '-', '.', 'i', 'j']
    for el in data:
        if not el.isdigit():
            if not el in li_char:
                res = 'В выражении недопустимые символы'
                return res

    if "j" in data or "i" in data:
        type_str = 'c'
    else:
        type_str = 'r'
    data_input = (type_str, data)

    return data_input


def calc_data(t, data):
    return calc_rational(data) if t == "r" else calc_compl(data)