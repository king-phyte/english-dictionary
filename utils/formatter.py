import json
from wiktionaryparser.utils import WordData, Definition, RelatedWord, Pronunciation
from typing import List, Optional, Iterable


class FormatWord:
    def __init__(self, word: WordData) -> None:
        self.word_data = word

    @staticmethod
    def convert_to_list(iterable: Iterable[str], start=1):
        """
        Returns numbered strings starting from :start
        Example:
            iterable: ("hello", "world", "!")
            start: 1

            Returns:
                1. hello
                2. world
                3. !
        """

        return "\n".join(
            map(
                lambda x: f"\t{x[0]}. {x[1]}",
                enumerate(iterable, start=start),
            )
        )

    @staticmethod
    def parse_etymology(word_data: WordData) -> str:
        return f"<b>Etymology:</b> {word_data.etymology.strip()}"

    @staticmethod
    def parse_pronunciations(word_data: WordData) -> str:
        for pronunciation in word_data.pronunciations:
            return f"<p><b>Pronunciations:</b></p> <p>{pronunciation.to_html()}</p>"

    @staticmethod
    def parse_related_words(definition: Definition) -> List[str]:
        related_words = []

        for related_word in definition.related_words:
            related_words.append(related_word.to_html())

        return related_words

    @staticmethod
    def parse_definitions(word_data: WordData) -> List[str]:
        definitions = []

        for definition in word_data.definition_list:
            definitions.append(definition.to_html())

        return definitions

    @staticmethod
    def to_html(word_data: WordData):
        html_version = []

        if word_data.etymology:
            html_version.append(FormatWord.parse_etymology(word_data))

        if word_data.pronunciations:
            html_version.append(FormatWord.parse_pronunciations(word_data))

        if word_data.definition_list:
            html_version.extend(FormatWord.parse_definitions(word_data))

        return "<hr />".join(
            "<pre style='font-family: initial; font-size: initial'>"
            + section
            + "</pre>"
            for section in html_version
        )


# class HumanReadableFormat:
#     def __init__(self, data: Optional[List[dict]]) -> None:
#         self._raw_data = data
#         self._string = []
#
#     @staticmethod
#     def parse_etymology(group: WordData) -> str:
#         if group.etymology is not None:
#             return f"Etymology: {group.etymology.strip()}"
#
#         return ""
#
#     @staticmethod
#     def parse_pronunciation(group: WordData) -> str:
#         if group.pronunciations:
#             group_string = ["Pronunciations"]
#             pronunciation = Pronunciation(**group.pronunciations)
#             group_string.extend(
#                 map(
#                     lambda x: f"\t{x}",
#                     pronunciation.text,
#                 )
#             )
#             return "\n".join(group_string)
#
#         return ""
#
#     @staticmethod
#     def parse_definitions(group: WordData) -> str:
#         if group.definition_list and isinstance(group.definition_list, list):
#             group_string = ["Definitions:"]
#
#             for section in group.definition_list:
#                 definition = Definition(**section)
#
#                 if definition.part_of_speech:
#                     group_string.append(
#                         "\n\tPart of speech: " + definition.part_of_speech
#                     )
#
#                     group_string.extend(
#                         map(
#                             lambda x: f"\t{x[0]}. {x[1]}",
#                             enumerate(definition.text, start=1),
#                         )
#                     )
#
#                 if definition.related_words:
#                     for sec in definition.related_words:
#                         related_words = RelatedWord(**sec)
#
#                         group_string.append(f"\n\t{related_words.relationship_type}")
#
#                         group_string.extend(
#                             map(
#                                 lambda x: f"\t{x[0]}. {x[1]}",
#                                 enumerate(related_words.words, start=1),
#                             )
#                         )
#
#                 if definition.example_uses:
#                     group_string.append(f"\n\tExamples:")
#
#                     group_string.extend(
#                         map(
#                             lambda x: f"\t{x[0]}. {x[1]}",
#                             enumerate(definition.example_uses, start=1),
#                         )
#                     )
#
#             return "\n".join(group_string)
#
#     def display(self) -> None:
#         print(self.get_formatted_form())
#
#     def get_formatted_form(self) -> str:
#         for group in self._raw_data:
#             group = WordData(**group)
#             self._string.append(self.parse_etymology(group))
#             self._string.append(self.parse_pronunciation(group))
#             self._string.append(self.parse_definitions(group))
#
#         return "\n\n".join(self._string)


if __name__ == "__main__":
    with open("../data.json") as f:
        data = json.load(f)

    formatter = HumanReadableFormat(data)
    formatter.display()
