import pytest

from utils.types import OrderedList, OrderedDict, WordData


def test_ordered_list_no_duplicates():
    no_duplicates = OrderedList(allow_duplicates=False)

    assert no_duplicates.peek() == []

    with pytest.raises(IndexError):
        no_duplicates.pop()
        raise IndexError("List index out of range")

    with pytest.raises(ValueError):
        no_duplicates.index(3)
        raise ValueError

    assert no_duplicates.append(4) is None
    no_duplicates.append(3)
    no_duplicates.append(5)
    assert 5 in no_duplicates
    assert 0 not in no_duplicates
    no_duplicates.append(1)
    assert no_duplicates.peek() == sorted([4, 3, 5, 1])
    no_duplicates.append(5)
    assert no_duplicates.index(5) == 3
    assert no_duplicates.append_multiple(i for i in range(10)) is None
    assert no_duplicates.peek() == list(i for i in range(10))
    assert no_duplicates.index(5) == 5
    assert no_duplicates.pop(3) == 3
    assert no_duplicates.clear() is None
    assert no_duplicates.peek() == []


def test_ordered_list_duplicates():
    duplicates = OrderedList(allow_duplicates=True)

    assert duplicates.peek() == []

    with pytest.raises(IndexError):
        duplicates.pop()
        raise IndexError("List index out of range")

    with pytest.raises(ValueError):
        duplicates.index(3)
        raise ValueError

    assert duplicates.append(3) is None
    duplicates.append(4)
    duplicates.append(5)
    duplicates.append(1)
    assert duplicates.peek() == sorted([3, 4, 5, 1])
    duplicates.append(5)
    assert duplicates.index(5) == [3, 4]
    assert duplicates.append_multiple(i for i in range(10)) is None
    assert 5 in duplicates
    assert len(duplicates.peek()) == len([0, 1, 1, 2, 3, 3, 4, 4, 5, 5, 5, 6, 7, 8, 9])
    assert duplicates.peek() == [0, 1, 1, 2, 3, 3, 4, 4, 5, 5, 5, 6, 7, 8, 9]
    assert duplicates.index(5) == [8, 9, 10]
    assert duplicates.pop() == 9
    assert duplicates.pop(8) == 5
    assert duplicates.clear() is None
    assert duplicates.peek() == []


def test_ordered_dict():
    dictionary = OrderedDict()

    assert dictionary.peek() == []

    with pytest.raises(IndexError):
        dictionary.pop()
        raise IndexError("List index out of range")

    assert dictionary.append("king") is None
    assert dictionary.append_multiple(["hey", "huh?", "a", "zab"]) is None
    assert len(dictionary) == len(["king", "hey", "huh?", "a", "zab"])
    assert dictionary.peek() == sorted(["king", "hey", "huh?", "a", "zab"])
    assert dictionary.pop() == "zab"

    with pytest.raises(ValueError):
        dictionary.index(3)
        raise ValueError

    assert "king" in dictionary
    assert "pop" not in dictionary

    assert dictionary.find("zab") == -1
    assert dictionary.find("hey") == 1


def test_word_data():
    word = WordData("hi")

    assert str(word) == "hi"
