import pytest

from english_dictionary.core import Dictionary, WordData, Definition, RelatedWord


@pytest.fixture
def word():
    definition1 = Definition(
        definition="Something something",
        example="Huh?",
        related_words=[
            RelatedWord(
                relationship_type="noun",
                words=["idk", "idc"],
            ),
        ],
    )
    word = WordData(
        name="hi",
        etymology="From nowhere",
        definitions=[
            definition1,
        ],
    )
    return word


def test_dictionary_is_sorted(word):
    dictionary = Dictionary()

    with pytest.raises(IndexError):
        dictionary.pop()
        raise IndexError

    assert dictionary.append(word) is None

    assert dictionary.peek() == ["hi"]
    dictionary.append(word)
    assert dictionary.peek() == ["hi"]
    dictionary.append(WordData("king"))
    dictionary.append(WordData("ape"))
    dictionary.append(WordData("zab"))
    dictionary.append(WordData("ghana"))
    assert dictionary.peek() == sorted(["hi", "king", "ape", "zab", "ghana"])


def test_dictionary():
    dictionary = Dictionary()

    dictionary.append(WordData("king"))
    dictionary.append(WordData("ape"))
    dictionary.append(WordData("zab"))
    dictionary.append(WordData("ghana"))

    dictionary.remove(WordData("king"))
    assert dictionary.peek() == sorted(["ape", "zab", "ghana"])
