import pytest
from utils.functions import binary_search


@pytest.mark.parametrize(
    "test_input, result",
    [
        (([1, 2, 3, 4, 5], 3), 2),
        (([0, 3, 18, 902], 902), 3),
        (([3, 5, 6, 9, 10, 99], 0), -1),
        (([0, 5, 7, 10, 15], 0), 0),
        ((["a", "b", "c", "d", "e", "f"], "e"), 4),
        ((["a", "b", "c", "d", "e", "f"], "z"), -1),
        (([], 2), -1),
    ],
)
def test_binary_search(test_input, result):
    sequence, target = test_input
    assert binary_search(sequence, target) == result
