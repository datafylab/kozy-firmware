#!/usr/bin/env python3
# Test script to verify the GUI changes work correctly

import sys
import importlib.util

def test_imports():
    """Test that all modules can be imported without errors."""
    try:
        # Test importing main window
        spec = importlib.util.spec_from_file_location("main_window", "/workspace/gui/main_window.py")
        main_window_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(main_window_module)
        print("✓ Successfully imported main_window module")
        
        # Test importing dialogs
        spec = importlib.util.spec_from_file_location("dialogs", "/workspace/gui/dialogs.py")
        dialogs_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(dialogs_module)
        print("✓ Successfully imported dialogs module")
        
        # Test importing styles
        spec = importlib.util.spec_from_file_location("styles", "/workspace/gui/styles.py")
        styles_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(styles_module)
        print("✓ Successfully imported styles module")
        
        return True
    except Exception as e:
        print(f"✗ Error importing modules: {e}")
        return False

def test_theme_functions():
    """Test that theme functions exist in styles module."""
    try:
        from gui.styles import get_raw_cyber_stylesheet, get_dark_stylesheet, get_light_stylesheet
        
        raw_cyber = get_raw_cyber_stylesheet()
        dark = get_dark_stylesheet()
        light = get_light_stylesheet()
        
        if raw_cyber and dark and light:
            print("✓ All theme functions work correctly")
            return True
        else:
            print("✗ Theme functions returned None or empty strings")
            return False
    except Exception as e:
        print(f"✗ Error testing theme functions: {e}")
        return False

def test_settings_dialog():
    """Test that SettingsDialog class exists."""
    try:
        from gui.dialogs import SettingsDialog, AboutDialog
        
        # Check that both classes exist
        if SettingsDialog and AboutDialog:
            print("✓ SettingsDialog and AboutDialog classes exist")
            return True
        else:
            print("✗ SettingsDialog or AboutDialog classes missing")
            return False
    except Exception as e:
        print(f"✗ Error testing dialog classes: {e}")
        return False

def main():
    """Run all tests."""
    print("Testing GUI changes...")
    print("="*50)
    
    tests = [
        ("Module imports", test_imports),
        ("Theme functions", test_theme_functions),
        ("Dialog classes", test_settings_dialog),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "="*50)
    print("Test Results:")
    all_passed = True
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  {test_name}: {status}")
        if not result:
            all_passed = False
    
    print(f"\nOverall: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)