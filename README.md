<div align="center">
  <img src="thumbnails/kozy-firmware-logo.png" alt="Logo" width="100" height="100"/>
  <h3 align="center">BlenderKit</h3>

  Control firmware and software for Kozy-xx
  
  ![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/datafylab/kozy-firmware/total?color=blue)
  [![GitHub Release](https://img.shields.io/github/v/release/datafylab/kozy-firmware?color=green)](https://github.com/datafylab/kozy-firmware/releases/latest)
  [![Project license](https://img.shields.io/github/license/datafylab/kozy-firmware.svg?color=orange)](LICENSE)
  </br>
  ![GitHub commit activity](https://img.shields.io/github/commit-activity/y/datafylab/kozy-firmware?color=blue)
  ![GitHub branch check runs](https://img.shields.io/github/check-runs/datafylab/kozy-firmware/main?color=green)

</div>

## Description

Control firmware and software for Kozy-xx

It helps synchronize cameras, microcontrollers, and AI models into a single system for robotics...
> But it's not universal yet and only works with RealSense and RPI Pico.

Of course, first of all, this is created for personal projects.
> It's supposed to be a simple replacement for ROS, with various elements to make it easier to configure and modify devices, graphs, etc. But it's still in an incredibly early stage of development, and I don't think anything great will come out of it.

## System requirements
- **OS**: Linux (Ubuntu/Arch/Fedora/etc.) or Windows
- **Python**: 3.11.13 (other 3.11.x versions may work)
- **Display**: Any screen to access the `Kozy-Control-Panel` GUI

## Quick Start!
1. Сlone the repository::
   ```bash
   git clone https://github.com/datafylab/kozy-firmware.git
   cd kozy-firmware
   pip install -r requirements.txt

2. Launch it!
   ```bash
   python main.py

   Or build it!
   ```bash
   pyinstaller --onefile main.py

[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/datafylab)
