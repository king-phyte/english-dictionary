from dataclasses import dataclass, field
from typing import Union, List, NoReturn, Type, Any, Sequence, Optional

from english_dictionary.utils.formatter import FormatWord
from english_dictionary.utils.helpers import binary_search


class OrderedList:
    def __init__(
        self, allow_duplicates: bool = False, instance: Type[Any] = int
    ) -> None:
        self._allow_duplicates = allow_duplicates
        self._instance = instance
        self._list = []

    @staticmethod
    def bisect_left(
        sorted_collection: list, item: int, lower_bound: int = 0, upper_bound: int = -1
    ) -> int:
        if upper_bound < 0:
            upper_bound = len(sorted_collection)

        while lower_bound < upper_bound:
            mid = (lower_bound + upper_bound) // 2
            if sorted_collection[mid] < item:
                lower_bound = mid + 1
            else:
                upper_bound = mid

        return lower_bound

    def insort_left(self, item) -> None:
        self._list.insert(self.bisect_left(self._list, item), item)

    def append(self, item) -> None:
        if not isinstance(item, self._instance):
            raise ValueError

        if (not self._allow_duplicates) and (item in self):
            return

        if len(self) < 1:
            self._list.append(item)
            return

        self.insort_left(item)

    def find(self, target):
        return binary_search(self._list, target)

    def index(self, item) -> Union[int, List[int], NoReturn]:
        """
        Returns the index of item.
        Raises ValueError if the value is not present.
        """
        if item not in self:
            raise ValueError

        if not self._allow_duplicates:
            return self.find(item)

        first_item_index = self._list.index(item)

        return list(range(first_item_index, first_item_index + self._list.count(item)))

    def append_multiple(self, iterable) -> None:
        for item in iterable:
            self.append(item)

    def peek(self) -> list:
        return self._list

    def pop(self, index=-1) -> Union[int, NoReturn]:
        """Remove and return item at index (default last).
        Raises IndexError if list is empty or index is out of range."""

        return self._list.pop(index)

    def remove(self, item):
        self.pop(self.index(item))

    def clear(self) -> None:
        """Removes all elements in the list"""
        self._list = []

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"{self._list}"

    def __len__(self) -> int:
        return len(self._list)

    def __contains__(self, item) -> bool:
        return binary_search(self._list, item) != -1


@dataclass
class RelatedWord:
    relationship_type: str
    words: Sequence[str] = field(default_factory=list)

    def to_html(self):
        return f"{self.relationship_type.capitalize()}: {', '.join(self.words)}"

    def __getitem__(self, item):
        return getattr(item)


@dataclass
class Pronunciation:
    text: Sequence[str] = field(default_factory=list)
    audio: Optional[Sequence[str]] = None

    def to_html(self) -> str:
        return FormatWord.convert_to_list(self.text)

    def __getitem__(self, item):
        return getattr(item)


@dataclass
class Definition:
    part_of_speech: Optional[str] = None
    texts: Optional[Sequence[str]] = None
    related_words: Optional[Sequence[RelatedWord]] = None
    example_uses: Optional[Sequence[str]] = None

    def to_html(self):
        section = (
            f"<b>Part of speech:</b> {self.part_of_speech}<br />"
            + f"{FormatWord.convert_to_list(self.texts)}"
        )
        if self.example_uses:
            section += f"<p><b>Examples:</b></p> <p>{FormatWord.convert_to_list(self.example_uses)}</p>"

        if self.related_words:
            section += f"<p><b>Related Words:</b></p> <p>{FormatWord.convert_to_list(FormatWord.parse_related_words(self))}</p>"

        return section

    def __getitem__(self, item):
        return getattr(item)


class RW:
    ...


class Def:
    def __init__(self, definition: str, example: str, related_words: RW):
        ...

    def __getitem__(self, item):
        return getattr(item)


class Meaning:
    def __init__(self, part_of_speech: Optional[str], definitions: list[Def]):
        ...

    def __getitem__(self, item):
        return getattr(item)


class WordData:
    def __init__(
        self,
        name: str,
        etymology: Optional[str] = None,
        definitions: Optional[Sequence[Definition]] = None,
        pronunciations: Optional[Sequence[Pronunciation]] = None,
        *args,
        **kwargs,
    ):
        self._name = name.lower()
        self.etymology = etymology if etymology else ""
        self.definition_list = definitions
        self.pronunciations = pronunciations
        self.meanings: Optional[Sequence[Meaning]] = kwargs.get("meanings")

    def get_name(self) -> str:
        return self._name

    @staticmethod
    def from_api(api: list[dict]):
        return WordData(**api[0])

    @staticmethod
    def from_dict(word_data: dict):
        name = word_data.get("name")
        if not word_data.get("data"):
            return WordData(name)
        word_data = word_data.get("data")[0]
        definition = word_data["definitions"][0]
        related_words = (
            definition["related_words"][0] if definition["related_words"] else None
        )
        return WordData(
            name=name,
            etymology=word_data.get("etymology"),
            definitions=[
                Definition(
                    part_of_speech=definition.get("part_of_speech"),
                    texts=definition.get("texts"),
                    related_words=None
                    if not related_words
                    else [
                        RelatedWord(
                            relationship_type=related_words.get("relationship_type"),
                            words=related_words.get("words"),
                        ),
                    ],
                    example_uses=definition.get("example_uses"),
                )
            ],
        )

    def __getitem__(self, item):
        return getattr(item)

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return self._name

    def __len__(self) -> int:
        return len(self._name)

    def __le__(self, other) -> bool:
        return self._name < other.get_name()

    def __gt__(self, other) -> bool:
        return self._name > other.get_name()

    def __eq__(self, other):
        return self._name == other.get_name()


class Dictionary(OrderedList):
    def __init__(self, *args, **kwargs):
        super().__init__(allow_duplicates=False, instance=WordData)

    def peek(self) -> list:
        return list(map(str, self._list))

    def edit_word(self, old: WordData, new: WordData):
        self.remove(old)
        self.append(new)

    def get_word_details(self, word: str):
        return self._list[binary_search(self.peek(), word)]
