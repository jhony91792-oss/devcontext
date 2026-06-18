# Watch mode functionality for DevContext

import os
import time
import subprocess
from pathlib import Path
from typing import Callable, Optional, List


class FileWatcher:
    """Watch filesystem for changes and trigger callbacks."""
    
    def __init__(self, path: str = ".", ignore_dirs: Optional[List[str]] = None):
        self.path = Path(path).resolve()
        self.ignore_dirs = ignore_dirs or [".git", "__pycache__", "node_modules", ".venv"]
        self.mtimes = {}
        self.running = False
        
    def scan(self) -> dict:
        """Get current file modification times."""
        files = {}
        for root, dirs, filenames in os.walk(self.path):
            # Filter ignore dirs
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]
            
            for filename in filenames:
                filepath = os.path.join(root, filename)
                try:
                    files[filepath] = os.path.getmtime(filepath)
                except OSError:
                    pass
        return files
    
    def detect_changes(self) -> List[str]:
        """Detect changed files since last scan."""
        current = self.scan()
        changes = []
        
        for filepath, mtime in current.items():
            if filepath not in self.mtimes:
                changes.append(filepath)
            elif self.mtimes[filepath] != mtime:
                changes.append(filepath)
        
        self.mtimes = current
        return changes
    
    def watch(self, callback: Callable[[List[str]], None], interval: float = 1.0):
        """Watch for changes and call callback on changes."""
        self.running = True
        self.mtimes = self.scan()  # Initial scan
        
        while self.running:
            changes = self.detect_changes()
            if changes:
                callback(changes)
            time.sleep(interval)
    
    def stop(self):
        """Stop watching."""
        self.running = False


def watch_and_generate(path: str = ".", output_file: str = ".devcontext.json", interval: float = 5.0):
    """Watch project and auto-regenerate context on changes."""
    import devcontext
    
    def on_changes(changes):
        print(f"Changes detected in {len(changes)} files:")
        for f in changes[:10]:
            print(f"  {f}")
        print("Regenerating context...")
        
        try:
            # Run generate command
            subprocess.run(
                ["devcontext", "generate", path, "-o", output_file],
                check=True
            )
            print(f"Context updated: {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error generating context: {e}")
    
    print(f"Watching {path} for changes...")
    print(f"Context will be regenerated to {output_file} every {interval}s")
    print("Press Ctrl+C to stop")
    
    watcher = FileWatcher(path)
    try:
        watcher.watch(on_changes, interval)
    except KeyboardInterrupt:
        watcher.stop()
        print("\nStopped watching.")


# CLI integration
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Watch project for changes")
    parser.add_argument("path", nargs="?", default=".", help="Project path")
    parser.add_argument("-o", "--output", default=".devcontext.json", help="Output file")
    parser.add_argument("-i", "--interval", type=float, default=5.0, help="Check interval (seconds)")
    
    args = parser.parse_args()
    watch_and_generate(args.path, args.output, args.interval)


if __name__ == "__main__":
    main()