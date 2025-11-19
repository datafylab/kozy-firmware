# devices/realsense.py
import logging
import numpy as np

try:
    import pyrealsense2 as rs
    REAL_SENSE_AVAILABLE = True
except ImportError:
    REAL_SENSE_AVAILABLE = False
    rs = None

def detect_realsense():
    """Detect if a RealSense camera is connected."""
    if not REAL_SENSE_AVAILABLE:
        return False, "Driver missing"

    try:
        context = rs.context()
        devices = context.query_devices()
        if devices:
            device = devices[0]
            name = device.get_info(rs.camera_info.name)
            serial = device.get_info(rs.camera_info.serial_number)
            return True, f"Connected ({serial})"
        else:
            return False, "Not found"
    except Exception as e:
        logging.error(f"RealSense detection error: {e}")
        return False, "Detection error"

def normalize_depth_for_display(depth_array, max_distance_mm=3000):
    """Normalize depth values for display purposes."""
    depth_clipped = np.clip(depth_array, 0, max_distance_mm)
    depth_normalized = (depth_clipped.astype(np.float32) / max_distance_mm) * 255.0
    return depth_normalized.astype(np.uint8)
