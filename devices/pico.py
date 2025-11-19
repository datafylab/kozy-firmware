# devices/pico.py
import serial
import serial.tools.list_ports
import time
import logging

def find_pico_port():
    """Find the port to which the Pico is connected (by VID/PID or name)."""
    # VID/PID for Raspberry Pi Pico in MicroPython mode
    PICO_VID = 0x2E8A  # Raspberry Pi
    PICO_PID = 0x0005  # MicroPython CDC

    ports = serial.tools.list_ports.comports()
    for port in ports:
        if port.vid == PICO_VID and port.pid == PICO_PID:
            return port.device
    return None

def connect_to_pico(timeout=3):
    """Connect to the Pico and request its identification code."""
    pico_port = find_pico_port()
    if not pico_port:
        logging.warning("Pico not found")
        return None

    try:
        with serial.Serial(pico_port, baudrate=115200, timeout=1) as serial_connection:
            logging.info(f"Connected to Pico on {pico_port}")
            # Send command
            serial_connection.write(b"GET_CODE\n")
            serial_connection.flush()

            # Wait for response up to timeout
            start_time = time.time()
            while time.time() - start_time < timeout:
                line = serial_connection.readline().decode('utf-8', errors='ignore').strip()
                if line.startswith("CODE:"):
                    code = line[5:]
                    logging.info(f"Received code from Pico: {code}")
                    return code
                elif line:  # Log only non-empty "garbage" strings
                    logging.warning(f"Unexpected data from Pico: {line}")

            logging.warning("Pico did not respond with CODE in time")
            return None

    except Exception as e:
        logging.error(f"Failed to communicate with Pico: {e}")
        return None
