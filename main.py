# main.py
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont
from gui.main_window import RobotGUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Monospace", 10)
    font.setStyleHint(QFont.TypeWriter)
    app.setFont(font)

    window = RobotGUI()
    window.show()
    sys.exit(app.exec())
