# devices/pico.py
import serial
import serial.tools.list_ports
import time
import logging

def find_pico_port():
    """Ищет порт, к которому подключена Pico (по VID/PID или имени)"""
    # VID/PID для Raspberry Pi Pico в режиме MicroPython
    PICO_VID = 0x2E8A  # Raspberry Pi
    PICO_PID = 0x0005  # MicroPython CDC

    ports = serial.tools.list_ports.comports()
    for port in ports:
        if port.vid == PICO_VID and port.pid == PICO_PID:
            return port.device
    return None

def connect_to_pico(timeout=3):
    """Подключается к Pico и запрашивает код по команде"""
    port = find_pico_port()
    if not port:
        logging.warning("Pico not found")
        return None

    try:
        with serial.Serial(port, baudrate=115200, timeout=1) as ser:
            logging.info(f"Connected to Pico on {port}")
            # Отправляем команду
            ser.write(b"GET_CODE\n")
            ser.flush()

            # Ждём ответ до таймаута
            start = time.time()
            while time.time() - start < timeout:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line.startswith("CODE:"):
                    code = line[5:]
                    logging.info(f"Received code from Pico: {code}")
                    return code
                elif line:  # Логируем только непустые "мусорные" строки
                    logging.warning(f"Unexpected data from Pico: {line}")

            logging.warning("Pico did not respond with CODE in time")
            return None

    except Exception as e:
        logging.error(f"Failed to communicate with Pico: {e}")
        return None
