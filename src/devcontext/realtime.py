# Real-time file diff and watch module for DevContext

import os
import time
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime


class FileWatcher:
    """Watch files for changes."""
    
    def __init__(self, path: str, ignore_patterns: List[str] = None):
        self.path = Path(path)
        self.ignore_patterns = ignore_patterns or [".git", "__pycache__", ".pyc"]
        self.file_hashes: Dict[str, str] = {}
        self._scan_files()
    
    def _scan_files(self):
        """Scan all files and compute hashes."""
        self.file_hashes = {}
        
        for root, dirs, files in os.walk(self.path):
            # Filter ignored directories
            dirs[:] = [d for d in dirs if not any(p in d for p in self.ignore_patterns)]
            
            for f in files:
                filepath = Path(root) / f
                rel_path = str(filepath.relative_to(self.path))
                
                if any(p in rel_path for p in self.ignore_patterns):
                    continue
                
                try:
                    with open(filepath, 'rb') as fp:
                        file_hash = hashlib.md5(fp.read()).hexdigest()
                    self.file_hashes[rel_path] = file_hash
                except:
                    pass
    
    def check_changes(self) -> Dict[str, Any]:
        """Check for file changes since last scan."""
        changes = {
            "added": [],
            "modified": [],
            "deleted": []
        }
        
        current_hashes: Dict[str, str] = {}
        
        for root, dirs, files in os.walk(self.path):
            dirs[:] = [d for d in dirs if not any(p in d for p in self.ignore_patterns)]
            
            for f in files:
                filepath = Path(root) / f
                rel_path = str(filepath.relative_to(self.path))
                
                if any(p in rel_path for p in self.ignore_patterns):
                    continue
                
                try:
                    with open(filepath, 'rb') as fp:
                        file_hash = hashlib.md5(fp.read()).hexdigest()
                    current_hashes[rel_path] = file_hash
                    
                    if rel_path not in self.file_hashes:
                        changes["added"].append(rel_path)
                    elif file_hash != self.file_hashes[rel_path]:
                        changes["modified"].append(rel_path)
                except:
                    pass
        
        # Find deleted files
        for rel_path in self.file_hashes:
            if rel_path not in current_hashes:
                changes["deleted"].append(rel_path)
        
        # Update hashes
        self.file_hashes = current_hashes
        
        return changes


class RealtimeContext:
    """Real-time context with change tracking."""
    
    def __init__(self, path: str = "."):
        self.path = Path(path)
        self.watcher = FileWatcher(path)
    
    def generate_with_diff(self) -> Dict[str, Any]:
        """Generate context with diff info."""
        from devcontext import DevContext
        
        # Get current context
        dc = DevContext(str(self.path))
        context = dc.generate()
        
        # Check changes
        changes = self.watcher.check_changes()
        
        # Add change info to context
        context["changes"] = changes
        context["change_timestamp"] = datetime.now().isoformat()
        
        return context
    
    def watch(self, callback: Callable, interval: int = 10):
        """Watch for changes and call callback."""
        while True:
            changes = self.watcher.check_changes()
            
            if any(changes.values()):
                context = self.generate_with_diff()
                callback(context, changes)
            
            time.sleep(interval)


def generate_diff_context(path: str = ".") -> Dict[str, Any]:
    """Quick diff context generation."""
    watcher = FileWatcher(path)
    return watcher.check_changes()


# CLI
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Watch and diff files")
    parser.add_argument("path", nargs="?", default=".", help="Path to watch")
    parser.add_argument("-i", "--interval", type=int, default=10, help="Check interval (seconds)")
    parser.add_argument("--once", action="store_true", help="Check once and exit")
    
    args = parser.parse_args()
    
    watcher = FileWatcher(args.path)
    
    if args.once:
        changes = watcher.check_changes()
        import json
        print(json.dumps(changes, indent=2))
    else:
        print(f"Watching {args.path} for changes (Ctrl+C to stop)...")
        try:
            while True:
                changes = watcher.check_changes()
                if any(changes.values()):
                    print(f"\n[{datetime.now().isoformat()}] Changes detected:")
                    for kind, files in changes.items():
                        if files:
                            print(f"  {kind}: {', '.join(files)}")
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\nStopped.")


if __name__ == "__main__":
    main()