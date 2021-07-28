from typing import Sequence

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication, QIcon
from PyQt5.QtWidgets import (
    QSplitter,
    QMainWindow,
    QHBoxLayout,
    QFrame,
    QApplication,
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
)

from utils.types import Dictionary, WordData


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

        self.search_button = QPushButton(QIcon("../utils/svgs/search.svg"), "")
        self.add_word_button = QPushButton(QIcon("../utils/svgs/plus.svg"), "")
        self.edit_word_button = QPushButton("Edit")
        self.delete_word_button = QPushButton("Delete")
        self.detail_display = QTextBrowser()

        self.build_window()
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

        from gui.words import king, queen, test

        self.dictionary.append_multiple([king, test, queen])
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
            def accepted_():

                if word_field.text() == "":
                    message = QMessageBox.critical(
                        None, self.window_title, "Word field cannot be empty"
                    )
                    return

                word_data = {
                    "name": word_field.text().strip(),
                    "data": [
                        {
                            "etymology": etymology_field.text().strip()
                            if etymology_field.text()
                            else None,
                            "definitions": [
                                {
                                    "part_of_speech": part_of_speech_field.text().strip()
                                    if part_of_speech_field.text()
                                    else None,
                                    "texts": [
                                        text_field.text().strip()
                                        if text_field.text()
                                        else None,
                                    ],
                                    "related_words": [
                                        {
                                            "relationship_type": relationship_type_field.text().strip()
                                            if relationship_type_field.text()
                                            else None,
                                            "words": words_field.text().strip().split()
                                            if relationship_type_field.text()
                                            else None,
                                        }
                                    ],
                                    "example_uses": [
                                        examples_field.text().strip()
                                        if examples_field.text()
                                        else None,
                                    ],
                                }
                            ],
                        }
                    ],
                }
                self.dictionary.append(WordData.from_dict(word_data))

                self.update_dictionary([WordData.from_dict(word_data).get_name()])

                dialog.close()

            def cancel_handler():
                dialog.close()

            vbox = QVBoxLayout()
            dialog = QDialog()
            dialog.setWindowTitle("Add Word")
            description = QFormLayout()
            part_of_speech_field = QLineEdit()
            description.addRow(QLabel("Part of Speech"), part_of_speech_field)
            text_field = QLineEdit()
            description.addRow(QLabel("Text"), text_field)
            description_group = QGroupBox()

            description_group.setLayout(description)

            related_words = QFormLayout()
            relationship_type_field = QLineEdit()
            related_words.addRow(QLabel("Relationship Type"), relationship_type_field)
            words_field = QLineEdit()
            related_words.addRow(QLabel("Words"), words_field)
            related_words_group = QGroupBox()

            related_words_group.setLayout(related_words)

            examples = QFormLayout()
            examples_field = QLineEdit()
            examples.addWidget(examples_field)

            examples_group = QGroupBox()
            examples_group.setLayout(examples)

            form_layout = QFormLayout()

            word_field = QLineEdit()
            etymology_field = QLineEdit()
            word_field.setClearButtonEnabled(True)
            form_layout.addRow(QLabel("Word"), word_field)
            form_layout.addRow(QLabel("Etymology"), etymology_field)
            form_layout.addRow(QLabel("Description"), description_group)
            form_layout.addRow(QLabel("Related Words"), related_words_group)
            form_layout.addRow(QLabel("Examples"), examples_group)

            vbox.addLayout(form_layout)
            group_box = QGroupBox()

            hbox = QHBoxLayout()

            done_button = QPushButton("Done")
            done_button.clicked.connect(accepted_)

            cancel_button = QPushButton("Cancel")
            cancel_button.clicked.connect(cancel_handler)
            hbox.addWidget(done_button)
            hbox.addWidget(cancel_button)

            group_box.setLayout(hbox)
            vbox.addWidget(group_box)
            dialog.setLayout(vbox)
            dialog.setModal(True)
            dialog.exec_()

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
            def accepted_():

                if word_field.text().strip() == "":
                    message = QMessageBox.critical(
                        None, self.window_title, "Word field cannot be empty"
                    )
                    return

                word_data = {
                    "name": word_field.text().strip(),
                    "data": [
                        {
                            "etymology": etymology_field.text().strip()
                            if etymology_field.text()
                            else None,
                            "definitions": [
                                {
                                    "part_of_speech": part_of_speech_field.text().strip()
                                    if part_of_speech_field.text()
                                    else None,
                                    "texts": [
                                        text_field.text().strip()
                                        if text_field.text()
                                        else None,
                                    ],
                                    "related_words": None
                                    if not relationship_type_field.text().strip()
                                    else [
                                        {
                                            "relationship_type": relationship_type_field.text().strip(),
                                            "words": words_field.text().strip(),
                                        }
                                    ],
                                    "example_uses": None
                                    if not examples_field.text().strip()
                                    else [examples_field.text().strip()],
                                }
                            ],
                        }
                    ],
                }
                result = WordData.from_dict(word_data)
                self.delete_word()

                self.dictionary.append(result)

                self.update_dictionary([result.get_name()])
                self.list_widget.setCurrentItem(
                    self.list_widget.item(self.list_widget.currentRow() - 1)
                )
                dialog.close()

            def cancel_handler():
                dialog.close()

            vbox = QVBoxLayout()
            dialog = QDialog()
            dialog.setWindowTitle("Add Word")

            description = QFormLayout()
            part_of_speech_field = QLineEdit(word.definition_list[0].part_of_speech)
            part_of_speech_field.setClearButtonEnabled(True)
            description.addRow(QLabel("Part of Speech"), part_of_speech_field)
            text_field = QLineEdit(
                word.definition_list[0].texts[0]
                if word.definition_list[0].texts
                else ""
            )
            text_field.setClearButtonEnabled(True)

            description.addRow(QLabel("Text"), text_field)
            description_group = QGroupBox()

            description_group.setLayout(description)

            related_words = QFormLayout()
            rel_wor = word.definition_list[0].related_words
            relationship_type_field = QLineEdit(
                f"{rel_wor[0].relationship_type if rel_wor else ''}"
            )
            relationship_type_field.setClearButtonEnabled(True)

            related_words.addRow(QLabel("Relationship Type"), relationship_type_field)
            words_field = QLineEdit(f"{rel_wor[0].words[0] if rel_wor else ''}")
            words_field.setClearButtonEnabled(True)

            related_words.addRow(QLabel("Words"), words_field)
            related_words_group = QGroupBox()

            related_words_group.setLayout(related_words)

            examples = QFormLayout()
            examples_field = QLineEdit(
                word.definition_list[0].example_uses[0]
                if word.definition_list[0].example_uses
                else ""
            )
            examples_field.setClearButtonEnabled(True)
            examples.addWidget(examples_field)

            examples_group = QGroupBox()
            examples_group.setLayout(examples)

            form_layout = QFormLayout()

            word_field = QLineEdit(word.get_name())
            word_field.setClearButtonEnabled(True)
            etymology_field = QLineEdit(word.etymology if word.etymology else "")
            etymology_field.setClearButtonEnabled(True)
            form_layout.addRow(QLabel("Word"), word_field)
            form_layout.addRow(QLabel("Etymology"), etymology_field)
            form_layout.addRow(QLabel("Description"), description_group)
            form_layout.addRow(QLabel("Related Words"), related_words_group)
            form_layout.addRow(QLabel("Examples"), examples_group)

            vbox.addLayout(form_layout)
            group_box = QGroupBox()

            hbox = QHBoxLayout()

            done_button = QPushButton("Done")
            done_button.clicked.connect(accepted_)

            cancel_button = QPushButton("Cancel")
            cancel_button.clicked.connect(cancel_handler)
            hbox.addWidget(done_button)
            hbox.addWidget(cancel_button)

            group_box.setLayout(hbox)
            vbox.addWidget(group_box)
            dialog.setLayout(vbox)
            dialog.setModal(True)
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
        self.dictionary.remove_word(self.dictionary.get_word_details(word))
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

        import json
        from wiktionaryparser.core import WiktionaryParser

        parser = WiktionaryParser()

        json_data = parser.fetch(text)

        print(json_data)

        with open("../try.json", "w") as f:
            json.dump(json_data, f, indent=4)

        json_data = {"name": text, "data": json_data}
        word = WordData.from_dict(json_data)
        self.dictionary.append(word)
        self.update_dictionary([word.get_name()])
        # print(self.dictionary.peek())

    def parse_word_data(self, word: str) -> str:
        word = self.fetch_word(word)

        from utils.formatter import FormatWord

        return (
            f"<b style='font-size: 40px'>{word.get_name().capitalize()}</b><hr />"
            + FormatWord.to_html(word)
        )


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
