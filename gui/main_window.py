# gui/main_window.py
import sys
import logging
import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QTabWidget, QLabel, QTextEdit, QPushButton, QSplitter, QFrame,
    QPlainTextEdit, QSizePolicy, QGroupBox, QComboBox, QMenuBar, QMenu
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPixmap, QIcon

# Импорты наших модулей
from gui.styles import get_raw_cyber_stylesheet
from gui.panels import DevicePanel
from gui.dialogs import AboutDialog
from utils.logger import setup_logger
from config import load_config, save_config
from devices.realsense import REAL_SENSE_AVAILABLE, rs, detect_realsense, normalize_depth_for_display

if REAL_SENSE_AVAILABLE:
    import numpy as np


class RobotGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initialize_window()
        self.create_widgets()
        self.setup_layout()
        self.setup_logging()
        self.initialize_devices()
    
    def initialize_window(self):
        """Initialize the main window properties."""
        self.setWindowTitle("Kozy Control Panel")
        self.resize(1500, 900)
        self.setStyleSheet(get_raw_cyber_stylesheet())
        self.config = load_config()
        self.setup_menu()
        
        # Initialize RealSense variables
        self.pipeline = None
        self.timer = None
    
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
        program_menu.addAction("Settings", self.open_about)

    def open_about(self):
        """Open the about dialog."""
        about_dialog = AboutDialog(self)
        about_dialog.exec()

    def create_control_panel(self):
        """Create the control panel with device controls."""
        panel = QFrame()
        layout = QVBoxLayout(panel)
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignTop)

        # Add title
        title = QLabel("MODULE CONTROL")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-weight: bold; color: #b8a0ff; margin-bottom: 8px;")
        layout.addWidget(title)

        # Create device panels
        self.create_realsense_panel(layout)
        self.create_servo_panel(layout)
        self.create_pico_panel(layout)

        layout.addStretch()
        return panel

    def create_realsense_panel(self, parent_layout):
        """Create the RealSense camera control panel."""
        self.realsense_panel = DevicePanel("RealSense D415")
        realsense_layout = QVBoxLayout()
        self.realsense_status = self.realsense_panel.status_label
        realsense_layout.addWidget(self.realsense_status)

        # Resolution selection
        resolution_layout = self.create_resolution_control()
        realsense_layout.addLayout(resolution_layout)

        # FPS selection
        fps_layout = self.create_fps_control()
        realsense_layout.addLayout(fps_layout)

        # Load saved configuration
        saved_res = self.config.get("resolution", "1280x720")
        saved_fps = str(self.config.get("fps", 30))
        self.resolution_combo.setCurrentText(saved_res)
        self.fps_combo.setCurrentText(saved_fps)

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
        self.realsense_panel.setLayout(realsense_layout)
        parent_layout.addWidget(self.realsense_panel)

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

    def create_servo_panel(self, parent_layout):
        """Create the servo drives control panel."""
        self.servo_panel = DevicePanel("Servo Drives")
        servo_layout = QVBoxLayout()
        servo_layout.addWidget(self.servo_panel.status_label)
        servo_layout.addWidget(QPushButton("Initialize"))
        self.servo_panel.setLayout(servo_layout)
        parent_layout.addWidget(self.servo_panel)

    def create_pico_panel(self, parent_layout):
        """Create the Raspberry Pi Pico control panel."""
        self.pico_panel = DevicePanel("RPi Pico")
        pico_layout = QVBoxLayout()
        self.pico_status = self.pico_panel.status_label
        pico_layout.addWidget(self.pico_status)

        connect_button = QPushButton("Connect")
        connect_button.clicked.connect(self.connect_pico)
        pico_layout.addWidget(connect_button)

        self.btn_pico_connect = connect_button
        self.pico_panel.setLayout(pico_layout)
        parent_layout.addWidget(self.pico_panel)

    def detect_devices(self):
        """Detect connected devices and update their status."""
        realsense_success, realsense_message = detect_realsense()
        realsense_color = "#6bff9b" if realsense_success else ("#ff6b6b" if "missing" in realsense_message else "#ffaa6b")
        self.realsense_panel.set_status(realsense_message, realsense_color)

        self.servo_panel.set_status("Unknown", "#ffaa6b")
        self.pico_panel.set_status("Disconnected", "#ffaa6b")

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
