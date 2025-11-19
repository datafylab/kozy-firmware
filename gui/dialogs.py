# gui/dialogs.py
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QComboBox, QHBoxLayout
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


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Settings")
        self.setFixedSize(400, 200)
        if parent:
            self.setStyleSheet(parent.styleSheet())

        layout = QVBoxLayout(self)

        # Theme selection
        theme_layout = QHBoxLayout()
        theme_label = QLabel("Theme:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Raw Cyber", "Dark", "Light"])
        
        # Set current theme
        if parent:
            current_theme = parent.current_theme
            if current_theme == "raw_cyber":
                self.theme_combo.setCurrentText("Raw Cyber")
            elif current_theme == "dark":
                self.theme_combo.setCurrentText("Dark")
            elif current_theme == "light":
                self.theme_combo.setCurrentText("Light")
        
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)
        layout.addLayout(theme_layout)

        # Connect theme change
        self.theme_combo.currentTextChanged.connect(self.change_theme)

        # Add some spacing
        layout.addStretch()

        # OK button
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)

    def change_theme(self, theme_name):
        """Change the application theme when selection changes."""
        if self.parent:
            if theme_name == "Raw Cyber":
                self.parent.change_theme("raw_cyber")
            elif theme_name == "Dark":
                self.parent.change_theme("dark")
            elif theme_name == "Light":
                self.parent.change_theme("light")
