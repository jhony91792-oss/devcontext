# Compat module for DevContext - Python compatibility utilities

import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional


def get_python_version() -> tuple:
    """Get Python version as tuple."""
    return sys.version_info[:2]


def get_cache_dir() -> Path:
    """Get cache directory."""
    if sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Caches"
    else:
        base = Path.home() / ".cache"
    
    return base / "devcontext"


def get_config_dir() -> Path:
    """Get config directory."""
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path.home() / ".config"
    
    return base / "devcontext"


def ensure_dir(path: Path) -> Path:
    """Ensure directory exists."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_system_info() -> Dict[str, Any]:
    """Get system information."""
    return {
        "platform": sys.platform,
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}",
        "cache_dir": str(get_cache_dir()),
        "config_dir": str(get_config_dir()),
    }


# CLI
def main():
    import argparse
    parser = argparse.ArgumentParser(description="DevContext system info")
    
    args = parser.parse_args()
    
    info = get_system_info()
    print("System Information:")
    for key, value in info.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()