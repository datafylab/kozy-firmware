#!/usr/bin/env python3
"""
Тестовый скрипт для проверки исправлений в GUI
"""
import sys
import os
sys.path.append('/workspace')

def test_imports():
    """Тестируем импорты для проверки корректности изменений"""
    try:
        from gui.main_window import RobotGUI
        print("✓ Импорт RobotGUI успешен")
    except Exception as e:
        print(f"✗ Ошибка импорта RobotGUI: {e}")
        return False
    
    try:
        from gui.panels import DevicePanel
        print("✓ Импорт DevicePanel успешен")
    except Exception as e:
        print(f"✗ Ошибка импорта DevicePanel: {e}")
        return False
    
    return True

def test_main_window_structure():
    """Проверяем структуру основного окна"""
    try:
        from gui.main_window import RobotGUI
        import inspect
        
        # Проверяем наличие ключевых методов
        methods_to_check = [
            'initialize_realsense_module',
            'remove_module', 
            'start_realsense',
            'stop_realsense'
        ]
        
        robot_gui = RobotGUI.__dict__
        
        for method in methods_to_check:
            if method in robot_gui:
                print(f"✓ Метод {method} найден")
            else:
                print(f"✗ Метод {method} не найден")
                return False
                
        return True
    except Exception as e:
        print(f"✗ Ошибка при проверке структуры: {e}")
        return False

if __name__ == "__main__":
    print("Тестирование исправлений в GUI...")
    print()
    
    success = True
    success &= test_imports()
    print()
    success &= test_main_window_structure()
    
    print()
    if success:
        print("✓ Все тесты пройдены успешно!")
    else:
        print("✗ Некоторые тесты не пройдены!")
        sys.exit(1)