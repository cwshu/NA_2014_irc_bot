#!/usr/bin/python3
import re
def cal(exp):
    if re.findall(r"([0-9+\-*/.()\^]*)", exp)[0] != exp:
        # check no special characters
        return "special char"
    
    double_star_or_divide = re.findall(r"[*]{2}|[/]{2}", exp)
    if double_star_or_divide:
        return "double_star_or_divide"

    exp = exp.replace("^", "**")
    print(exp)
    try:
        val = eval(exp)
    except SyntaxError:
        return "syntax error"
    except ZeroDivisionError:
        return "overflow"
    else:
        return val
#    exp_without_parenthesis = exp.replace("(", "").replace(")", "")
#    # print(exp_without_parenthesis)
#    m = re.match(r"([\d]*\.[\d]*[+\-*/^])*[\d]*\.[\d]", exp) # token list ignoring '(', ')'
#    if m.group()

            
while 1:
    exp = input()
    print(cal(exp))

"""
token_map = {'+':'ADD', '-':'ADD',
             '*':'MUL', '/':'MUL',
             '(':'LPAR', ')':'RPAR'}

print('[\d.]+|[%s]' % ''.join(token_map))
"""
