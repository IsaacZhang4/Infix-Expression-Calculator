from Calculator import Calculator
from AdvancedCalculator import AdvancedCalculator


def run_tests():
    # Testing Calculator
    CalcBasic = Calculator()

    # Calculator takes infix expressions
    expressions = [
        '4 + 3 - 2',
        '-2 + 3.5',
        '7 ^ 2 ^ 3',
        '( 3.5 ) [ 15 ]',
        '3 { 5 } - 15 + 85 [ 12 ]'
    ]

    for expression in expressions:
        CalcBasic.setExpr(expression)
        print(f'{expression} = {CalcBasic.calculate}')

    # Testing Advanced Calculator
    CalcAdvanced = AdvancedCalculator()

    # Advanced calculator takes expressions of the form a = n; b = n1 (operator) a (operator) etc...; etc...; return (expression)
    advancedExpressions = [
        'a = 5;b = 7 + a;a = 7;c = a + b;c = a * 0;return c',
        'A = 1;B = A + 9;C = A + B;A = 20;D = A + B + C;return D - A'
    ]

    for expression in advancedExpressions:
        CalcAdvanced.setExpression(expression)
        print(CalcAdvanced.calculateExpressions())
        print(CalcAdvanced.states)


if __name__ == "__main__":
    run_tests()
