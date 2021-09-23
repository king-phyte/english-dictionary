from typing import List, Iterable

from english_dictionary.types import WordData, Definition


class BaseAPIFormatter:
    def __init__(self, word: WordData) -> None:
        self._word_data = word

    def parse_etymology(self) -> str:
        return f"<b>Etymology:</b> {self._word_data.etymology.strip()}"

    def parse_pronunciations(self) -> str:
        for pronunciation in self._word_data.pronunciations:
            return f"<p><b>Pronunciations:</b></p> <p>{pronunciation.to_html()}</p>"

    def parse_meanings(self) -> List[str]:
        meanings = []

        for meaning in self._word_data.meanings:
            meanings.append(meaning.to_html())

        return meanings

    def to_html(self):
        html_version = []

        if self._word_data.etymology:
            html_version.append(self.parse_etymology())

        if self._word_data.pronunciations:
            html_version.append(self.parse_pronunciations())

        return "<hr />".join(
            "<pre style='font-family: initial; font-size: initial'>"
            + section
            + "</pre>"
            for section in html_version
        )


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
