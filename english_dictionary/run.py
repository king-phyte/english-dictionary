#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication

import english_dictionary


def main():
    import sys

    app = QApplication(sys.argv)
    window = english_dictionary.gui.components.MainWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
