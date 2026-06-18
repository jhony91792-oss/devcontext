# Metrics collection for DevContext

import json
import time
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime


class MetricsCollector:
    """Collect usage metrics."""
    
    def __init__(self, storage_path: str = None):
        if storage_path is None:
            from devcontext.compat import get_cache_dir
            storage_path = str(Path(get_cache_dir()) / "metrics.json")
        
        self.storage_path = Path(storage_path)
        self.metrics = self._load()
    
    def _load(self) -> Dict[str, Any]:
        """Load metrics from storage."""
        if self.storage_path.exists():
            with open(self.storage_path) as f:
                return json.load(f)
        return {
            "generations": 0,
            "formats": {},
            "total_files_processed": 0,
            "total_time": 0,
            "last_run": None,
            "paths": []
        }
    
    def _save(self):
        """Save metrics to storage."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.storage_path, 'w') as f:
            json.dump(self.metrics, f, indent=2)
    
    def record_generation(self, path: str, format: str, files: int, duration: float):
        """Record a context generation."""
        self.metrics["generations"] += 1
        self.metrics["total_files_processed"] += files
        self.metrics["total_time"] += duration
        self.metrics["last_run"] = datetime.now().isoformat()
        
        # Track format usage
        if format not in self.metrics["formats"]:
            self.metrics["formats"][format] = 0
        self.metrics["formats"][format] += 1
        
        # Track paths
        if path not in self.metrics["paths"]:
            self.metrics["paths"].append(path)
        
        self._save()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current statistics."""
        avg_time = (
            self.metrics["total_time"] / self.metrics["generations"]
            if self.metrics["generations"] > 0 else 0
        )
        
        return {
            "generations": self.metrics["generations"],
            "total_files": self.metrics["total_files_processed"],
            "avg_generation_time": round(avg_time, 3),
            "total_time": round(self.metrics["total_time"], 2),
            "formats": self.metrics["formats"],
            "unique_paths": len(self.metrics["paths"]),
            "last_run": self.metrics["last_run"]
        }
    
    def reset(self):
        """Reset all metrics."""
        self.metrics = {
            "generations": 0,
            "formats": {},
            "total_files_processed": 0,
            "total_time": 0,
            "last_run": None,
            "paths": []
        }
        self._save()
    
    def export(self, filepath: str):
        """Export metrics to file."""
        with open(filepath, 'w') as f:
            json.dump({
                "stats": self.get_stats(),
                "raw": self.metrics
            }, f, indent=2)


# CLI
def main():
    import argparse
    parser = argparse.ArgumentParser(description="DevContext metrics")
    sub = parser.add_subparsers(dest="command")
    
    stats_cmd = sub.add_parser("stats", help="Show statistics")
    
    reset_cmd = sub.add_parser("reset", help="Reset metrics")
    reset_cmd.add_argument("-y", "--yes", action="store_true")
    
    export_cmd = sub.add_parser("export", help="Export metrics")
    export_cmd.add_argument("-o", "--output", required=True)
    
    args = parser.parse_args()
    
    collector = MetricsCollector()
    
    if args.command == "stats":
        stats = collector.get_stats()
        print("DevContext Metrics")
        print("=" * 40)
        print(f"Generations:     {stats['generations']}")
        print(f"Total files:     {stats['total_files']}")
        print(f"Avg time:        {stats['avg_generation_time']}s")
        print(f"Unique paths:    {stats['unique_paths']}")
        print(f"Last run:        {stats['last_run'] or 'Never'}")
        print()
        print("Format usage:")
        for fmt, count in stats['formats'].items():
            print(f"  {fmt}: {count}")
    
    elif args.command == "reset":
        if args.yes or input("Reset all metrics? (y/n) ").lower() == 'y':
            collector.reset()
            print("Metrics reset")
    
    elif args.command == "export":
        collector.export(args.output)
        print(f"Exported to {args.output}")


if __name__ == "__main__":
    main()