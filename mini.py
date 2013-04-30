import operator as op

from parsimonious.grammar import Grammar


class Mini(object):

    def __init__(self, env={}):
        env['sum'] = lambda *args: sum(args)
        self.env = env

    def parse(self, source):
        grammar = '\n'.join(v.__doc__ for k, v in vars(self.__class__).items()
                      if '__' not in k and hasattr(v, '__doc__') and v.__doc__)
        return Grammar(grammar)['program'].parse(source)

    def eval(self, source):
        node = self.parse(source) if isinstance(source, str) else source
        method = getattr(self, node.expr_name, lambda *a: 'error')
        if node.expr_name in ['ifelse', 'func']:
            return method(node)
        return method(node, [self.eval(n) for n in node])

    def program(self, node, children):
        'program = statement*'
        return children

    def statement(self, node, children):
        'statement = _ expr _'
        return children[1]

    def expr(self, node, children):
        'expr = func / ifelse / call / infix / assignment / number / name'
        return children[0]

    def func(self, node):
        'func = "(" parameters ")" _ "->" _ expr _'
        _, params, _, _, _, _, expr, _ = node
        params = map(self.eval, params)
        def func(*args):
            env = dict(self.env.items() + zip(params, args))
            return Mini(env).eval(expr)
        return func

    def parameters(self, node, children):
        'parameters = lvalue*'
        return children

    def ifelse(self, node):
        'ifelse = "if" _ expr _ "then" _ expr _ "else" _ expr _'
        _, _, cond, _, _, _, cons, _, _, _, alt, _ = node
        return self.eval(cons) if self.eval(cond) else self.eval(alt)

    def call(self, node, children):
        'call = name "(" arguments ")" _'
        name, _, arguments, _, _ = children
        return name(*arguments)

    def arguments(self, node, children):
        'arguments = argument*'
        return children

    def argument(self, node, children):
        'argument = expr _'
        return children[0]

    def infix(self, node, children):
        'infix = "(" _ expr _ operator _ expr _ ")" _'
        _, _, expr1, _, operator, _, expr2, _, _, _ = children
        return operator(expr1, expr2)

    def operator(self, node, children):
        'operator = "+" / "-" / "*" / "/"'
        operators = {'+': op.add, '-': op.sub, '*': op.mul, '/': op.div}
        return operators[node.text]

    def assignment(self, node, children):
        'assignment = lvalue _ "=" _ expr _'
        lvalue, _, _, _, expr, _ = children
        self.env[lvalue] = expr
        return expr

    def lvalue(self, node, children):
        'lvalue = ~"[a-z]+" _'
        return node.text.strip()

    def name(self, node, children):
        'name = ~"[a-z]+" _'
        return self.env.get(node.text.strip(), -1)

    def number(self, node, children):
        'number = ~"[0-9]+" _'
        return int(node.text)

    def _(self, node, children):
        '_ = ~"\s*"'
