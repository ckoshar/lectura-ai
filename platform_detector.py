import os
import sys
import platform
from error_handler import logger

def detect_platform():
    """
    Detect the current operating system platform.
    
    Returns:
        A string representing the platform: 'mac', 'windows', or 'linux'
    """
    system = platform.system().lower()
    
    if system == 'darwin':
        logger.info("Detected macOS platform")
        return 'mac'
    elif system == 'windows':
        logger.info("Detected Windows platform")
        return 'windows'
    elif system == 'linux':
        logger.info("Detected Linux platform")
        return 'linux'
    else:
        logger.warning(f"Unsupported platform detected: {system}")
        return 'unknown'

def get_recorder_module():
    """
    Get the appropriate recorder module for the current platform.
    
    Returns:
        The module name to import
    """
    current_platform = detect_platform()
    
    if current_platform == 'mac':
        return 'mac_recorder'
    elif current_platform == 'windows':
        return 'windows_recorder'
    elif current_platform == 'linux':
        return 'linux_recorder'
    else:
        logger.error(f"Unsupported platform: {current_platform}")
        raise ImportError(f"Unsupported platform: {current_platform}")

def import_recorder():
    """
    Import the appropriate recorder module for the current platform.
    
    Returns:
        The imported recorder module
    """
    try:
        module_name = get_recorder_module()
        logger.info(f"Importing recorder module: {module_name}")
        
        # Dynamic import
        if module_name == 'mac_recorder':
            import mac_recorder
            return mac_recorder
        elif module_name == 'windows_recorder':
            import windows_recorder
            return windows_recorder
        elif module_name == 'linux_recorder':
            import linux_recorder
            return linux_recorder
        else:
            raise ImportError(f"Unknown recorder module: {module_name}")
    except ImportError as e:
        logger.error(f"Failed to import recorder module: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        recorder = import_recorder()
        print(f"✅ Successfully imported {get_recorder_module()} for {detect_platform()}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1) 