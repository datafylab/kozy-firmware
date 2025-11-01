# gui/styles.py

def get_raw_cyber_stylesheet():
    return """
    QMainWindow, QWidget {
        background-color: #090a0f;
        color: #c5c8d6;
        font-family: "Cascadia Code", "Fira Code", "Monospace", sans-serif;
        font-size: 10pt;
    }
    QLabel { color: #d0d3e0; }
    QTabWidget::pane {
        border: 1px solid #3a3550;
        background: #0d0e16;
        border-radius: 4px;
    }
    QTabBar::tab {
        background: #141522;
        color: #a0a5c0;
        padding: 8px 16px;
        margin: 2px;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
    }
    QTabBar::tab:selected {
        background: #1e1f30;
        color: #b8a0ff;
    }
    QFrame {
        background: #0c0d15;
        border: 1px solid #2a2740;
        border-radius: 6px;
        padding: 8px;
    }
    QPushButton {
        background: #1a1b2a;
        color: #c0b0ff;
        border: 1px solid #3a3550;
        padding: 6px 14px;
        border-radius: 4px;
    }
    QPushButton:hover { background: #222335; border-color: #5a5080; }
    QPushButton:pressed { background: #2a2b40; }
    QComboBox {
        background: #0f101c;
        color: #c5c8d6;
        border: 1px solid #2a2740;
        padding: 4px;
        border-radius: 4px;
    }
    QComboBox:hover { border-color: #5a5080; }
    QPlainTextEdit, QTextEdit {
        background: #0b0c14;
        color: #c5c8d6;
        border: 1px solid #2a2740;
        border-radius: 4px;
        selection-background-color: #2a2845;
    }
    """
