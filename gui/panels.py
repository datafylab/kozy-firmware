# gui/panels.py
from PySide6.QtWidgets import QGroupBox, QLabel

class DevicePanel(QGroupBox):
    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #b8a0ff;
                border: 1px solid #2a2740;
                border-radius: 4px;
                margin-top: 12px;
                padding-top: 8px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 4px;
            }
        """)
        self.status_label = QLabel("Status: Unknown")
        self.status_label.setStyleSheet("color: #a0a5c0; font-weight: normal;")

    def set_status(self, text, color="#a0a5c0"):
        self.status_label.setText(f"Status: {text}")
        self.status_label.setStyleSheet(f"color: {color}; font-weight: normal;")
