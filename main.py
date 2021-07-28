from PyQt5.QtWidgets import QApplication

from gui.components import MainWindow

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
