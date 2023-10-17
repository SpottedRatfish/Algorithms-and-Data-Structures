from lista_4_zadanie_4_Michał_Tokarski import BinaryTree, Empty




def valid_node(x):
    if not type(x) in [float, int, str]:
        raise Empty(f'Incorrect value within a tree')
    return

def number_check(x):
    valid_node(x)
    if type(x) == str:
        return False
    else:
        return True

def diff(Tree, variable):
    """Funkcja bazuje na rekurencji. Obsługuje mnożenie, dodawanie, odejmowanie i dzielenie. Potęgi zapisać w formie mnożenia, to jest x^2=x*x"""
    derr = BinaryTree()

    if number_check(Tree[0]):
        if not Tree.is_leaf(0):
            raise Empty("Incorrect expression")
        derr.set_root(0)

    elif Tree[0] == variable:
        if not Tree.is_leaf(0):
            raise Empty("Incorrect expression")
        derr.set_root(1)

    elif not Tree[0] in ['+', '-', '*', '/']:
        if not Tree.is_leaf(0):
            raise Empty("Incorrect expression")
        derr.set_root(0)

    elif Tree[0] == '+':
        if len(Tree._children(0)) != 2:
            raise Empty("Incorrect expression")
        derr.set_root('+')
        derr.merge(diff(Tree.segment(1), variable), 1)
        derr.merge(diff(Tree.segment(2), variable), 2)

    elif Tree[0] == '-':
        if len(Tree._children(0)) != 2:
            raise Empty("Incorrect expression")
        derr.set_root('-')
        derr.merge(diff(Tree.segment(1), variable), 1)
        derr.merge(diff(Tree.segment(2), variable), 2)

    elif Tree[0] == '*':
        if len(Tree._children(0)) != 2:
            raise Empty("Incorrect expression")
        derr.set_root('+')
        derr.set_left('*', 0)
        derr.set_right('*', 0)

        derr.merge(Tree.segment(1), 3)
        derr.merge(diff(Tree.segment(2), variable), 4)

        derr.merge(Tree.segment(2), 5)
        derr.merge(diff(Tree.segment(1), variable), 6)

    elif Tree[0] == '/':
        if len(Tree._children(0)) != 2:
            raise Empty("Incorrect expression")
        if Tree[2] == 0:
            raise ZeroDivisionError
        derr.set_root('/')
        derr.set_left('-', 0)
        derr.set_right('*', 0)

        derr.set_left('*', 1)
        derr.set_right('*', 1)
        derr.merge(Tree.segment(2), 5)
        derr.merge(Tree.segment(2), 6)

        derr.merge(Tree.segment(2), 7)
        derr.merge(diff(Tree.segment(1), variable), 8)
        derr.merge(Tree.segment(1), 9)
        derr.merge(diff(Tree.segment(2), variable), 10)


    return derr

def to_expression(Tree):
    result = ''

    if number_check(Tree[0]):
        result = str(Tree[0])
        if Tree[0] < 0:
            result = '(' + result + ')'

    elif not Tree[0] in ['+', '-', '*', '/']:
        result = Tree[0]

    elif Tree[0] in ['+', '-', '*', '/']:
        if type(Tree[1]) in [int, float] and type(Tree[2]) in[int, float]:
            expr = f'{Tree[1]}{Tree[0]}{Tree[2]}'
            result = str(eval(expr))
            if eval(expr) < 0:
                result = '(' + result + ')'

        elif Tree[1] == 0:
            expr = f'{Tree[1]}{Tree[0]}5'
            result = str(eval(expr))
            result = result.replace('5', Tree[2])
            if eval(expr) < 0:
                result = '(' + result + ')'

        elif Tree[2] == 0:
            expr = f'5{Tree[0]}{Tree[2]}'
            result = str(eval(expr))
            result = result.replace('5', Tree[1])
            if eval(expr) < 0:
                result = '(' + result + ')'

        else:
            result = f'({to_expression(Tree.segment(1))}{Tree[0]}{to_expression(Tree.segment(2))})'


    return result

def differentiate(Tree, variable):
    A = diff(Tree, variable)
    return to_expression(A)

if __name__ == '__main__':
    test = BinaryTree('/')
    test.set_left('+', 0)
    test.set_right('y', 0)
    test.set('x', 3)
    test.set('x', 4)
    print('d/dx',to_expression(test)), '='
    print(differentiate(test, 'x'), '\n')

    print('d/dy', to_expression(test), '=')
    print(differentiate(test, 'y'), '\n')


