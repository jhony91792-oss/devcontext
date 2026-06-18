# Configuration handling for DevContext

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any


DEFAULT_CONFIG = {
    "max_depth": 10,
    "skip_dirs": [".git", "__pycache__", "node_modules", ".venv", "venv", "dist", "build"],
    "skip_files": [".DS_Store", "Thumbs.db", "*.pyc", "*.pyo"],
    "include_hidden": False,
    "output_format": "json",
    "show_stats": True,
    "languages": None,  # None = all supported
    "exclude_patterns": [],
    "include_patterns": ["*"],
}


def find_config(start_path: str = ".") -> Optional[Path]:
    """Find .devcontextrc config file in directory tree."""
    path = Path(start_path).resolve()
    candidates = [
        path / ".devcontextrc",
        path / ".devcontextrc.json",
        path / "devcontext.json",
        path / ".devcontext" / "config.json",
    ]
    
    for candidate in candidates:
        if candidate.exists():
            return candidate
    
    # Check parent directories
    parent = path.parent
    if parent != path:
        return find_config(str(parent))
    
    return None


def load_config(start_path: str = ".") -> Dict[str, Any]:
    """Load configuration from file or return defaults."""
    config_file = find_config(start_path)
    
    if config_file is None:
        return DEFAULT_CONFIG.copy()
    
    try:
        with open(config_file) as f:
            user_config = json.load(f)
        
        # Merge with defaults
        config = DEFAULT_CONFIG.copy()
        config.update(user_config)
        return config
    except Exception:
        return DEFAULT_CONFIG.copy()


def save_config(config: Dict[str, Any], path: str = ".devcontextrc") -> None:
    """Save configuration to file."""
    with open(path, 'w') as f:
        json.dump(config, f, indent=2)


def get_config_path() -> Path:
    """Get default config file path."""
    return Path.home() / ".config" / "devcontext" / "config.json"


def ensure_global_config() -> Path:
    """Ensure global config directory exists."""
    config_path = get_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)
    return config_path


def load_global_config() -> Dict[str, Any]:
    """Load global (user-level) configuration."""
    config_path = get_config_path()
    
    if not config_path.exists():
        return DEFAULT_CONFIG.copy()
    
    try:
        with open(config_path) as f:
            return json.load(f)
    except Exception:
        return DEFAULT_CONFIG.copy()


def merge_configs(*configs: Dict[str, Any]) -> Dict[str, Any]:
    """Merge multiple config dicts, with later ones overriding earlier."""
    result = {}
    for config in configs:
        result.update(config)
    return result


# CLI integration helpers
def config_to_cli_args(config: Dict[str, Any]) -> List[str]:
    """Convert config dict to CLI arguments."""
    args = []
    
    if config.get("max_depth"):
        args.extend(["--max-depth", str(config["max_depth"])])
    
    if config.get("include_hidden"):
        args.append("--include-hidden")
    
    if config.get("output_format"):
        args.extend(["--format", config["output_format"]])
    
    if config.get("show_stats") is False:
        args.append("--no-stats")
    
    return args