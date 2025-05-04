import platform
import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

def import_recorder():
    """
    Import the appropriate recorder module based on the platform.
    
    Returns:
        The recorder module for the current platform
    """
    system = platform.system().lower()
    
    if system == "darwin":  # macOS
        from .mac_recorder import MacRecorder
        return MacRecorder()
    elif system == "windows":
        from .windows_recorder import WindowsRecorder
        return WindowsRecorder()
    elif system == "linux":
        from .linux_recorder import LinuxRecorder
        return LinuxRecorder()
    else:
        raise ImportError(f"Unsupported platform: {system}")
