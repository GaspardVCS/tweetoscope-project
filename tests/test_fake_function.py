def addition(a, b):
    return a + b

def test_addition():
    assert addition(1, 1) == 2
    assert addition(1, -1) == 0

if __name__ == "__main__":
    test_addition()