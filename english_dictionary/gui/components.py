from typing import Sequence, Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QMainWindow, QDialog, QMessageBox

from .add_word_dialog import Ui_Dialog
from .mainwindow import Ui_MainWindow
from ..api import BaseAPI
from ..core import Dictionary, WordData
from ..database import DATABASE_DIRECTORY, DATABASE_NAME, Database


class AddWordDialog(QDialog, Ui_Dialog):
    def __init__(self, *args, **kwargs) -> None:
        super(AddWordDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)

    def get_results(self) -> Optional[BaseAPI]:
        if self.name_textedit.text().strip() == "":
            message = QMessageBox.critical(
                None, self.windowTitle(), "Word field cannot be empty"
            )
            return None

        word_data = [
            {
                "name": self.name_textedit.text().strip(),
                "etymology": self.etymology_textedit.text().strip(),
                "meanings": [
                    {
                        "part_of_speech": self.part_of_speech_textedit_1.text().strip(),
                        "definitions": [
                            {
                                "definition": self.definition_textedit_1.text().strip(),
                                "example": self.examples_textedit_1.text().strip(),
                                "related_words": [
                                    {
                                        "relationship_type": self.relationship_type_textedit.text().strip(),
                                        "words": self.words_text_edit_1.text()
                                        .strip()
                                        .split(", ")
                                        if self.words_text_edit_1.text()
                                        else "",
                                    }
                                ],
                            }
                        ],
                    }
                ],
            }
        ]
        return word_data


class EditWordDialog(AddWordDialog):
    def __init__(self, word_data: WordData = None, *args, **kwargs) -> None:
        super(AddWordDialog, self).__init__(*args, **kwargs)
        self._word_data = word_data
        self.setupUi(self)
        self.fill_values()

    def fill_values(self) -> None:
        self.name_textedit.setText(self._word_data.get_name())


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.dictionary = Dictionary()
        self.setupUi(self)
        self.install_handlers()
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
                with Database(DATABASE_DIRECTORY / DATABASE_NAME) as db:
                    db.save_word(result)
                self.dictionary.append(WordData.from_api(result))
                self.update_dictionary([WordData.from_api(result).get_name()])

    def install_handlers(self) -> None:
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

        def add_handler():
            dialog = EditWordDialog(word_data=word)
            dialog.exec_()

        add_handler()

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
        self.update_dictionary([word_data.get_name()])

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
