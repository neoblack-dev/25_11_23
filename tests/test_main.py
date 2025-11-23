import pytest
import math
from source.main import circle_per, circle_area

@pytest.fixture()
def before_results():
    print('\nдо теста')
    yield
    print('\nпосле теста')


def test_circle_per():
    assert circle_per(5) == 2 * math.pi * 5

def test_circle_area(before_results):
    assert circle_area(5) == math.pi * 5 * 5

def test_circle_per_zero():
    assert circle_per(0) == 0

def test_circle_area_zero():
    assert circle_area(0) == 0
