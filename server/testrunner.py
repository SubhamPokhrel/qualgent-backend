# test_runner.py
import importlib.util
import sys
import traceback

def execute_appwright_test(driver, test_path):
    """Execute AppWright test script with the given driver"""
    try:
        # Load test module dynamically
        spec = importlib.util.spec_from_file_location("test_module", test_path)
        test_module = importlib.util.module_from_spec(spec)
        
        # Add driver to module namespace
        test_module.driver = driver
        
        # Execute the module
        spec.loader.exec_module(test_module)
        
        # Try to call main test function
        if hasattr(test_module, 'run_test'):
            result = test_module.run_test(driver)
        elif hasattr(test_module, 'test_main'):
            result = test_module.test_main(driver)
        else:
            # If no specific function, assume module execution was the test
            result = {"passed": True, "message": "Test executed successfully"}
        
        return result
        
    except Exception as e:
        return {
            "passed": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }