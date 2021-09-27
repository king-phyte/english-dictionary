from pathlib import Path
from typing import Sequence

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication, QIcon
from PyQt5.QtWidgets import (
    QSplitter,
    QMainWindow,
    QHBoxLayout,
    QFrame,
    QLineEdit,
    QPushButton,
    QListWidget,
    QVBoxLayout,
    QGridLayout,
    QTextBrowser,
    QDialog,
    QFormLayout,
    QLabel,
    QGroupBox,
    QMessageBox,
    QWidget,
)

from english_dictionary.types import Dictionary, WordData

SVGS_DIR = Path(__file__).parent / "svgs"


class AddWordDialog(QDialog):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.description = QFormLayout()
        self.part_of_speech_field = QLineEdit()
        self.text_field = QLineEdit()
        self.description_group = QGroupBox()
        self.vbox = QVBoxLayout()
        self.group_box = QGroupBox()
        self.hbox = QHBoxLayout()
        self.done_button = QPushButton("Done")
        self.cancel_button = QPushButton("Cancel")
        self.related_words = QFormLayout()
        self.relationship_type_field = QLineEdit()
        self.words_field = QLineEdit()
        self.related_words_group = QGroupBox()
        self.examples = QFormLayout()
        self.examples_field = QLineEdit()
        self.examples_group = QGroupBox()
        self.form_layout = QFormLayout()
        self.word_field = QLineEdit()
        self.etymology_field = QLineEdit()
        self.build_ui()

    def build_ui(self):
        self.setWindowTitle("Add Word")
        self.setModal(True)

        self.description.addRow(QLabel("Part of Speech"), self.part_of_speech_field)
        self.description.addRow(QLabel("Text"), self.text_field)
        self.description_group.setLayout(self.description)
        self.related_words.addRow(
            QLabel("Relationship Type"), self.relationship_type_field
        )
        self.related_words.addRow(QLabel("Words"), self.words_field)
        self.related_words_group.setLayout(self.related_words)
        self.examples.addWidget(self.examples_field)
        self.examples_group.setLayout(self.examples)
        self.word_field.setClearButtonEnabled(True)
        self.form_layout.addRow(QLabel("Word"), self.word_field)
        self.form_layout.addRow(QLabel("Etymology"), self.etymology_field)
        self.form_layout.addRow(QLabel("Description"), self.description_group)
        self.form_layout.addRow(QLabel("Related Words"), self.related_words_group)
        self.form_layout.addRow(QLabel("Examples"), self.examples_group)
        self.vbox.addLayout(self.form_layout)
        self.done_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        self.hbox.addWidget(self.done_button)
        self.hbox.addWidget(self.cancel_button)
        self.group_box.setLayout(self.hbox)

        self.vbox.addWidget(self.group_box)

        self.setLayout(self.vbox)

    def get_results(self):
        if self.word_field.text().strip() == "":
            message = QMessageBox.critical(
                None, self.windowTitle(), "Word field cannot be empty"
            )
            return None

        word_data = [
            {
                "name": self.word_field.text().strip(),
                "etymology": self.etymology_field.text().strip(),
                "meanings": [
                    {
                        "part_of_speech": self.part_of_speech_field.text().strip(),
                        "definitions": [
                            {
                                "definition": self.text_field.text().strip(),
                                "example": self.examples_field.text().strip(),
                                "related_words": [
                                    {
                                        "relationship_type": self.relationship_type_field.text().strip(),
                                        "words": self.words_field.text().strip().split()
                                        if self.words_field.text()
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
    def __init__(self, parent: QWidget = None, word_data: WordData = None) -> None:
        super(AddWordDialog, self).__init__(parent=parent)
        self.word_data = word_data
        self.fill_values()
        self.build_ui()

    def fill_values(self):
        self.word_field.setText(self.word_data["name"])


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.dictionary = Dictionary()

        self.window_title = "English Dictionary"

        self.central_frame = QFrame(self)
        self.splitter = QSplitter(self.central_frame)
        self.left_frame = QFrame(self.splitter)
        self.right_frame = QFrame(self.splitter)
        self.top_left_layout_2 = QGridLayout(self.left_frame)
        self.grid_layout = QGridLayout(self.right_frame)

        self.list_widget = QListWidget()
        self.search_bar = QLineEdit()

        self.search_button = QPushButton(QIcon(str(SVGS_DIR / "search.svg")), "")
        self.add_word_button = QPushButton(QIcon(str(SVGS_DIR / "plus.svg")), "")
        self.edit_word_button = QPushButton("Edit")
        self.delete_word_button = QPushButton("Delete")
        self.detail_display = QTextBrowser()

        self.build_window()
        self.fill_with_dummy_data()
        self.list_widget.setCurrentItem(self.list_widget.item(0))
        self.show()

    def build_window(self):
        left, top, width, height = 100, 100, 800, 600
        self.setWindowTitle(self.window_title)
        self.setGeometry(left, top, width, height)

        QGuiApplication.setFallbackSessionManagementEnabled(False)
        self.setUnifiedTitleAndToolBarOnMac(True)

        hbox = QHBoxLayout(self.central_frame)
        hbox.addWidget(self.splitter)

        self.search_bar.setFixedWidth(200)
        self.search_bar.setPlaceholderText("Search")
        self.search_bar.setClearButtonEnabled(True)
        self.search_bar.setMaxLength(32)
        self.search_bar.textChanged.connect(self.filter_displayed_words)
        self.search_bar.returnPressed.connect(self.fetch_word_from_internet)

        self.search_button.clicked.connect(self.fetch_word_from_internet)
        self.list_widget.setSortingEnabled(True)
        self.list_widget.sortItems(Qt.AscendingOrder)

        self.top_left_layout_2.addWidget(self.search_bar, 1, 1, 1, 4, Qt.AlignLeft)
        self.top_left_layout_2.addWidget(self.search_button, 1, 5, 1, 1, Qt.AlignLeft)
        self.top_left_layout_2.addWidget(self.add_word_button, 1, 6, 1, 1, Qt.AlignLeft)
        self.top_left_layout_2.addWidget(self.list_widget, 2, 1, 1, 6, Qt.AlignLeft)

        self.splitter.setHandleWidth(20)

        self.delete_word_button.setStyleSheet("background: red")

        self.detail_display.setMinimumSize(600, 600)
        self.detail_display.setAcceptRichText(True)
        self.detail_display.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.detail_display.setStyleSheet("background: white")
        self.detail_display.setPlaceholderText(
            "Welcome to the English Dictionary app.\nPlease add a word to the dictionary."
        )
        self.detail_display.setReadOnly(True)

        self.grid_layout.addWidget(
            self.edit_word_button, 0, 4, 1, 1, alignment=Qt.AlignRight
        )
        self.grid_layout.addWidget(
            self.delete_word_button, 0, 5, 1, 1, alignment=Qt.AlignRight
        )
        self.grid_layout.addWidget(
            self.detail_display, 2, 0, 1, 6, alignment=Qt.AlignCenter
        )

        self.delete_word_button.clicked.connect(self.delete_word)
        self.edit_word_button.clicked.connect(self.edit_word)

        self.update_dictionary(self.dictionary.peek())

        self.list_widget.currentItemChanged.connect(lambda: self.display_detail())

        def add_handler():
            dialog = AddWordDialog()
            if dialog.exec_() == QDialog.Accepted:
                if result := dialog.get_results():
                    self.dictionary.append(WordData.from_api(result))
                    self.update_dictionary([WordData.from_api(result).get_name()])

        self.add_word_button.clicked.connect(add_handler)

        self.central_frame.setLayout(hbox)
        self.setCentralWidget(self.central_frame)

    def filter_displayed_words(self, text: str):
        for widget in self.list_widget.findItems("", Qt.MatchContains):
            if widget in self.list_widget.findItems(text, Qt.MatchContains):
                widget.setHidden(False)
            else:
                widget.setHidden(True)

    def edit_word(self):
        text = self.list_widget.currentItem().text()
        word = self.fetch_word(text)

        def add_handler():
            dialog = EditWordDialog(word_data=word)
            dialog.exec_()

        add_handler()

    def update_dictionary(self, words: Sequence[str]) -> None:
        for word in words:
            if self.list_widget.findItems(word, Qt.MatchExactly):
                continue
            self.list_widget.addItem(word)
        self.list_widget.sortItems(Qt.AscendingOrder)

    def delete_word(self):
        word = self.list_widget.currentItem().text()
        self.dictionary.remove(self.dictionary.get_word_details(word))
        self.list_widget.takeItem(self.list_widget.row(self.list_widget.currentItem()))

    def display_detail(self):
        if len(self.list_widget.findItems("", Qt.MatchContains)) == 1:
            self.detail_display.clear()
            self.edit_word_button.setVisible(False)
            return

        text = self.parse_word_data(self.list_widget.currentItem().text())
        self.detail_display.setHtml(text)
        self.list_widget.sortItems(Qt.AscendingOrder)

        if not self.edit_word_button.isVisible():
            self.edit_word_button.setVisible(True)

    def fetch_word(self, word: str) -> WordData:
        return self.dictionary.get_word_details(word)

    def fetch_word_from_internet(self):
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

        word = WordData.from_api(BaseAPIBuilder.from_free_dictionary_api(word))
        self.dictionary.append(word)
        self.update_dictionary([word.get_name()])

    def parse_word_data(self, word: str) -> str:
        word = self.fetch_word(word)

        from english_dictionary.utils.formatter import BaseAPIFormatter

        formatter = BaseAPIFormatter(word)

        return (
            f"<b style='font-size: 40px'>{word.get_name().capitalize()}</b><hr />"
            + formatter.to_html()
        )

    def fill_with_dummy_data(self):
        from english_dictionary.api import BaseAPIBuilder

        king = WordData.from_api(
            BaseAPIBuilder.from_free_dictionary_api(
                [
                    {
                        "word": "king",
                        "phonetic": "kɪŋ",
                        "phonetics": [
                            {
                                "text": "kɪŋ",
                                "audio": "//ssl.gstatic.com/dictionary/static/sounds/20200429/king--1_gb_1.mp3",
                            }
                        ],
                        "origin": (
                            "Old English cyning, cyng, of Germanic origin;"
                            "related to Dutch koning and German König, also to kin."
                        ),
                        "meanings": [
                            {
                                "partOfSpeech": "noun",
                                "definitions": [
                                    {
                                        "definition": (
                                            "the male ruler of an independent state, especially one who inherits"
                                            "the position by right of birth."
                                        ),
                                        "example": "King Henry VIII",
                                        "synonyms": [
                                            "ruler",
                                            "sovereign",
                                            "monarch",
                                            "supreme ruler",
                                            "crowned head",
                                            "majesty",
                                            "Crown",
                                            "head of state",
                                            "royal personage",
                                            "emperor",
                                            "prince",
                                            "potentate",
                                            "overlord",
                                            "liege lord",
                                            "lord",
                                            "leader",
                                            "chief",
                                        ],
                                        "antonyms": [],
                                    },
                                    {
                                        "definition": (
                                            "the most important chess piece, of which each player has one,"
                                            "which the opponent has to checkmate in order to win."
                                            "The king can move in any direction, including diagonally, to any"
                                            "adjacent square that is not attacked by an opponent's piece or pawn."
                                        ),
                                        "synonyms": [],
                                        "antonyms": [],
                                    },
                                ],
                            },
                            {
                                "partOfSpeech": "verb",
                                "definitions": [
                                    {
                                        "definition": "make (someone) king.",
                                        "synonyms": [],
                                        "antonyms": [],
                                    },
                                    {
                                        "definition": "act in an unpleasantly superior and domineering way.",
                                        "example": "he'll start kinging it over the lot of us again",
                                        "synonyms": [],
                                        "antonyms": [],
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "word": "God Save the Queen",
                        "phonetic": "ɡɒdseɪvðəˈkwiːn",
                        "phonetics": [
                            {
                                "text": "ɡɒdseɪvðəˈkwiːn",
                                "audio": (
                                    "//ssl.gstatic.com/dictionary/static/sounds/20200429/"
                                    "god_save_the_queen--1_gb_1.mp3"
                                ),
                            }
                        ],
                        "origin": (
                            "evidence suggests a 17th-century origin for the complete words and tune of the anthem."
                            "The ultimate origin is obscure: the phrase ‘God save the King’ occurs "
                            "in various passages in the Old Testament, while as early as 1545 it was a watchword in "
                            "the navy, with ‘long to reign over us’ as a countersign."
                        ),
                        "meanings": [
                            {
                                "partOfSpeech": "noun",
                                "definitions": [
                                    {
                                        "definition": "the British national anthem.",
                                        "synonyms": [],
                                        "antonyms": [],
                                    }
                                ],
                            }
                        ],
                    },
                ]
            )
        )

        hello = WordData.from_api(
            BaseAPIBuilder.from_free_dictionary_api(
                [
                    {
                        "word": "hello",
                        "phonetics": [
                            {
                                "text": "/həˈloʊ/",
                                "audio": "https://lex-audio.useremarkable.com/mp3/hello_us_1_rr.mp3",
                            },
                            {
                                "text": "/hɛˈloʊ/",
                                "audio": "https://lex-audio.useremarkable.com/mp3/hello_us_2_rr.mp3",
                            },
                        ],
                        "meanings": [
                            {
                                "partOfSpeech": "exclamation",
                                "definitions": [
                                    {
                                        "definition": "Used as a greeting or to begin a phone conversation.",
                                        "example": "hello there, Katie!",
                                    }
                                ],
                            },
                            {
                                "partOfSpeech": "noun",
                                "definitions": [
                                    {
                                        "definition": "An utterance of “hello”; a greeting.",
                                        "example": "she was getting polite nods and hellos from people",
                                        "synonyms": [
                                            "greeting",
                                            "welcome",
                                            "salutation",
                                            "saluting",
                                            "hailing",
                                            "address",
                                            "hello",
                                            "hallo",
                                        ],
                                    }
                                ],
                            },
                            {
                                "partOfSpeech": "intransitive verb",
                                "definitions": [
                                    {
                                        "definition": "Say or shout “hello”; greet someone.",
                                        "example": "I pressed the phone button and helloed",
                                    }
                                ],
                            },
                        ],
                    }
                ]
            )
        )

        self.dictionary.append(king)
        self.dictionary.append(hello)
        self.update_dictionary([king.get_name(), hello.get_name()])
