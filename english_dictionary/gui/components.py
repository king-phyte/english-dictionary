from typing import Sequence, Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QMainWindow, QDialog, QMessageBox

from .add_word_dialog import Ui_Dialog
from .mainwindow import Ui_MainWindow
from ..api import BaseAPI
from ..core import Dictionary, WordData


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

        word = WordData.from_api(BaseAPIBuilder.from_free_dictionary_api(word))
        self.dictionary.append(word)
        self.update_dictionary([word.get_name()])

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
        from ..api import BaseAPIBuilder

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

        power = WordData.from_api(
            BaseAPIBuilder.from_free_dictionary_api(
                [
                    {
                        "word": "power",
                        "phonetic": "\u02c8pa\u028a\u0259",
                        "phonetics": [
                            {
                                "text": "\u02c8pa\u028a\u0259",
                                "audio": "//ssl.gstatic.com/dictionary/static/sounds/20200429/power--_gb_1.mp3",
                            }
                        ],
                        "origin": (
                            "Middle English: from Anglo-Norman French poeir, "
                            "from an alteration of Latin posse \u2018be able\u2019."
                        ),
                        "meanings": [
                            {
                                "partOfSpeech": "noun",
                                "definitions": [
                                    {
                                        "definition": (
                                            "the ability or capacity to do something or act in a particular way."
                                        ),
                                        "example": "the power of speech",
                                        "synonyms": [
                                            "ability",
                                            "capacity",
                                            "capability",
                                            "potential",
                                            "potentiality",
                                            "faculty",
                                            "property",
                                            "competence",
                                            "competency",
                                        ],
                                        "antonyms": ["inability", "incapacity"],
                                    },
                                    {
                                        "definition": (
                                            "the capacity or ability to direct or influence "
                                            "the behaviour of others or the course of events."
                                        ),
                                        "example": "a political process that offers people power over their own lives",
                                        "synonyms": [],
                                        "antonyms": [],
                                    },
                                    {
                                        "definition": "physical strength and force exerted by something or someone.",
                                        "example": "the power of the storm",
                                        "synonyms": [
                                            "strength",
                                            "powerfulness",
                                            "might",
                                            "force",
                                            "forcefulness",
                                            "mightiness",
                                            "weight",
                                            "vigour",
                                            "energy",
                                            "intensity",
                                            "potency",
                                            "brawn",
                                            "brawniness",
                                            "muscle",
                                            "punch",
                                            "welly",
                                            "thew",
                                            "eloquence",
                                            "effectiveness",
                                            "cogency",
                                            "persuasiveness",
                                            "impressiveness",
                                            "authoritativeness",
                                        ],
                                        "antonyms": ["weakness", "impotence"],
                                    },
                                    {
                                        "definition": (
                                            "energy that is produced by mechanical, electrical, "
                                            "or other means and used to operate a device."
                                        ),
                                        "example": "generating power from waste",
                                        "synonyms": [
                                            "energy",
                                            "electrical power",
                                            "nuclear power",
                                            "solar power",
                                            "steam power",
                                            "water power",
                                            "juice",
                                        ],
                                        "antonyms": [],
                                    },
                                    {
                                        "definition": (
                                            "the rate of doing work, measured in watts "
                                            "or less frequently horse power."
                                        ),
                                        "synonyms": [],
                                        "antonyms": [],
                                    },
                                    {
                                        "definition": (
                                            "the product obtained when a number is multiplied "
                                            "by itself a certain number of times."
                                        ),
                                        "example": "2 to the power of 4 equals 16",
                                        "synonyms": [],
                                        "antonyms": [],
                                    },
                                    {
                                        "definition": "a large number or amount of something.",
                                        "example": (
                                            "there's a power of difference between "
                                            "farming now and when I was a lad"
                                        ),
                                        "synonyms": [
                                            "a great deal of",
                                            "a lot of",
                                            "much",
                                            "lots of",
                                            "loads of",
                                            "heaps of",
                                            "masses of",
                                            "tons of",
                                            "a deal of",
                                        ],
                                        "antonyms": [],
                                    },
                                ],
                            },
                            {
                                "partOfSpeech": "verb",
                                "definitions": [
                                    {
                                        "definition": "supply (a device) with mechanical or electrical energy.",
                                        "example": "the car is powered by a fuel-injected 3.0-litre engine",
                                        "synonyms": [],
                                        "antonyms": [],
                                    },
                                    {
                                        "definition": "move or travel with great speed or force.",
                                        "example": "he powered round a bend",
                                        "synonyms": [],
                                        "antonyms": [],
                                    },
                                ],
                            },
                        ],
                    }
                ]
            )
        )
        self.dictionary.append_multiple([king, hello, power])
        self.update_dictionary([king.get_name(), hello.get_name(), power.get_name()])
