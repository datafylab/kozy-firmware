# gui/main_window.py
import sys
import logging
import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QTabWidget, QLabel, QTextEdit, QPushButton, QSplitter, QFrame,
    QPlainTextEdit, QSizePolicy, QGroupBox, QComboBox, QMenuBar, QMenu,
    QToolButton, QMenu, QScrollArea, QStyle
)
from PySide6.QtGui import QAction, QIcon, QPalette, QColor
from PySide6.QtCore import Qt, QTimer, QSize
from PySide6.QtGui import QImage, QPixmap, QIcon

# Импорты наших модулей
from gui.styles import get_raw_cyber_stylesheet, get_dark_stylesheet, get_light_stylesheet
from gui.panels import DevicePanel
from gui.dialogs import AboutDialog, SettingsDialog
from utils.logger import setup_logger
from config import load_config, save_config
from devices.realsense import REAL_SENSE_AVAILABLE, rs, detect_realsense, normalize_depth_for_display

if REAL_SENSE_AVAILABLE:
    import numpy as np


class RobotGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.modules = {}  # Dictionary to store active modules
        self.module_widgets = {}  # Dictionary to store module widgets
        self.current_theme = "raw_cyber"  # Default theme
        self.initialize_window()
        self.create_widgets()
        self.setup_layout()
        self.setup_logging()
        self.initialize_devices()
    
    def initialize_window(self):
        """Initialize the main window properties."""
        self.setWindowTitle("Kozy Control Panel")
        self.resize(1500, 900)
        self.setStyleSheet(self.get_current_stylesheet())
        self.config = load_config()
        self.setup_menu()
        
        # Initialize RealSense variables
        self.pipeline = None
        self.timer = None
    
    def get_current_stylesheet(self):
        """Get the current theme stylesheet."""
        if self.current_theme == "raw_cyber":
            return get_raw_cyber_stylesheet()
        elif self.current_theme == "dark":
            return get_dark_stylesheet()
        elif self.current_theme == "light":
            return get_light_stylesheet()
        else:
            return get_raw_cyber_stylesheet()
    
    def change_theme(self, theme_name):
        """Change the application theme."""
        self.current_theme = theme_name
        self.setStyleSheet(self.get_current_stylesheet())
    
    def create_widgets(self):
        """Create all the main widgets for the interface."""
        self.control_panel = self.create_control_panel()
        self.tabs = self.create_tabs()
        self.console = self.create_console()
    
    def setup_layout(self):
        """Set up the main application layout."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.control_panel)
        splitter.addWidget(self.tabs)
        splitter.addWidget(self.console)
        splitter.setSizes([340, 900, 300])
        main_layout.addWidget(splitter)
    
    def setup_logging(self):
        """Initialize logging system."""
        setup_logger(self.log_text)
    
    def initialize_devices(self):
        """Detect and initialize connected devices."""
        self.detect_devices()
        QTimer.singleShot(100, self.auto_connect_pico)

    def auto_connect_pico(self):
        """Automatically connect to the Pico on startup."""
        logging.info("Auto-connecting to Pico...")
        self.connect_pico()

    def connect_pico(self):
        """Connect to the Raspberry Pi Pico and get its identification code."""
        from devices.pico import connect_to_pico
        self.btn_pico_connect.setEnabled(False)
        self.pico_panel.set_status("Connecting...", "#ffaa6b")

        pico_code = connect_to_pico()

        if pico_code:
            self.pico_panel.set_status(f"Code: {pico_code}", "#6bff9b")
            logging.info(f"Pico connected! Code: {pico_code}")
        else:
            self.pico_panel.set_status("Failed", "#ff6b6b")

        self.btn_pico_connect.setEnabled(True)

    def setup_menu(self):
        """Set up the application menu bar."""
        menu_bar = self.menuBar()
        menu_bar.setStyleSheet("background: #0c0d15; color: #c0b0ff;")
        
        file_menu = menu_bar.addMenu("File")
        file_menu.addAction("Save Configuration", self.save_configuration)
        file_menu.addAction("Load Configuration", self.load_configuration)
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)

        program_menu = menu_bar.addMenu("Program")
        program_menu.addAction("Settings", self.open_settings)
        
        # Theme submenu
        theme_menu = program_menu.addMenu("Theme")
        raw_cyber_action = theme_menu.addAction("Raw Cyber")
        raw_cyber_action.triggered.connect(lambda: self.change_theme("raw_cyber"))
        
        dark_action = theme_menu.addAction("Dark")
        dark_action.triggered.connect(lambda: self.change_theme("dark"))
        
        light_action = theme_menu.addAction("Light")
        light_action.triggered.connect(lambda: self.change_theme("light"))

    def open_settings(self):
        """Open the settings dialog."""
        from gui.dialogs import SettingsDialog
        settings_dialog = SettingsDialog(self)
        settings_dialog.exec()

    def create_control_panel(self):
        """Create the control panel with module management."""
        panel = QFrame()
        layout = QVBoxLayout(panel)
        layout.setAlignment(Qt.AlignCenter)  # Center the content

        # Add title
        title = QLabel("MODULES")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-weight: bold; color: #b8a0ff; margin-bottom: 8px;")
        layout.addWidget(title)

        # Create a scroll area for modules
        self.modules_scroll = QScrollArea()
        self.modules_scroll.setWidgetResizable(True)
        self.modules_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.modules_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Create a container widget for the modules
        self.modules_container = QWidget()
        self.modules_layout = QVBoxLayout(self.modules_container)
        self.modules_layout.setAlignment(Qt.AlignTop)
        
        # Initially empty - will be populated by add_module
        self.modules_scroll.setWidget(self.modules_container)
        
        # Add the scroll area to the main layout
        layout.addWidget(self.modules_scroll)

        # Create the circular add button
        self.add_module_button = QToolButton()
        self.add_module_button.setText("+")
        self.add_module_button.setFixedSize(50, 50)
        self.add_module_button.setStyleSheet("""
            QToolButton {
                background-color: #2a2b40;
                color: white;
                border-radius: 25px;
                font-size: 24px;
                font-weight: bold;
                border: 2px solid #5a5080;
            }
            QToolButton:hover {
                background-color: #3a3b50;
                border: 2px solid #7a70a0;
            }
            QToolButton:pressed {
                background-color: #4a4b60;
            }
        """)
        self.add_module_button.clicked.connect(self.show_add_module_menu)
        
        layout.addWidget(self.add_module_button)
        layout.setAlignment(self.add_module_button, Qt.AlignCenter)

        return panel

    def show_add_module_menu(self):
        """Show a menu to add new modules."""
        menu = QMenu(self)
        
        # Add sample module options
        real_sense_action = menu.addAction("RealSense Camera")
        real_sense_action.triggered.connect(lambda: self.add_module("RealSense Camera"))
        
        servo_action = menu.addAction("Servo Drives")
        servo_action.triggered.connect(lambda: self.add_module("Servo Drives"))
        
        pico_action = menu.addAction("RPi Pico")
        pico_action.triggered.connect(lambda: self.add_module("RPi Pico"))
        
        # Show the menu at the position of the add button
        pos = self.add_module_button.mapToGlobal(self.add_module_button.rect().bottomLeft())
        menu.exec(pos)
    
    def add_module(self, module_name):
        """Add a new module to the control panel."""
        # Create a new module panel
        module_panel = DevicePanel(module_name)
        
        # Create buttons for module control
        module_buttons_layout = QHBoxLayout()
        
        # Disable/enable button
        toggle_button = QPushButton("Disable")
        toggle_button.setStyleSheet("""
            QPushButton {
                background: #1a1b2a;
                color: #c0b0ff;
                border: 1px solid #3a3550;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 9px;
            }
            QPushButton:hover { 
                background: #222335; 
                border-color: #5a5080; 
            }
        """)
        toggle_button.clicked.connect(lambda: self.toggle_module(module_name))
        
        # Remove button
        remove_button = QPushButton("Remove")
        remove_button.setStyleSheet("""
            QPushButton {
                background: #1a1b2a;
                color: #ff6b6b;
                border: 1px solid #3a3550;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 9px;
            }
            QPushButton:hover { 
                background: #222335; 
                border-color: #ff6b6b; 
            }
        """)
        remove_button.clicked.connect(lambda: self.remove_module(module_name))
        
        module_buttons_layout.addWidget(toggle_button)
        module_buttons_layout.addWidget(remove_button)
        module_buttons_layout.addStretch()
        
        # Create the module layout
        module_layout = QVBoxLayout()
        module_layout.addWidget(module_panel)
        module_layout.addLayout(module_buttons_layout)
        
        # Add to the modules container
        module_widget = QWidget()
        module_widget.setLayout(module_layout)
        self.modules_layout.addWidget(module_widget)
        
        # Store references
        self.modules[module_name] = {
            'panel': module_panel,
            'enabled': True,
            'toggle_button': toggle_button,
            'remove_button': remove_button
        }
        self.module_widgets[module_name] = module_widget
        
        # Initialize the module based on its type
        self.initialize_module(module_name)
    
    def initialize_module(self, module_name):
        """Initialize specific module functionality."""
        if module_name == "RealSense Camera":
            self.initialize_realsense_module(module_name)
        elif module_name == "Servo Drives":
            self.initialize_servo_module(module_name)
        elif module_name == "RPi Pico":
            self.initialize_pico_module(module_name)
    
    def initialize_realsense_module(self, module_name):
        """Initialize RealSense camera module."""
        module_info = self.modules[module_name]
        panel = module_info['panel']
        
        # Add RealSense-specific controls
        realsense_layout = QVBoxLayout()
        status_label = panel.status_label
        realsense_layout.addWidget(status_label)
        
        # Resolution selection
        resolution_layout = self.create_resolution_control()
        realsense_layout.addLayout(resolution_layout)
        
        # FPS selection
        fps_layout = self.create_fps_control()
        realsense_layout.addLayout(fps_layout)
        
        # Stream control buttons
        start_button = QPushButton("Start Stream")
        stop_button = QPushButton("Stop Stream")
        stop_button.setEnabled(False)
        start_button.clicked.connect(self.start_realsense)
        stop_button.clicked.connect(self.stop_realsense)
        
        self.btn_rs_start = start_button
        self.btn_rs_stop = stop_button
        
        realsense_layout.addWidget(start_button)
        realsense_layout.addWidget(stop_button)
        panel.setLayout(realsense_layout)
        
        # Detect RealSense
        if REAL_SENSE_AVAILABLE:
            realsense_success, realsense_message = detect_realsense()
            realsense_color = "#6bff9b" if realsense_success else ("#ff6b6b" if "missing" in realsense_message else "#ffaa6b")
            panel.set_status(realsense_message, realsense_color)
        else:
            panel.set_status("Not available", "#ff6b6b")
    
    def initialize_servo_module(self, module_name):
        """Initialize servo drives module."""
        module_info = self.modules[module_name]
        panel = module_info['panel']
        
        servo_layout = QVBoxLayout()
        servo_layout.addWidget(panel.status_label)
        init_button = QPushButton("Initialize")
        init_button.clicked.connect(lambda: self.servo_initialize(module_name))
        servo_layout.addWidget(init_button)
        panel.setLayout(servo_layout)
        
        panel.set_status("Unknown", "#ffaa6b")
    
    def initialize_pico_module(self, module_name):
        """Initialize RPi Pico module."""
        module_info = self.modules[module_name]
        panel = module_info['panel']
        
        pico_layout = QVBoxLayout()
        self.pico_status = panel.status_label
        pico_layout.addWidget(self.pico_status)
        
        connect_button = QPushButton("Connect")
        connect_button.clicked.connect(self.connect_pico)
        pico_layout.addWidget(connect_button)
        
        self.btn_pico_connect = connect_button
        panel.setLayout(pico_layout)
        
        panel.set_status("Disconnected", "#ffaa6b")
    
    def servo_initialize(self, module_name):
        """Placeholder for servo initialization."""
        self.modules[module_name]['panel'].set_status("Initialized", "#6bff9b")
        logging.info(f"Servo module {module_name} initialized")
    
    def toggle_module(self, module_name):
        """Toggle module enabled/disabled state."""
        module_info = self.modules[module_name]
        if module_info['enabled']:
            # Disable the module
            module_info['toggle_button'].setText("Enable")
            module_info['panel'].setStyleSheet("""
                QGroupBox {
                    font-weight: bold;
                    color: #555555;
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
            module_info['panel'].set_status("Disabled", "#555555")
            module_info['enabled'] = False
            
            # Disable any controls in the module
            for i in range(module_info['panel'].layout().count()):
                widget = module_info['panel'].layout().itemAt(i).widget()
                if widget and hasattr(widget, 'setEnabled'):
                    widget.setEnabled(False)
        else:
            # Enable the module
            module_info['toggle_button'].setText("Disable")
            module_info['panel'].setStyleSheet("""
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
            if module_name == "RealSense Camera":
                if REAL_SENSE_AVAILABLE:
                    realsense_success, realsense_message = detect_realsense()
                    realsense_color = "#6bff9b" if realsense_success else ("#ff6b6b" if "missing" in realsense_message else "#ffaa6b")
                    module_info['panel'].set_status(realsense_message, realsense_color)
                else:
                    module_info['panel'].set_status("Not available", "#ff6b6b")
            elif module_name == "Servo Drives":
                module_info['panel'].set_status("Unknown", "#ffaa6b")
            elif module_name == "RPi Pico":
                module_info['panel'].set_status("Disconnected", "#ffaa6b")
            
            module_info['enabled'] = True
            
            # Enable any controls in the module
            for i in range(module_info['panel'].layout().count()):
                widget = module_info['panel'].layout().itemAt(i).widget()
                if widget and hasattr(widget, 'setEnabled'):
                    widget.setEnabled(True)
    
    def remove_module(self, module_name):
        """Remove a module from the control panel."""
        # Remove from layout
        module_widget = self.module_widgets[module_name]
        self.modules_layout.removeWidget(module_widget)
        module_widget.deleteLater()
        
        # Remove from dictionaries
        del self.modules[module_name]
        del self.module_widgets[module_name]
        
        logging.info(f"Module {module_name} removed")

    def create_resolution_control(self):
        """Create resolution selection controls."""
        resolution_layout = QHBoxLayout()
        resolution_layout.addWidget(QLabel("Resolution:"))
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems(["640x480", "1280x720", "1920x1080"])
        resolution_layout.addWidget(self.resolution_combo)
        return resolution_layout

    def create_fps_control(self):
        """Create FPS selection controls."""
        fps_layout = QHBoxLayout()
        fps_layout.addWidget(QLabel("FPS:"))
        self.fps_combo = QComboBox()
        self.fps_combo.addItems(["15", "30", "60"])
        fps_layout.addWidget(self.fps_combo)
        return fps_layout

    def detect_devices(self):
        """Detect connected devices and update their status if RealSense module exists."""
        if "RealSense Camera" in self.modules:
            if REAL_SENSE_AVAILABLE:
                realsense_success, realsense_message = detect_realsense()
                realsense_color = "#6bff9b" if realsense_success else ("#ff6b6b" if "missing" in realsense_message else "#ffaa6b")
                self.modules["RealSense Camera"]['panel'].set_status(realsense_message, realsense_color)
            else:
                self.modules["RealSense Camera"]['panel'].set_status("Not available", "#ff6b6b")

        # Update servo and pico statuses if modules exist
        if "Servo Drives" in self.modules:
            self.modules["Servo Drives"]['panel'].set_status("Unknown", "#ffaa6b")
        
        if "RPi Pico" in self.modules:
            self.modules["RPi Pico"]['panel'].set_status("Disconnected", "#ffaa6b")

    def create_tabs(self):
        """Create the tabbed interface with camera, charts, and AI tabs."""
        tabs = QTabWidget()

        camera_tab = self.create_camera_tab()
        tabs.addTab(camera_tab, "Camera")

        for tab_name in ["Charts", "AI"]:
            empty_tab = self.create_empty_tab()
            tabs.addTab(empty_tab, tab_name)

        return tabs

    def create_camera_tab(self):
        """Create the camera tab with RGB and depth stream displays."""
        camera_tab = QWidget()
        camera_layout = QVBoxLayout(camera_tab)
        
        # Create RGB video display
        self.video_label_rgb = QLabel("RGB Stream")
        self.video_label_rgb.setAlignment(Qt.AlignCenter)
        self.video_label_rgb.setStyleSheet("background: #000; color: #a0b0ff; font-size: 14px;")
        self.video_label_rgb.setMinimumSize(640, 360)
        self.video_label_rgb.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Create depth video display
        self.video_label_depth = QLabel("Depth Stream")
        self.video_label_depth.setAlignment(Qt.AlignCenter)
        self.video_label_depth.setStyleSheet("background: #000; color: #c0a0ff; font-size: 14px;")
        self.video_label_depth.setMinimumSize(640, 360)
        self.video_label_depth.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        camera_layout.addWidget(self.video_label_rgb)
        camera_layout.addWidget(self.video_label_depth)
        return camera_tab

    def create_empty_tab(self):
        """Create an empty tab with placeholder text."""
        tab = QWidget()
        tab.setLayout(QVBoxLayout())
        tab.layout().addWidget(QLabel("Nothing here yet...."))
        return tab

    def create_console(self):
        """Create the system console with log display and command input."""
        panel = QFrame()
        layout = QVBoxLayout(panel)
        layout.addWidget(QLabel("System Console", alignment=Qt.AlignCenter))
        
        self.log_text = QPlainTextEdit(readOnly=True, maximumBlockCount=1000)
        layout.addWidget(self.log_text)

        self.cmd_input = QTextEdit(maximumHeight=50, placeholderText="command >")
        execute_button = QPushButton("Execute", clicked=self.send_command)
        layout.addWidget(self.cmd_input)
        layout.addWidget(execute_button)
        return panel

    def send_command(self):
        """Execute a command from the command input field."""
        command_text = self.cmd_input.toPlainText().strip()
        if command_text:
            logging.info(f"cmd: {command_text}")
            self.cmd_input.clear()

    def start_realsense(self):
        """Start the RealSense camera stream."""
        if not REAL_SENSE_AVAILABLE:
            logging.error("Cannot start: pyrealsense2 not installed")
            return

        try:
            width, height = map(int, self.resolution_combo.currentText().split("x"))
            fps = int(self.fps_combo.currentText())

            self.pipeline = rs.pipeline()
            config = rs.config()
            config.enable_stream(rs.stream.color, width, height, rs.format.rgb8, fps)
            config.enable_stream(rs.stream.depth, width, height, rs.format.z16, fps)
            self.pipeline.start(config)

            self.timer = QTimer()
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(int(1000 / fps))

            self.realsense_panel.set_status("Streaming", "#6bff9b")
            self.btn_rs_start.setEnabled(False)
            self.btn_rs_stop.setEnabled(True)
            logging.info(f"RealSense stream started @ {width}x{height} @ {fps} FPS")

        except Exception as e:
            self.realsense_panel.set_status("Start failed", "#ff6b6b")
            logging.error(f"Failed to start stream: {e}")

    def stop_realsense(self):
        """Stop the RealSense camera stream."""
        if self.timer:
            self.timer.stop()
        if self.pipeline:
            self.pipeline.stop()
            self.pipeline = None
        self.realsense_panel.set_status("Stopped", "#ffaa6b")
        self.btn_rs_start.setEnabled(True)
        self.btn_rs_stop.setEnabled(False)
        logging.info("RealSense stream stopped")

    def update_frame(self):
        """Update the camera frames in the display."""
        if not self.pipeline:
            return

        try:
            frames = self.pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()

            if color_frame:
                self.update_rgb_frame(color_frame)

            if depth_frame:
                self.update_depth_frame(depth_frame)

        except Exception as e:
            logging.error(f"frame error: {e}")

    def update_rgb_frame(self, color_frame):
        """Update the RGB frame in the display."""
        rgb_image = np.asanyarray(color_frame.get_data())
        height, width, channels = rgb_image.shape
        qt_image = QImage(rgb_image.data, width, height, channels * width, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image).scaled(
            self.video_label_rgb.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.video_label_rgb.setPixmap(pixmap)

    def update_depth_frame(self, depth_frame):
        """Update the depth frame in the display."""
        depth_image = np.asanyarray(depth_frame.get_data())
        depth_colormap = normalize_depth_for_display(depth_image)
        height, width = depth_colormap.shape
        qt_image = QImage(depth_colormap.data, width, height, width, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(qt_image).scaled(
            self.video_label_depth.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.video_label_depth.setPixmap(pixmap)

    def save_configuration(self):
        """Save the current configuration to file."""
        resolution = self.resolution_combo.currentText()
        fps = int(self.fps_combo.currentText())
        
        if save_config(resolution, fps):
            logging.info("Configuration saved")
        else:
            logging.error("Failed to save configuration")

    def load_configuration(self):
        """Load configuration from file and update UI."""
        self.config = load_config()
        self.resolution_combo.setCurrentText(self.config.get("resolution", "1280x720"))
        self.fps_combo.setCurrentText(str(self.config.get("fps", 30)))
        logging.info("Configuration loaded")

    def closeEvent(self, event):
        """Handle application shutdown."""
        self.stop_realsense()
        logging.info("system shutdown")
        event.accept()
