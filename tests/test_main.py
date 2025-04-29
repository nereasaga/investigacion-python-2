import pytest
from src.main import suma, is_greater_than

@pytest.mark.basico
def test_suma():
    resultado = suma(2, 5)
    print("El resultado de suma(2, 5) es:", resultado)
    assert resultado == 7 

@pytest.mark.basico
def test_is_greater_than():
    print("Comparando si 10 es mayor que 5")
    assert is_greater_than(10, 5) is True

@pytest.mark.avanzado
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
    print(f"Probando suma({input_x}, {input_y})")
    assert suma(input_x, input_y) == expected
