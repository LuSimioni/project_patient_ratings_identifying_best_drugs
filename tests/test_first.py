from src.app import hello_world


def test_print_hi():
    output = hello_world()
    check = 'Hello, cambada!'
    assert output == check 