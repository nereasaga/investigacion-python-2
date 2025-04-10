from src.main import suma, is_greater_than

def test_suma():
    assert suma(2,5) == 7 

def test_is_greater_than():
    assert is_greater_than(10, 5) is True