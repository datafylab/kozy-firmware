#!/usr/bin/env python3
"""Test script to verify imports work correctly."""

try:
    from PySide6.QtWidgets import (
        QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
        QTabWidget, QLabel, QTextEdit, QPushButton, QSplitter, QFrame,
        QPlainTextEdit, QSizePolicy, QGroupBox, QComboBox, QMenuBar, QMenu,
        QToolButton, QMenu, QScrollArea, QStyle
    )
    from PySide6.QtGui import QAction, QIcon, QPalette, QColor
    from PySide6.QtCore import Qt, QTimer, QSize
    from PySide6.QtGui import QImage, QPixmap, QIcon
    
    print("All imports successful!")
    
    # Try creating a simple QApplication to verify GUI functionality
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    print("QApplication created successfully!")
    print("All tests passed - imports are working correctly.")
    
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)