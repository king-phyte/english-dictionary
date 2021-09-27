from dataclasses import dataclass, field
from typing import Union, List, NoReturn, Type, Any, Sequence, Optional

from utils.helpers import binary_search


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
        return (
            f"<b>{self.relationship_type.capitalize()}</b>: {', '.join(self.words)}"
            if self.words
            else ""
        )

    def __getitem__(self, item):
        return getattr(item)


@dataclass
class Pronunciation:
    text: Sequence[str] = field(default_factory=list)
    audio: Optional[Sequence[str]] = None

    def to_html(self) -> str:
        return self.text

    def __getitem__(self, item):
        return getattr(item)


@dataclass
class Definition:
    definition: Optional[str] = None
    example: Optional[str] = None
    related_words: Sequence[RelatedWord] = field(default_factory=list)

    def to_html(self):
        html_version = []

        if self.definition:
            html_version.append(self.definition)

        if self.example:
            html_version.append(f"<b>Example:</b> {self.example}")

        for related_word in self.related_words:
            if related_word.words:
                html_version.append(related_word.to_html())

        return "\n\n".join(html_version)

    def __getitem__(self, item):
        return getattr(item)


@dataclass
class Meaning:
    part_of_speech: Optional[str] = None
    definitions: list[Definition] = field(default_factory=list)

    def to_html(self):
        pos = f"<b>Part of speech:</b> {self.part_of_speech}\n\n"
        definitions = "\n".join(
            (definition.to_html()) for definition in self.definitions
        )
        return pos + definitions

    def __getitem__(self, item):
        return getattr(item)


class WordData:
    def __init__(
        self,
        name: str,
        etymology: Optional[str] = None,
        meanings: Optional[Sequence[Meaning]] = None,
        pronunciations: Optional[Sequence[Pronunciation]] = None,
        *args,
        **kwargs,
    ):
        self._name = name.lower()
        self.etymology = etymology if etymology else ""
        self.pronunciations = pronunciations
        self.meanings = meanings

    def get_name(self) -> str:
        return self._name

    @staticmethod
    def from_api(api: list[dict]):
        word = api[0]
        return WordData(
            name=word.get("name"),
            etymology=word.get("etymology"),
            pronunciations=[
                Pronunciation(**pronunciation)
                for pronunciation in word.get("pronunciations")
            ]
            if word.get("pronunciations")
            else [],
            meanings=[
                Meaning(
                    part_of_speech=meaning.get("part_of_speech"),
                    definitions=[
                        Definition(
                            definition=definition.get("definition"),
                            example=definition.get("example"),
                            related_words=[
                                RelatedWord(**related_word)
                                for related_word in definition.get("related_words")
                            ],
                        )
                        for definition in meaning.get("definitions")
                    ],
                )
                for meaning in word.get("meanings")
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
