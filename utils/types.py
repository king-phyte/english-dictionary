from typing import Union, List, NoReturn, Type, Any, Sequence, Optional, Dict
from utils.formatter import FormatWord


class OrderedList:
    def __init__(
        self, allow_duplicates: bool = False, instance: Type[Any] = int
    ) -> None:
        self._allow_duplicates = allow_duplicates
        self._instance = instance
        self._list = []

    def append(self, item) -> None:
        if not isinstance(item, self._instance):
            raise ValueError

        if (not self._allow_duplicates) and (item in self):
            return

        if len(self) < 1:
            return self._list.append(item)

        for i in range(len(self)):
            if item > self._list[i]:
                continue
            else:
                return self._list.insert(i, item)

        return self._list.append(item)

    def find(self, target):
        if len(self) < 1:
            return -1

        lower_bound = 0
        upper_bound = len(self._list) - 1

        while lower_bound <= upper_bound:
            mid_point = (lower_bound + upper_bound) // 2

            if self._list[mid_point] == target:
                return mid_point

            elif self._list[mid_point] > target:
                upper_bound = mid_point - 1

            elif self._list[mid_point] < target:
                lower_bound = mid_point + 1

        return -1

    def index(self, item) -> Union[int, List[int], NoReturn]:
        """
        Returns the index of item.
        Raises ValueError if the value is not present.
        """
        if item not in self:
            raise ValueError

        if not self._allow_duplicates:
            return self._list.index(item)

        indexes = []

        start = 0
        for i in range(self._list.count(item)):
            current_index = self._list.index(item, start)
            indexes.append(current_index)
            start = current_index + 1

        return indexes

    def append_multiple(self, iterable) -> None:
        for item in iterable:
            self.append(item)

    def peek(self) -> list:
        return self._list

    def pop(self, index=-1) -> Union[int, NoReturn]:
        """Remove and return item at index (default last).
        Raises IndexError if list is empty or index is out of range."""
        if len(self) <= 0:
            raise IndexError("List index out of range")

        return self._list.pop(index)

    def clear(self) -> None:
        """Removes all elements in the list"""
        self._list = []

    def __str__(self) -> str:
        return f"{self._list}"

    def __repr__(self) -> str:
        return self.__str__()

    def __len__(self) -> int:
        return len(self._list)

    def __contains__(self, item) -> bool:
        return item in self._list


#
# class OrderedDict(OrderedList):
#     def __init__(self) -> None:
#         super().__init__(allow_duplicates=False, instance=str)


class RelatedWord:
    def __init__(
        self,
        relationship_type: str,
        words: Sequence[str],
        *args,
        **kwargs,
    ):
        self.relationship_type = relationship_type if relationship_type else ""
        self.words = words if words else []

    def to_html(self):
        return f"{self.relationship_type.capitalize()}: {', '.join(self.words)}"

    def __getitem__(self, item):
        return getattr(item)


class Pronunciation:
    def __init__(
        self,
        text: List[str] = None,
        audio: List[str] = None,
        *args,
        **kwargs,
    ) -> None:
        self.text = text if text is not None else []
        self.audio = audio if audio is not None else []

    def to_html(self) -> str:
        return FormatWord.convert_to_list(self.text)

    def __getitem__(self, item):
        return getattr(item)


class Definition:
    def __init__(
        self,
        part_of_speech: Optional[str] = None,
        texts: Optional[Sequence[str]] = None,
        related_words: Optional[Sequence[RelatedWord]] = None,
        example_uses: Optional[Sequence[str]] = None,
        *args,
        **kwargs,
    ) -> None:
        self.part_of_speech = part_of_speech
        self.texts = texts
        self.related_words = related_words
        self.example_uses = example_uses

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

    def get_name(self) -> str:
        return self._name

    @staticmethod
    def from_dict(word_data: dict):
        name = word_data.get("name")
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
        #
        # test = WordData(name=word_data.get("name"))
        # word_data: Union[Optional[Sequence[Sequence[Dict[str, Any]]]]] = (
        #     word_data.get("data"),
        # )
        # if word_data is not None:
        #     definitions_list = []
        #     for group in word_data:
        #         for section in group:
        #             test.etymology = group[0].get("etymology")
        #             # pronunciations=[
        #             #     Pronunciation(
        #             #         text=[
        #             #             "IPA: /t\u025bst/",
        #             #             "Rhymes: -\u025bst",
        #             #             "(South African) IPA: /test/",
        #             #         ]
        #             #     ),
        #             # ],
        #             if section.get("definitions"):
        #                 definitions = []
        #                 for definition in section.get("definitions"):
        #                     _definition = Definition()
        #                     _definition.part_of_speech = definition.get(
        #                         "part_of_speech"
        #                     )
        #
        #                     if definition.get("related_words"):
        #                         related_words = []
        #                         for related_word in definition.get("related_words"):
        #                             _related_word = RelatedWord(
        #                                 relationship_type=related_word.get(
        #                                     "relationship_type"
        #                                 ),
        #                                 words=related_word.get("words"),
        #                             )
        #                             related_words.append(_related_word)
        #                         _definition.related_words = definition.related_words
        #                     _definition.texts = definition.get("texts")
        #                     _definition.example_uses = definition.get("example_uses")
        #
        #                     definitions.append(Definition)
        #                 test.definition_list = definitions
        #
        #         #     definitions=[
        #         #         Definition(
        #         #             part_of_speech="noun",
        #         #             texts=(
        #         #                 "test (plural tests)",
        #         #                 "A challenge, trial.",
        #         #                 "A cupel or cupelling hearth in which precious metals are melted for trial and refinement.",
        #         #                 "(academia) An examination, given often during the academic term.",
        #         #                 "A session in which a product or piece of equipment is examined under everyday or extreme conditions to evaluate its durability, etc.",
        #         #                 "(cricket, normally \u201cTest\u201d) A Test match.",
        #         #                 "(marine biology) The external calciferous shell, or endoskeleton, of an echinoderm, e.g. sand dollars and sea urchins.",
        #         #                 "(botany) Testa; seed coat.",
        #         #                 "(obsolete) Judgment; distinction; discrimination.",
        #         #             ),
        #         #             related_words=(
        #         #                 RelatedWord(
        #         #                     relationship_type="synonyms",
        #         #                     words=[
        #         #                         "(challenge, trial): See Thesaurus:test",
        #         #                         "(academics: examination): examination, quiz",
        #         #                     ],
        #         #                 ),
        #         #                 RelatedWord(
        #         #                     relationship_type="antonyms",
        #         #                     words=[
        #         #                         "(academics: examination): recess",
        #         #                     ],
        #         #                 ),
        #         #             ),
        #         #             example_uses=[
        #         #                 "Numerous experimental tests and other observations have been offered in favor of animal mind reading,"
        #         #                 "and although many scientists are skeptical, others assert that humans are not the only species capable"
        #         #                 "of representing what others do and don\u2019t perceive and know.",
        #         #                 "Who would excel, when few can make a test / Betwixt indifferent writing and the best?",
        #         #             ],
        #         #         ),
        #         #         Definition(
        #         #             part_of_speech="verb",
        #         #             texts=(
        #         #                 "test (third-person singular simple present tests, present participle testing, simple past and past participle tested)",
        #         #                 "To challenge.",
        #         #                 "To refine (gold, silver, etc.) in a test or cupel; to subject to cupellation.",
        #         #                 "To put to the proof; to prove the truth, genuineness, or quality of by experiment, or by some principle or standard; to try.",
        #         #                 "(academics) To administer or assign an examination, often given during the academic term, to (somebody).",
        #         #                 "To place a product or piece of equipment under everyday and/or extreme conditions and examine it for its durability, etc.",
        #         #                 "(copulative) To be shown to be by test.",
        #         #                 "(chemistry) To examine or try, as by the use of some reagent.",
        #         #             ),
        #         #             example_uses=[
        #         #                 "Climbing the mountain tested our stamina.",
        #         #                 "to test the soundness of a principle; to test the validity of an argument",
        #         #                 "Experience is the surest standard by which to test the real tendency of the existing constitution.",
        #         #                 "Similar studies of rats have employed four different intracranial resorbable, slow sustained release systems\u2014\u00a0[\u2026]. Such a slow-release device containing angiogenic factors could be placed on the pia mater covering the cerebral cortex and tested in persons with senile dementia in long term studies.",
        #         #                 "He tested positive for cancer.",
        #         #                 "It is probable that children who test above 180 IQ are actually present in our juvenile population in greater frequency than at the rate of one in a million.",
        #         #                 "to test a solution by litmus paper",
        #         #             ],
        #         #             related_words=(
        #         #                 RelatedWord(
        #         #                     relationship_type="related term",
        #         #                     words=["attest", "contest", "detest", "protest"],
        #         #                 ),
        #         #             ),
        #         #         ),
        #         #     ],
        #         # )
        #
        # # return test

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

    def remove_word(self, word: WordData):
        self._list.remove(word)

    def edit_word(self, old: WordData, new: WordData):
        self.remove_word(old)
        self.append(new)

    def find_word(self, word: WordData):
        return self.find(word)

    def get_word_details(self, word: str):
        return self._list[self.peek().index(word)]
