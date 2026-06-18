# Compatibility layer for DevContext

import sys
import os
from typing import Dict, Any, Optional

# Python version compatibility
PY38 = sys.version_info >= (3, 8)
PY39 = sys.version_info >= (3, 9)
PY310 = sys.version_info >= (3, 10)
PY311 = sys.version_info >= (3, 11)


def get_python_version() -> str:
    """Get Python version string."""
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


def is_frozen() -> bool:
    """Check if running as frozen executable (PyInstaller)."""
    return getattr(sys, 'frozen', False)


def get_platform() -> str:
    """Get platform string."""
    if sys.platform.startswith('linux'):
        return 'linux'
    elif sys.platform == 'darwin':
        return 'macos'
    elif sys.platform == 'win32':
        return 'windows'
    return 'unknown'


def get_home_config_dir() -> str:
    """Get home config directory for current platform."""
    if get_platform() == 'windows':
        base = os.environ.get('APPDATA', str(os.path.expanduser('~')))
        return os.path.join(base, 'DevContext')
    elif get_platform() == 'macos':
        base = os.environ.get('HOME', str(os.path.expanduser('~')))
        return os.path.join(base, 'Library', 'Application Support', 'DevContext')
    else:  # Linux
        xdg_config = os.environ.get('XDG_CONFIG_HOME', '')
        if xdg_config:
            return os.path.join(xdg_config, 'devcontext')
        return os.path.expanduser('~/.config/devcontext')


def get_cache_dir() -> str:
    """Get cache directory for current platform."""
    if get_platform() == 'windows':
        base = os.environ.get('LOCALAPPDATA', os.environ.get('APPDATA', str(os.path.expanduser('~'))))
        return os.path.join(base, 'DevContext', 'Cache')
    elif get_platform() == 'macos':
        base = os.environ.get('HOME', str(os.path.expanduser('~')))
        return os.path.join(base, 'Library', 'Caches', 'DevContext')
    else:  # Linux
        xdg_cache = os.environ.get('XDG_CACHE_HOME', '')
        if xdg_cache:
            return os.path.join(xdg_cache, 'devcontext')
        return os.path.expanduser('~/.cache/devcontext')


# Path helpers
def expand_path(path: str) -> str:
    """Expand user and environment variables in path."""
    return os.path.abspath(os.path.expanduser(os.path.expandvars(path)))


def ensure_dir(path: str) -> bool:
    """Ensure directory exists."""
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except OSError:
        return False


# Encoding helpers (Python 3.8 compatibility)
def ensure_text(s, encoding: str = 'utf-8') -> str:
    """Ensure value is text (str)."""
    if isinstance(s, bytes):
        return s.decode(encoding)
    return str(s)


def ensure_binary(s, encoding: str = 'utf-8') -> bytes:
    """Ensure value is binary (bytes)."""
    if isinstance(s, str):
        return s.encode(encoding)
    return bytes(s)


# JSON compatibility
import json

def json_loads(s):
    """Load JSON with compatibility for Python 3.8."""
    return json.loads(s)


# functools compatibility for Python < 3.9
try:
    from functools import cached_property
except ImportError:
    from functools import property as cached_property
    
    def cached_property(func):
        """Simple cached_property implementation for Python 3.8."""
        return property(func)


# typing helpers
OptionalStr = Optional[str]
OptionalInt = Optional[int]
DictStr = Dict[str, Any]


# Export all
__all__ = [
    'PY38', 'PY39', 'PY310', 'PY311',
    'get_python_version', 'is_frozen', 'get_platform',
    'get_home_config_dir', 'get_cache_dir',
    'expand_path', 'ensure_dir',
    'ensure_text', 'ensure_binary',
    'json_loads',
    'cached_property',
    'OptionalStr', 'OptionalInt', 'DictStr',
]