# gui/dialogs.py
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox
from PySide6.QtCore import Qt

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Kozy Control Panel")
        self.setFixedSize(500, 300)
        if parent:
            self.setStyleSheet(parent.styleSheet())

        layout = QVBoxLayout(self)

        title_label = QLabel("Kozy Control Panel")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #b8a0ff; margin: 20px;")
        layout.addWidget(title_label)

        description_label = QLabel("Silly program IDK :P")
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setStyleSheet("color: #c5c8d6; margin: 10px;")
        layout.addWidget(description_label)

        footer_label = QLabel("Made by Datafy Lab")
        footer_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        footer_label.setStyleSheet("color: #5a5080; font-size: 10px; margin: 10px;")
        layout.addWidget(footer_label)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)
