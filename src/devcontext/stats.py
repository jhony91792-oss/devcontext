# Statistics tracking for DevContext

import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta


class StatsTracker:
    """Track DevContext usage statistics."""
    
    def __init__(self, stats_file: Optional[str] = None):
        if stats_file is None:
            from devcontext.compat import get_cache_dir
            get_cache_dir()
            stats_file = Path("~/.cache/devcontext/stats.json").expanduser()
        
        self.stats_file = Path(stats_file)
        self.stats_file.parent.mkdir(parents=True, exist_ok=True)
        self.stats = self._load()
    
    def _load(self) -> Dict[str, Any]:
        """Load stats from file."""
        if self.stats_file.exists():
            try:
                with open(self.stats_file) as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                pass
        
        return self._default_stats()
    
    def _default_stats(self) -> Dict[str, Any]:
        """Get default stats structure."""
        return {
            "total_runs": 0,
            "total_files_scanned": 0,
            "total_bytes_processed": 0,
            "languages_used": {},
            "last_run": None,
            "last_run_duration": 0,
            "errors": 0,
            "star_history": [],
            "installs": 0,
        }
    
    def _save(self):
        """Save stats to file."""
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except OSError:
            pass
    
    def record_run(self, files_scanned: int = 0, bytes_processed: int = 0,
                   language: str = None, duration: float = 0,
                   success: bool = True):
        """Record a run."""
        self.stats["total_runs"] += 1
        self.stats["last_run"] = datetime.now().isoformat()
        self.stats["last_run_duration"] = duration
        self.stats["total_files_scanned"] += files_scanned
        self.stats["total_bytes_processed"] += bytes_processed
        
        if language:
            lang_stats = self.stats["languages_used"]
            lang_stats[language] = lang_stats.get(language, 0) + 1
        
        if not success:
            self.stats["errors"] += 1
        
        self._save()
    
    def record_star(self, count: int):
        """Record star count."""
        self.stats["star_history"].append({
            "count": count,
            "timestamp": datetime.now().isoformat()
        })
        self._save()
    
    def get_summary(self) -> Dict[str, Any]:
        """Get stats summary."""
        return {
            "total_runs": self.stats["total_runs"],
            "total_files_scanned": self.stats["total_files_scanned"],
            "languages_used": self.stats["languages_used"],
            "last_run": self.stats["last_run"],
            "avg_duration": self.stats["last_run_duration"],
            "errors": self.stats["errors"],
        }
    
    def get_top_languages(self, n: int = 5) -> List[tuple]:
        """Get top N languages by usage."""
        langs = self.stats.get("languages_used", {})
        return sorted(langs.items(), key=lambda x: x[1], reverse=True)[:n]
    
    def get_star_history(self) -> List[Dict[str, Any]]:
        """Get star count history."""
        return self.stats.get("star_history", [])
    
    def clear(self):
        """Clear all stats."""
        self.stats = self._default_stats()
        self._save()


# Global stats tracker instance
_stats: Optional[StatsTracker] = None


def get_stats() -> StatsTracker:
    """Get global stats tracker."""
    global _stats
    if _stats is None:
        _stats = StatsTracker()
    return _stats


# CLI commands
def main():
    import argparse
    parser = argparse.ArgumentParser(description="DevContext Statistics")
    sub = parser.add_subparsers(dest="command")
    
    show = sub.add_parser("show", help="Show stats summary")
    show.add_argument("--json", action="store_true", help="JSON output")
    
    history = sub.add_parser("history", help="Show star history")
    
    clear = sub.add_parser("clear", help="Clear all stats")
    
    args = parser.parse_args()
    
    stats = get_stats()
    
    if args.command == "show":
        if args.json:
            print(json.dumps(stats.get_summary(), indent=2))
        else:
            summary = stats.get_summary()
            print("DevContext Statistics")
            print("=" * 40)
            print(f"Total runs: {summary['total_runs']}")
            print(f"Files scanned: {summary['total_files_scanned']}")
            print(f"Last run: {summary['last_run']}")
            print(f"Errors: {summary['errors']}")
            print("\nTop languages:")
            for lang, count in stats.get_top_languages():
                print(f"  {lang}: {count}")
    
    elif args.command == "history":
        history = stats.get_star_history()
        if not history:
            print("No star history yet")
        else:
            for entry in history:
                print(f"{entry['timestamp']}: {entry['count']} stars")
    
    elif args.command == "clear":
        stats.clear()
        print("Stats cleared")


if __name__ == "__main__":
    main()