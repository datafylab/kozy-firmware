# utils/logger.py
import logging
from PySide6.QtWidgets import QPlainTextEdit

class QLogHandler(logging.Handler):
    def __init__(self, text_edit: QPlainTextEdit):
        super().__init__()
        self.text_edit = text_edit

    def emit(self, record):
        msg = self.format(record)
        self.text_edit.appendPlainText(msg)

def setup_logger(text_edit: QPlainTextEdit):
    handler = QLogHandler(text_edit)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)
