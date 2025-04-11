import pytest
from src.main import suma, is_greater_than

def test_suma():
    assert suma(2,5) == 7 

def test_is_greater_than():
    assert is_greater_than(10, 5) is True

#ejemplo decorador

@pytest.mark.parametrize(
        "input_x,input_y,expected",
        [
            (5,1,6),
            (6,suma(4,2),12),
            (suma(19,1),15,35),
            (-7,10,suma(-7,10)),

        ]
)

def test_suma_params(input_x,input_y,expected):
    assert suma (input_x,input_y) == expected

