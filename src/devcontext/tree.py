# Tree module for DevContext - display project structure

import os
from pathlib import Path
from typing import Dict, Any, List, Optional


def get_tree_structure(path: str = ".", max_depth: int = 10, ignore_patterns: List[str] = None) -> str:
    """Generate ASCII tree of project structure."""
    
    if ignore_patterns is None:
        ignore_patterns = [".git", "node_modules", "__pycache__", ".pyc", ".venv", ".venv39"]
    
    root_path = Path(path)
    lines = [f"{root_path.name}/"]
    
    def walk_directory(current_path: Path, prefix: str = "", depth: int = 0):
        if depth >= max_depth:
            return
        
        try:
            entries = sorted(current_path.iterdir(), key=lambda e: (not e.is_dir(), e.name))
        except PermissionError:
            return
        
        dirs = []
        files = []
        
        for entry in entries:
            name = entry.name
            
            # Check ignore patterns
            if any(pattern in name for pattern in ignore_patterns):
                continue
            
            if entry.is_dir():
                dirs.append(entry)
            else:
                files.append(entry)
        
        # Process directories
        for i, dir_entry in enumerate(dirs):
            is_last_dir = (i == len(dirs) - 1) and len(files) == 0
            connector = "└── " if is_last_dir else "├── "
            
            lines.append(f"{prefix}{connector}{dir_entry.name}/")
            
            extension = "    " if is_last_dir else "│   "
            walk_directory(dir_entry, prefix + extension, depth + 1)
        
        # Process files
        for i, file_entry in enumerate(files):
            is_last = (i == len(files) - 1)
            connector = "└── " if is_last else "├── "
            lines.append(f"{prefix}{connector}{file_entry.name}")
    
    walk_directory(root_path)
    return "\n".join(lines)


def get_tree_dict(path: str = ".", max_depth: int = 10, ignore_patterns: List[str] = None) -> Dict[str, Any]:
    """Generate tree as nested dictionary."""
    
    if ignore_patterns is None:
        ignore_patterns = [".git", "node_modules", "__pycache__", ".pyc", ".venv", ".venv39"]
    
    root_path = Path(path)
    
    def walk(current_path: Path, depth: int = 0) -> Dict[str, Any]:
        if depth >= max_depth:
            return {}
        
        node = {"_type": "dir", "_path": str(current_path), "children": {}}
        
        try:
            entries = sorted(current_path.iterdir(), key=lambda e: (not e.is_dir(), e.name))
        except PermissionError:
            return node
        
        for entry in entries:
            name = entry.name
            
            if any(pattern in name for pattern in ignore_patterns):
                continue
            
            if entry.is_dir():
                node["children"][name] = walk(entry, depth + 1)
            else:
                node["children"][name] = {"_type": "file", "_path": str(entry)}
        
        return node
    
    return {root_path.name: walk(root_path)}


# CLI
def main():
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description="Display project tree")
    parser.add_argument("path", nargs="?", default=".", help="Path to display")
    parser.add_argument("-d", "--max-depth", type=int, default=10, help="Maximum depth")
    parser.add_argument("-j", "--json", action="store_true", help="JSON output")
    parser.add_argument("--show-lang", action="store_true", help="Show language icons")
    
    args = parser.parse_args()
    
    if args.json:
        tree = get_tree_dict(args.path, args.max_depth)
        print(json.dumps(tree, indent=2))
    else:
        tree = get_tree_structure(args.path, args.max_depth)
        print(tree)


if __name__ == "__main__":
    main()