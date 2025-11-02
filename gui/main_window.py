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
        self.setWindowTitle("Kozy Control Panel")
        self.resize(1500, 900)
        self.setStyleSheet(get_raw_cyber_stylesheet())

        self.config = load_config()
        self.setup_menu()

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)

        self.control_panel = self.create_control_panel()
        self.tabs = self.create_tabs()
        self.console = self.create_console()

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.control_panel)
        splitter.addWidget(self.tabs)
        splitter.addWidget(self.console)
        splitter.setSizes([340, 900, 300])
        main_layout.addWidget(splitter)

        setup_logger(self.log_text)
        self.pipeline = None
        self.timer = None

        self.detect_devices()
        QTimer.singleShot(100, self.auto_connect_pico)

    def auto_connect_pico(self):
        logging.info("Auto-connecting to Pico...")
        self.connect_pico()

    def connect_pico(self):
        from devices.pico import connect_to_pico
        self.btn_pico_connect.setEnabled(False)
        self.pico_panel.set_status("Connecting...", "#ffaa6b")

        code = connect_to_pico()

        if code:
            self.pico_panel.set_status(f"Code: {code}", "#6bff9b")
            logging.info(f"Pico connected! Code: {code}")
        else:
            self.pico_panel.set_status("Failed", "#ff6b6b")

        self.btn_pico_connect.setEnabled(True)

    def setup_menu(self):
        menubar = self.menuBar()
        menubar.setStyleSheet("background: #0c0d15; color: #c0b0ff;")
        file_menu = menubar.addMenu("File")
        file_menu.addAction("Save Configuration", self.save_configuration)
        file_menu.addAction("Load Configuration", self.load_configuration)
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)

        program_menu = menubar.addMenu("Program")
        program_menu.addAction("Settings", self.open_about)

    def open_about(self):
        dialog = AboutDialog(self)
        dialog.exec()

    def create_control_panel(self):
        panel = QFrame()
        layout = QVBoxLayout(panel)
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignTop)

        title = QLabel("DEVICE CONTROL")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-weight: bold; color: #b8a0ff; margin-bottom: 8px;")
        layout.addWidget(title)

        self.realsense_panel = DevicePanel("RealSense D415")
        realsense_layout = QVBoxLayout()
        self.realsense_status = self.realsense_panel.status_label
        realsense_layout.addWidget(self.realsense_status)

        res_layout = QHBoxLayout()
        res_layout.addWidget(QLabel("Resolution:"))
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems(["640x480", "1280x720", "1920x1080"])
        res_layout.addWidget(self.resolution_combo)
        realsense_layout.addLayout(res_layout)

        fps_layout = QHBoxLayout()
        fps_layout.addWidget(QLabel("FPS:"))
        self.fps_combo = QComboBox()
        self.fps_combo.addItems(["15", "30", "60"])
        fps_layout.addWidget(self.fps_combo)
        realsense_layout.addLayout(fps_layout)

        saved_res = self.config.get("resolution", "1280x720")
        saved_fps = str(self.config.get("fps", 30))
        self.resolution_combo.setCurrentText(saved_res)
        self.fps_combo.setCurrentText(saved_fps)

        self.btn_rs_start = QPushButton("Start Stream")
        self.btn_rs_stop = QPushButton("Stop Stream")
        self.btn_rs_stop.setEnabled(False)
        self.btn_rs_start.clicked.connect(self.start_realsense)
        self.btn_rs_stop.clicked.connect(self.stop_realsense)

        realsense_layout.addWidget(self.btn_rs_start)
        realsense_layout.addWidget(self.btn_rs_stop)
        self.realsense_panel.setLayout(realsense_layout)
        layout.addWidget(self.realsense_panel)

        # Другие панели
        self.servo_panel = DevicePanel("Servo Drives")
        servo_layout = QVBoxLayout()
        servo_layout.addWidget(self.servo_panel.status_label)
        servo_layout.addWidget(QPushButton("Initialize"))
        self.servo_panel.setLayout(servo_layout)
        layout.addWidget(self.servo_panel)

        self.pico_panel = DevicePanel("RPi Pico")
        pico_layout = QVBoxLayout()
        self.pico_status = self.pico_panel.status_label
        pico_layout.addWidget(self.pico_status)

        self.btn_pico_connect = QPushButton("Connect")
        self.btn_pico_connect.clicked.connect(self.connect_pico)
        pico_layout.addWidget(self.btn_pico_connect)

        self.pico_panel.setLayout(pico_layout)
        layout.addWidget(self.pico_panel)

        layout.addStretch()
        return panel

    def detect_devices(self):
        success, msg = detect_realsense()
        color = "#6bff9b" if success else ("#ff6b6b" if "missing" in msg else "#ffaa6b")
        self.realsense_panel.set_status(msg, color)

        self.servo_panel.set_status("Unknown", "#ffaa6b")
        self.pico_panel.set_status("Disconnected", "#ffaa6b")

    def create_tabs(self):
        tabs = QTabWidget()

        cam_tab = QWidget()
        cam_layout = QVBoxLayout(cam_tab)
        self.video_label_rgb = QLabel("RGB Stream")
        self.video_label_rgb.setAlignment(Qt.AlignCenter)
        self.video_label_rgb.setStyleSheet("background: #000; color: #a0b0ff; font-size: 14px;")
        self.video_label_rgb.setMinimumSize(640, 360)
        self.video_label_rgb.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.video_label_depth = QLabel("Depth Stream")
        self.video_label_depth.setAlignment(Qt.AlignCenter)
        self.video_label_depth.setStyleSheet("background: #000; color: #c0a0ff; font-size: 14px;")
        self.video_label_depth.setMinimumSize(640, 360)
        self.video_label_depth.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        cam_layout.addWidget(self.video_label_rgb)
        cam_layout.addWidget(self.video_label_depth)
        tabs.addTab(cam_tab, "Camera")

        for name in ["Charts", "AI"]:
            tab = QWidget()
            tab.setLayout(QVBoxLayout())
            tab.layout().addWidget(QLabel("Nothing here yet...."))
            tabs.addTab(tab, name)

        return tabs

    def create_console(self):
        panel = QFrame()
        layout = QVBoxLayout(panel)
        layout.addWidget(QLabel("System Console", alignment=Qt.AlignCenter))
        self.log_text = QPlainTextEdit(readOnly=True, maximumBlockCount=1000)
        layout.addWidget(self.log_text)

        self.cmd_input = QTextEdit(maximumHeight=50, placeholderText="command >")
        layout.addWidget(self.cmd_input)
        layout.addWidget(QPushButton("Execute", clicked=self.send_command))
        return panel

    def send_command(self):
        cmd = self.cmd_input.toPlainText().strip()
        if cmd:
            logging.info(f"cmd: {cmd}")
            self.cmd_input.clear()

    def start_realsense(self):
        if not REAL_SENSE_AVAILABLE:
            logging.error("Cannot start: pyrealsense2 not installed")
            return

        try:
            w, h = map(int, self.resolution_combo.currentText().split("x"))
            fps = int(self.fps_combo.currentText())

            self.pipeline = rs.pipeline()
            config = rs.config()
            config.enable_stream(rs.stream.color, w, h, rs.format.rgb8, fps)
            config.enable_stream(rs.stream.depth, w, h, rs.format.z16, fps)
            self.pipeline.start(config)

            self.timer = QTimer()
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(int(1000 / fps))

            self.realsense_panel.set_status("Streaming", "#6bff9b")
            self.btn_rs_start.setEnabled(False)
            self.btn_rs_stop.setEnabled(True)
            logging.info(f"RealSense stream started @ {w}x{h} @ {fps} FPS")

        except Exception as e:
            self.realsense_panel.set_status("Start failed", "#ff6b6b")
            logging.error(f"Failed to start stream: {e}")

    def stop_realsense(self):
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
        if not self.pipeline:
            return

        try:
            frames = self.pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()

            if color_frame:
                img_rgb = np.asanyarray(color_frame.get_data())
                h, w, ch = img_rgb.shape
                qt_img_rgb = QImage(img_rgb.data, w, h, ch * w, QImage.Format_RGB888)
                pixmap_rgb = QPixmap.fromImage(qt_img_rgb).scaled(
                    self.video_label_rgb.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.video_label_rgb.setPixmap(pixmap_rgb)

            if depth_frame:
                depth_image = np.asanyarray(depth_frame.get_data())
                depth_colormap = normalize_depth_for_display(depth_image)
                h, w = depth_colormap.shape
                qt_img_depth = QImage(depth_colormap.data, w, h, w, QImage.Format_Grayscale8)
                pixmap_depth = QPixmap.fromImage(qt_img_depth).scaled(
                    self.video_label_depth.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.video_label_depth.setPixmap(pixmap_depth)

        except Exception as e:
            logging.error(f"frame error: {e}")

    def save_configuration(self):
        if save_config(self.resolution_combo.currentText(), int(self.fps_combo.currentText())):
            logging.info("Configuration saved")
        else:
            logging.error("Failed to save configuration")

    def load_configuration(self):
        self.config = load_config()
        self.resolution_combo.setCurrentText(self.config.get("resolution", "1280x720"))
        self.fps_combo.setCurrentText(str(self.config.get("fps", 30)))
        logging.info("Configuration loaded")

    def closeEvent(self, event):
        self.stop_realsense()
        logging.info("system shutdown")
        event.accept()
