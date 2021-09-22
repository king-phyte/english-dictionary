import pytest

from english_dictionary.types import Dictionary, WordData, Definition


class TestDictionary:
    @pytest.fixture
    def word(self):
        definition1 = Definition(
            part_of_speech="noun",
            texts=[
                "Nothing here",
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

    def test_dictionary_is_sorted(self, word):
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

    def test_dictionary(self):
        dictionary = Dictionary()

        dictionary.append(WordData("king"))
        dictionary.append(WordData("ape"))
        dictionary.append(WordData("zab"))
        dictionary.append(WordData("ghana"))

        dictionary.remove(WordData("king"))
        assert dictionary.peek() == sorted(["ape", "zab", "ghana"])
