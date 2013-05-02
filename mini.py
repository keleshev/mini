r"""
program = expr*

expr = ws (call | infix | assignment | name | number):expr ws -> expr

call = name:name '()' -> name()

infix = '(' expr:expr1 operator:operator expr:expr2 ')' -> operator(expr1, expr2)
operator = ('+' | '-' | '*' | '/'):op -> mini.operators[op]

assignment = lvalue:lvalue '=' expr:expr -> [mini.env.update({lvalue: expr}), expr][1]
lvalue = char+:ch ws -> ''.join(ch)

name = char+:ch ws -> mini.env.get(''.join(ch), -1)
char = :c ?(c in 'abcdefghijklmn') -> c

number = digit+:ds ws -> int(''.join(ds))
digit = :x ?(x in '0123456789') -> x

ws = (' ' | '\r' | '\n' | '\t')*
"""
import operator as op

from parsley import makeGrammar as grammar


class Mini(object):

    operators = {'+': op.add, '-': op.sub, '*': op.mul, '/': op.div}

    def __init__(self, env={}):
        env['sum'] = lambda *args: sum(args)
        self.env = env

    def eval(self, source):
        return grammar(__doc__, {'mini': self})(source).program()
