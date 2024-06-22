from src.app.func import print_hi


def test_print_hi():
    output = print_hi()
    check = 'Hi'
    assert output == check 