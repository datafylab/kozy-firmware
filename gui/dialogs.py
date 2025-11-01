# gui/dialogs.py
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox
from PySide6.QtCore import Qt

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Kozy-01 Control Panel")
        self.setFixedSize(500, 300)
        if parent:
            self.setStyleSheet(parent.styleSheet())

        layout = QVBoxLayout(self)

        logo_label = QLabel("Kozy-01 Control Panel")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #b8a0ff; margin: 20px;")
        layout.addWidget(logo_label)

        desc = QLabel("Silly program IDK :P")
        desc.setAlignment(Qt.AlignCenter)
        desc.setStyleSheet("color: #c5c8d6; margin: 10px;")
        layout.addWidget(desc)

        footer = QLabel("Made by Datafy Lab")
        footer.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        footer.setStyleSheet("color: #5a5080; font-size: 10px; margin: 10px;")
        layout.addWidget(footer)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)
