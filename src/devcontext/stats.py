# Stats module for DevContext - statistics tracking

import json
from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path


class StatsTracker:
    """Track DevContext usage statistics."""
    
    def __init__(self, storage_path: str = None):
        if storage_path is None:
            storage_path = str(Path.home() / ".cache" / "devcontext" / "stats.json")
        
        self.storage_path = Path(storage_path)
        self.stats = self._load()
    
    def _load(self) -> Dict[str, Any]:
        """Load stats from storage."""
        if self.storage_path.exists():
            try:
                with open(self.storage_path) as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "total_generations": 0,
            "total_files_processed": 0,
            "total_time_seconds": 0,
            "formats_used": {},
            "paths_scanned": [],
            "last_run": None
        }
    
    def _save(self):
        """Save stats to storage."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.storage_path, 'w') as f:
            json.dump(self.stats, f, indent=2)
    
    def record_generation(self, path: str, format: str, files: int, duration: float):
        """Record a context generation."""
        self.stats["total_generations"] += 1
        self.stats["total_files_processed"] += files
        self.stats["total_time_seconds"] += duration
        self.stats["last_run"] = datetime.now().isoformat()
        
        # Track format usage
        if format not in self.stats["formats_used"]:
            self.stats["formats_used"][format] = 0
        self.stats["formats_used"][format] += 1
        
        # Track unique paths
        if path not in self.stats["paths_scanned"]:
            self.stats["paths_scanned"].append(path)
        
        self._save()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current statistics."""
        avg_time = (
            self.stats["total_time_seconds"] / self.stats["total_generations"]
            if self.stats["total_generations"] > 0 else 0
        )
        
        return {
            "total_generations": self.stats["total_generations"],
            "total_files_processed": self.stats["total_files_processed"],
            "avg_generation_time": round(avg_time, 3),
            "total_time_seconds": round(self.stats["total_time_seconds"], 2),
            "formats_used": self.stats["formats_used"],
            "unique_paths": len(self.stats["paths_scanned"]),
            "last_run": self.stats["last_run"]
        }
    
    def reset(self):
        """Reset all statistics."""
        self.stats = {
            "total_generations": 0,
            "total_files_processed": 0,
            "total_time_seconds": 0,
            "formats_used": {},
            "paths_scanned": [],
            "last_run": None
        }
        self._save()


def get_stats() -> Dict[str, Any]:
    """Quick stats retrieval."""
    tracker = StatsTracker()
    return tracker.get_stats()


# CLI
def main():
    import argparse
    parser = argparse.ArgumentParser(description="DevContext statistics")
    sub = parser.add_subparsers(dest="command")
    
    show_cmd = sub.add_parser("show", help="Show statistics")
    show_cmd.add_argument("-j", "--json", action="store_true")
    
    reset_cmd = sub.add_parser("reset", help="Reset statistics")
    reset_cmd.add_argument("-y", "--yes", action="store_true")
    
    args = parser.parse_args()
    
    tracker = StatsTracker()
    
    if args.command == "show":
        stats = tracker.get_stats()
        
        if args.json:
            print(json.dumps(stats, indent=2))
        else:
            print("DevContext Statistics")
            print("=" * 40)
            print(f"Total generations: {stats['total_generations']}")
            print(f"Total files: {stats['total_files_processed']}")
            print(f"Avg time: {stats['avg_generation_time']}s")
            print(f"Unique paths: {stats['unique_paths']}")
            print(f"Last run: {stats['last_run'] or 'Never'}")
            print()
            print("Formats used:")
            for fmt, count in stats['formats_used'].items():
                print(f"  {fmt}: {count}")
    
    elif args.command == "reset":
        if args.yes or input("Reset all stats? (y/n) ").lower() == 'y':
            tracker.reset()
            print("Statistics reset")


if __name__ == "__main__":
    main()