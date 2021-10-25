from pathlib import Path
from typing import Sequence, Optional, Dict, Union

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication, QIcon
from PyQt5.QtWidgets import QMainWindow, QDialog, QMessageBox, QGroupBox

from .add_word_dialog import Ui_AddWordDialog as UiAddWordDialog
from .definition_groupbox import Ui_DefinitionGroupBox as UiDefinitionGroupBox
from .mainwindow import Ui_MainWindow as UiMainWindow
from .meanings_groupbox import Ui_MeaningsGroupBox as UiMeaningsGroupBox
from .pronunciation_groupbox import Ui_Pronunciation as UiPronunciationGroupBox
from .related_words_groupbox import Ui_RelatedWordsGroupBox as UiRelatedWordsGroupBox
from ..api import BaseAPI
from ..core import Dictionary, WordData, RelatedWord, Definition, Pronunciation, Meaning
from ..database import DATABASE_DIRECTORY, DATABASE_NAME, Database

SVGS_DIR = Path(__file__).resolve().parent / "svgs"
PLUS_SVG_PATH = SVGS_DIR / "plus.svg"
SEARCH_SVG_PATH = SVGS_DIR / "search.svg"
EDIT_SVG_PATH = SVGS_DIR / "edit.svg"
DELETE_SVG_PATH = SVGS_DIR / "trash-alt.svg"

plus_icon = QIcon(str(PLUS_SVG_PATH))


class RelatedWordsGroupBox(QGroupBox, UiRelatedWordsGroupBox):
    def __init__(
        self,
        related_word: Optional[RelatedWord] = None,
        *args,
        **kwargs,
    ) -> None:
        super(RelatedWordsGroupBox, self).__init__(*args, **kwargs)
        self._related_word = related_word
        self.setupUi(self)

    def set_fields_text(self):
        if self._related_word is not None:
            self.relationship_type_lineedit.setText(
                relationship_type
                if (relationship_type := self._related_word.relationship_type)
                else ""
            )

            self.related_words_lineedit.setText(
                ", ".join(words) if (words := self._related_word.words) else ""
            )

        return self

    def get_fields_content(self) -> Dict[str, Union[list, str]]:
        return {
            "relationship_type": self.relationship_type_lineedit.text().strip(),  # Required
            "words": (
                words.split(", ")
                if (words := self.related_words_lineedit.text().strip())
                else []
            ),
        }


class DefinitionGroupBox(QGroupBox, UiDefinitionGroupBox):
    def __init__(
        self,
        definition: Optional[Definition] = None,
        *args,
        **kwargs,
    ) -> None:
        super(DefinitionGroupBox, self).__init__(*args, **kwargs)
        self._definition = definition
        self._next_related_words_widget_index = 0
        self.setupUi(self)
        self.add_related_words_button.setIcon(plus_icon)
        self.install_slots()
        self.add_related_words_field()

    def install_slots(self) -> None:
        self.add_related_words_button.clicked.connect(self.add_related_words_field)

    def add_related_words_field(self) -> None:
        self.related_words_groupbox_layout.insertWidget(
            self._next_related_words_widget_index,
            RelatedWordsGroupBox(),
        )

        self._next_related_words_widget_index += 1

    @property
    def number_of_related_words_widgets_in_related_words_layout(self) -> int:
        return self._next_related_words_widget_index

    def set_fields_text(self):
        if self._definition is not None:
            self.definition_lineedit.setText(
                definition if (definition := self._definition.definition) else ""
            )

            self.example_lineedit.setText(
                example if (example := self._definition.example) else ""
            )

            for (i, related_word) in enumerate(self._definition.related_words):
                self.related_words_groupbox_layout.insertWidget(
                    i,
                    RelatedWordsGroupBox(related_word=related_word).set_fields_text(),
                )

                self._next_related_words_widget_index += 1

        return self

    def get_fields_content(self) -> Dict[str, Union[list, str]]:
        """
        Related words will not be added if it's relationship type is not provided
        """
        return {
            "definition": self.definition_lineedit.text().strip(),  # Required
            "example": self.example_lineedit.text().strip(),
            "related_words": [
                related_words_data
                for i in range(
                    self.number_of_related_words_widgets_in_related_words_layout
                )
                if (
                    (
                        related_words_data := (
                            self.related_words_groupbox_layout.itemAt(i)
                            .widget()
                            .get_fields_content()
                        )
                    )
                    and (related_words_data.get("relationship_type"))
                )
            ],
        }


class PronunciationGroupBox(QGroupBox, UiPronunciationGroupBox):
    next_widget_index = 0

    def __init__(
        self,
        pronunciation: Optional[Pronunciation] = None,
        *args,
        **kwargs,
    ) -> None:
        super(PronunciationGroupBox, self).__init__(*args, **kwargs)
        self._pronunciation = pronunciation
        self.setupUi(self)

    def set_fields_text(self):
        if self._pronunciation is not None:
            self.pronunciation_text_lineedit.setText(
                text if (text := self._pronunciation.text) else ""
            )

            self.pronunciation_audio_lineedit.setText(
                audio if (audio := self._pronunciation.audio) else ""
            )

        return self

    def get_fields_content(self) -> Dict[str, str]:
        return {
            "text": self.pronunciation_text_lineedit.text().strip(),
            "audio": self.pronunciation_audio_lineedit.text().strip(),
        }


class MeaningsGroupBox(QGroupBox, UiMeaningsGroupBox):
    next_widget_index = 0

    def __init__(
        self,
        meaning: Optional[Meaning] = None,
        *args,
        **kwargs,
    ) -> None:
        super(MeaningsGroupBox, self).__init__(*args, **kwargs)
        self._meaning = meaning
        self._next_definition_widget_index = 0
        self.setupUi(self)
        self.add_definition_button.setIcon(plus_icon)
        self.install_slots()
        self.add_definition_field()

    def install_slots(self) -> None:
        self.add_definition_button.clicked.connect(self.add_definition_field)

    def add_definition_field(self) -> None:
        self.definition_layout.insertWidget(
            self._next_definition_widget_index,
            DefinitionGroupBox(),
        )

        self._next_definition_widget_index += 1

    @property
    def number_of_definition_widgets_in_definition_layout(self) -> int:
        return self._next_definition_widget_index

    def set_fields_text(self):
        if self._meaning is not None:
            self.part_of_speech_lineedit.setText(
                pos if (pos := self._meaning.part_of_speech) else ""
            )

            for (i, definition) in enumerate(self._meaning.definitions):
                self.definition_layout.insertWidget(
                    i,
                    DefinitionGroupBox(definition=definition).set_fields_text(),
                )

                self._next_definition_widget_index += 1

        return self

    def get_fields_content(self) -> Dict[str, Union[list, str]]:
        """
        A definition will not be included if it does not have the definition field
        """
        return {
            "part_of_speech": self.part_of_speech_lineedit.text().strip(),  # Required
            "definitions": [
                definition_data
                for i in range(self.number_of_definition_widgets_in_definition_layout)
                if (
                    (
                        definition_data := self.definition_layout.itemAt(i)
                        .widget()
                        .get_fields_content()
                    )
                    and (definition_data.get("definition"))
                )
            ],
        }


class AddWordDialog(QDialog, UiAddWordDialog):
    def __init__(self, *args, **kwargs) -> None:
        super(AddWordDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.add_meaning_button.setIcon(plus_icon)
        self.add_pronunciation_button.setIcon(plus_icon)
        self.install_slots()
        self.add_pronunciation_field()
        self.add_meaning_field()

    def install_slots(self) -> None:
        self.add_pronunciation_button.clicked.connect(self.add_pronunciation_field)
        self.add_meaning_button.clicked.connect(self.add_meaning_field)

    def add_meaning_field(self) -> None:
        self.meanings_layout.insertWidget(
            MeaningsGroupBox.next_widget_index,
            MeaningsGroupBox(),
        )

        MeaningsGroupBox.next_widget_index += 1

    def add_pronunciation_field(self) -> None:
        self.pronunciation_layout.insertWidget(
            PronunciationGroupBox.next_widget_index,
            PronunciationGroupBox(),
        )

        PronunciationGroupBox.next_widget_index += 1

    def get_results(self) -> Optional[BaseAPI]:
        if self.name_lineedit.text().strip() == "":
            message = QMessageBox.critical(
                None,
                self.windowTitle(),
                "Word field cannot be empty",
            )
            return None

        word_data = [
            {
                "name": self.name_lineedit.text().strip(),  # Required
                "etymology": self.etymology_lineedit.text().strip(),
                "pronunciations": [
                    pronunciation_data
                    for i in range(PronunciationGroupBox.next_widget_index)
                    if (
                        (
                            pronunciation_data := (
                                self.pronunciation_layout.itemAt(i)
                                .widget()
                                .get_fields_content()
                            )
                        )
                        and (
                            pronunciation_data.get("text")
                            or pronunciation_data.get("audio")
                        )
                    )
                ],
                "meanings": [
                    meaning_data
                    for i in range(MeaningsGroupBox.next_widget_index)
                    if (
                        (
                            meaning_data := (
                                self.meanings_layout.itemAt(i)
                                .widget()
                                .get_fields_content()
                            )
                        )
                        and (meaning_data.get("part_of_speech"))
                    )
                ],
            }
        ]
        return word_data


class EditWordDialog(AddWordDialog):
    def __init__(
        self,
        word_data: WordData = None,
        *args,
        **kwargs,
    ) -> None:
        super(AddWordDialog, self).__init__(*args, **kwargs)
        self._word_data = word_data
        self.setupUi(self)
        self.install_slots()
        self.fill_values()

    def fill_values(self) -> None:
        self.name_lineedit.setText(self._word_data.get_name())
        self.etymology_lineedit.setText(
            etymology if (etymology := self._word_data.etymology) else ""
        )

        for (i, pronunciation) in enumerate(self._word_data.pronunciations):
            self.pronunciation_layout.insertWidget(
                i,
                PronunciationGroupBox(pronunciation=pronunciation).set_fields_text(),
            )

            PronunciationGroupBox.next_widget_index += 1

        for (i, meaning) in enumerate(self._word_data.meanings):
            self.meanings_layout.insertWidget(
                i,
                MeaningsGroupBox(meaning=meaning).set_fields_text(),
            )

            MeaningsGroupBox.next_widget_index += 1


class MainWindow(QMainWindow, UiMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.dictionary = Dictionary()
        self.setupUi(self)
        self.add_button.setIcon(plus_icon)
        self.delete_button.setIcon(QIcon(str(DELETE_SVG_PATH)))
        self.delete_button.setStyleSheet("background:red")
        self.search_button.setIcon(QIcon(str(SEARCH_SVG_PATH)))
        self.edit_button.setIcon(QIcon(str(EDIT_SVG_PATH)))
        self.install_slots()
        QGuiApplication.setFallbackSessionManagementEnabled(False)
        self.setUnifiedTitleAndToolBarOnMac(True)
        self.update_dictionary(self.dictionary.peek())
        self.fill_with_dummy_data()
        self.list_widget.sortItems(Qt.AscendingOrder)
        self.list_widget.setCurrentItem(self.list_widget.item(0))
        self.show()

    def add_word_handler(self) -> None:
        """Handler for adding new words to the dictionary"""
        dialog = AddWordDialog()
        if dialog.exec_() == QDialog.Accepted:
            if result := dialog.get_results():
                self.dictionary.append(WordData.from_api(result))
                with Database(DATABASE_DIRECTORY / DATABASE_NAME) as db:
                    db.save_word(result)
                self.update_dictionary(
                    [
                        WordData.from_api(result).get_name(),
                    ]
                )

    def install_slots(self) -> None:
        self.search_bar.textChanged.connect(self.filter_displayed_words)
        self.search_bar.returnPressed.connect(self.fetch_word_from_internet)
        self.search_button.clicked.connect(self.fetch_word_from_internet)

        self.add_button.clicked.connect(self.add_word_handler)

        self.list_widget.currentItemChanged.connect(self.display_detail)

        self.edit_button.clicked.connect(self.edit_word)

        self.delete_button.clicked.connect(self.delete_word)

    def filter_displayed_words(self, text: str) -> None:
        """Perform real time filtering of words as the user is typing"""
        for widget in self.list_widget.findItems("", Qt.MatchContains):
            if widget in self.list_widget.findItems(text, Qt.MatchContains):
                widget.setHidden(False)
            else:
                widget.setHidden(True)

    def edit_word(self) -> None:
        text = self.list_widget.currentItem().text()
        word = self.fetch_word(text)

        dialog = EditWordDialog(word_data=word)
        if dialog.exec_() == QDialog.Accepted:
            if result := dialog.get_results():
                self.dictionary.edit_word(word, WordData.from_api(result))
                with Database(DATABASE_DIRECTORY / DATABASE_NAME) as db:
                    db.edit_word(result)
                    self.update_dictionary(
                        [
                            WordData.from_api(result).get_name(),
                        ]
                    )

    def update_dictionary(self, words: Sequence[str]) -> None:
        """Update the UI"""
        for word in words:
            if self.list_widget.findItems(word, Qt.MatchExactly):
                continue
            self.list_widget.addItem(word)
        self.list_widget.sortItems(Qt.AscendingOrder)

    def delete_word(self) -> None:
        """Remove a word from the dictionary"""
        word = self.list_widget.currentItem().text()
        with Database(DATABASE_DIRECTORY / DATABASE_NAME) as db:
            db.delete_word(word)
        self.dictionary.remove(self.dictionary.get_word_details(word))
        self.list_widget.takeItem(self.list_widget.row(self.list_widget.currentItem()))

    def display_detail(self) -> None:
        """Display details of a word in the dictionary"""
        if len(self.list_widget.findItems("", Qt.MatchContains)) == 1:
            self.text_browser.clear()
            self.edit_button.setVisible(False)
            return

        text = self.parse_word_data(self.list_widget.currentItem().text())
        self.text_browser.setHtml(text)
        self.list_widget.sortItems(Qt.AscendingOrder)

        if not self.edit_button.isVisible():
            self.edit_button.setVisible(True)

    def fetch_word(self, word: str) -> WordData:
        """Returns a word with its details from the dictionary with the word's name alone"""
        return self.dictionary.get_word_details(word)

    def fetch_word_from_internet(self):
        """Fetch word from internet if not present in storage"""
        text = self.search_bar.text().strip().lower()

        if text in self.dictionary.peek():
            return

        message_box = QMessageBox()
        message_box.setText(
            f"The word '{text}' is not in your dictionary at the moment"
        )
        message_box.setInformativeText("Do you want to fetch from the internet?")
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        response = message_box.exec_()

        if response == QMessageBox.No:
            return

        from ..api import FreeDictionaryApi, BaseAPIBuilder

        parser = FreeDictionaryApi()

        try:
            word = parser.get_json(text)
        except Exception:
            message = QMessageBox.critical(
                None,
                self.windowTitle(),
                "Could not fetch word\nCheck your internet connection and try again",
            )
            return

        word = BaseAPIBuilder.from_free_dictionary_api(word)
        with Database(DATABASE_DIRECTORY / DATABASE_NAME) as db:
            db.save_word(word)
        word_data = WordData.from_api(word)
        self.dictionary.append(word_data)
        self.update_dictionary(
            [
                word_data.get_name(),
            ]
        )

    def parse_word_data(self, word: str) -> str:
        """Convert a word (with name alone) into HTML with all its details."""
        word = self.fetch_word(word)

        from english_dictionary.utils.formatter import BaseAPIFormatter

        formatter = BaseAPIFormatter(word)

        return (
            f"<b style='font-size: 40px'>{word.get_name().capitalize()}</b><hr />"
            + formatter.to_html()
        )

    def fill_with_dummy_data(self):
        with Database(DATABASE_DIRECTORY / DATABASE_NAME) as db:
            for word in db.fetch_all_words():
                word_data = WordData.from_api(word)
                self.dictionary.append(word_data)
                self.update_dictionary([word_data.get_name()])
