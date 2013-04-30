from mini import Mini


def test_numbers():
    assert Mini().eval('') == []
    assert Mini().eval('42') == [42]
    assert Mini().eval('42 12') == [42, 12]


def test_variables():
    assert Mini({'a': 42}).eval('a') == [42]
    assert Mini().eval('a = 2 \n a') == [2, 2]


def test_operators():
    assert Mini().eval('(42 + 2)') == [44]
    assert Mini().eval('(42 + (2 * 4))') == [50]


def test_functions():
    assert Mini().eval('sum(10 20)') == [30]
    assert Mini().eval('sum(10 20 30)') == [60]


def test_if():
    assert Mini().eval('if 1 then 42 else 12') == [42]
    assert Mini().eval('if 0 then 42 else 12') == [12]


def test_lambdas():
    assert Mini().eval('addten = (b) -> (b + 10) \n addten(2)')[-1] == 12
    source = 'x = 10 \n addx = (a) -> (a + x) \n addx(2)'
    assert Mini().eval(source)[-1] == 12


def test_factorial():
    # 0 => 1
    #   => n * (n - 1)!
    source = '''
        factorial = (n) ->
            if n then
                (n * factorial((n - 1)))
            else
                1
        factorial(0)
        factorial(5)
    '''
    assert Mini().eval(source)[1:] == [1, 120]


# github.com/halst/mini
