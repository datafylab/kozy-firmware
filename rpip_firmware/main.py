# main.py
import random
import sys

def generate_code():
    return ''.join(str(random.randint(0, 9)) for _ in range(6))

while True:
    try:
        line = sys.stdin.readline().strip()
        if line == "GET_CODE":
            code = generate_code()
            print(f"CODE:{code}")
    except Exception as e:
        pass