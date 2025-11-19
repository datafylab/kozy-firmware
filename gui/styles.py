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

def get_dark_stylesheet():
    return """
    QMainWindow, QWidget {
        background-color: #1e1e1e;
        color: #dcdcdc;
        font-family: "Cascadia Code", "Fira Code", "Monospace", sans-serif;
        font-size: 10pt;
    }
    QLabel { color: #cccccc; }
    QTabWidget::pane {
        border: 1px solid #3c3c3c;
        background: #2d2d30;
        border-radius: 4px;
    }
    QTabBar::tab {
        background: #333337;
        color: #cccccc;
        padding: 8px 16px;
        margin: 2px;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
    }
    QTabBar::tab:selected {
        background: #3d3d40;
        color: #ffffff;
    }
    QFrame {
        background: #252526;
        border: 1px solid #3c3c3c;
        border-radius: 6px;
        padding: 8px;
    }
    QPushButton {
        background: #333337;
        color: #ffffff;
        border: 1px solid #454545;
        padding: 6px 14px;
        border-radius: 4px;
    }
    QPushButton:hover { background: #3d3d40; border-color: #5a5a5a; }
    QPushButton:pressed { background: #454545; }
    QComboBox {
        background: #333337;
        color: #ffffff;
        border: 1px solid #454545;
        padding: 4px;
        border-radius: 4px;
    }
    QComboBox:hover { border-color: #5a5a5a; }
    QPlainTextEdit, QTextEdit {
        background: #1e1e1e;
        color: #dcdcdc;
        border: 1px solid #3c3c3c;
        border-radius: 4px;
        selection-background-color: #264f78;
    }
    """

def get_light_stylesheet():
    return """
    QMainWindow, QWidget {
        background-color: #f0f0f0;
        color: #000000;
        font-family: "Cascadia Code", "Fira Code", "Monospace", sans-serif;
        font-size: 10pt;
    }
    QLabel { color: #333333; }
    QTabWidget::pane {
        border: 1px solid #cccccc;
        background: #ffffff;
        border-radius: 4px;
    }
    QTabBar::tab {
        background: #e0e0e0;
        color: #333333;
        padding: 8px 16px;
        margin: 2px;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
    }
    QTabBar::tab:selected {
        background: #ffffff;
        color: #000000;
    }
    QFrame {
        background: #ffffff;
        border: 1px solid #cccccc;
        border-radius: 6px;
        padding: 8px;
    }
    QPushButton {
        background: #e0e0e0;
        color: #000000;
        border: 1px solid #cccccc;
        padding: 6px 14px;
        border-radius: 4px;
    }
    QPushButton:hover { background: #d0d0d0; border-color: #bbbbbb; }
    QPushButton:pressed { background: #c0c0c0; }
    QComboBox {
        background: #ffffff;
        color: #000000;
        border: 1px solid #cccccc;
        padding: 4px;
        border-radius: 4px;
    }
    QComboBox:hover { border-color: #bbbbbb; }
    QPlainTextEdit, QTextEdit {
        background: #ffffff;
        color: #000000;
        border: 1px solid #cccccc;
        border-radius: 4px;
        selection-background-color: #3399ff;
    }
    """
