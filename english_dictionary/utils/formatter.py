from english_dictionary.core import WordData


class BaseAPIFormatter:
    def __init__(self, word: WordData) -> None:
        self._word_data = word

    def parse_etymology(self) -> str:
        return f"<b>Etymology:</b> {self._word_data.etymology.strip()}"

    def parse_pronunciations(self) -> str:
        for pronunciation in self._word_data.pronunciations:
            return f"<p>{pronunciation.to_html()}</p>"

    def parse_meanings(self) -> str:
        meanings = []

        for meaning in self._word_data.meanings:
            meanings.append(meaning.to_html())

        return "\n<hr />\n".join(meanings)

    def to_html(self):
        html_version = []

        if self._word_data.etymology:
            html_version.append(self.parse_etymology())

        if self._word_data.pronunciations:
            html_version.append(self.parse_pronunciations())

        if self._word_data.meanings:
            html_version.append(self.parse_meanings())

        return "\n<hr />\n".join(
            "<pre style='font-family: inherit;'>" + section + "</pre>"
            for section in html_version
        )
