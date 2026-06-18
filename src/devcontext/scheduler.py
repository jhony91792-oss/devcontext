# Scheduled context generation for DevContext

import time
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta


class Schedule:
    """Represents a scheduled context generation."""
    
    def __init__(self, name: str, path: str, interval: int, output_dir: str):
        self.name = name
        self.path = path
        self.interval = interval  # seconds
        self.output_dir = Path(output_dir)
        self.last_run: Optional[datetime] = None
        self.enabled = True
    
    def should_run(self) -> bool:
        """Check if it's time to run."""
        if not self.enabled:
            return False
        
        if self.last_run is None:
            return True
        
        elapsed = (datetime.now() - self.last_run).total_seconds()
        return elapsed >= self.interval
    
    def run(self) -> Optional[Dict[str, Any]]:
        """Run context generation."""
        from devcontext import DevContext
        
        try:
            dc = DevContext(self.path)
            context = dc.generate()
            self.last_run = datetime.now()
            
            # Save output
            self.output_dir.mkdir(parents=True, exist_ok=True)
            output_file = self.output_dir / f"{self.name}_{int(time.time())}.json"
            
            with open(output_file, 'w') as f:
                json.dump(context, f, indent=2)
            
            return context
        except Exception as e:
            print(f"Schedule {self.name} failed: {e}")
            return None


class Scheduler:
    """Manage scheduled context generations."""
    
    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            from devcontext.compat import get_cache_dir
            config_path = str(Path(get_cache_dir()) / "schedules.json")
        
        self.config_path = Path(config_path)
        self.schedules: List[Schedule] = []
        self._load()
    
    def _load(self):
        """Load schedules from config."""
        if self.config_path.exists():
            with open(self.config_path) as f:
                data = json.load(f)
            
            for item in data.get("schedules", []):
                schedule = Schedule(
                    item["name"],
                    item["path"],
                    item["interval"],
                    item.get("output_dir", "/tmp/devcontext-schedules")
                )
                self.schedules.append(schedule)
    
    def _save(self):
        """Save schedules to config."""
        data = {
            "schedules": [
                {
                    "name": s.name,
                    "path": s.path,
                    "interval": s.interval,
                    "output_dir": str(s.output_dir)
                }
                for s in self.schedules
            ]
        }
        
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add(self, name: str, path: str, interval: int, output_dir: str = "/tmp/devcontext-schedules"):
        """Add a new schedule."""
        schedule = Schedule(name, path, interval, output_dir)
        self.schedules.append(schedule)
        self._save()
        return schedule
    
    def remove(self, name: str) -> bool:
        """Remove a schedule."""
        self.schedules = [s for s in self.schedules if s.name != name]
        self._save()
        return True
    
    def list(self) -> List[Dict[str, Any]]:
        """List all schedules."""
        return [
            {
                "name": s.name,
                "path": s.path,
                "interval": s.interval,
                "last_run": s.last_run.isoformat() if s.last_run else None,
                "enabled": s.enabled
            }
            for s in self.schedules
        ]
    
    def run_pending(self) -> List[Dict[str, Any]]:
        """Run all pending schedules."""
        results = []
        
        for schedule in self.schedules:
            if schedule.should_run():
                result = schedule.run()
                results.append({
                    "name": schedule.name,
                    "success": result is not None
                })
        
        self._save()
        return results
    
    def run_loop(self, check_interval: int = 60):
        """Run scheduler loop."""
        print(f"Scheduler started (checking every {check_interval}s)")
        
        try:
            while True:
                results = self.run_pending()
                
                if results:
                    for r in results:
                        status = "✅" if r["success"] else "❌"
                        print(f"{status} {r['name']}")
                
                time.sleep(check_interval)
        except KeyboardInterrupt:
            print("\nScheduler stopped.")


# CLI
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Schedule context generation")
    sub = parser.add_subparsers(dest="command")
    
    add_cmd = sub.add_parser("add", help="Add schedule")
    add_cmd.add_argument("name", help="Schedule name")
    add_cmd.add_argument("path", help="Project path")
    add_cmd.add_argument("interval", type=int, help="Interval in seconds")
    
    remove_cmd = sub.add_parser("remove", help="Remove schedule")
    remove_cmd.add_argument("name", help="Schedule name")
    
    list_cmd = sub.add_parser("list", help="List schedules")
    
    run_cmd = sub.add_parser("run", help="Run pending schedules")
    
    loop_cmd = sub.add_parser("loop", help="Run scheduler loop")
    loop_cmd.add_argument("-i", "--interval", type=int, default=60)
    
    args = parser.parse_args()
    
    scheduler = Scheduler()
    
    if args.command == "add":
        scheduler.add(args.name, args.path, args.interval)
        print(f"Added schedule: {args.name}")
    
    elif args.command == "remove":
        scheduler.remove(args.name)
        print(f"Removed schedule: {args.name}")
    
    elif args.command == "list":
        schedules = scheduler.list()
        print(f"Schedules: {len(schedules)}")
        for s in schedules:
            print(f"  - {s['name']}: {s['path']} (every {s['interval']}s)")
    
    elif args.command == "run":
        results = scheduler.run_pending()
        for r in results:
            print(f"{'✅' if r['success'] else '❌'} {r['name']}")
    
    elif args.command == "loop":
        scheduler.run_loop(args.interval)


if __name__ == "__main__":
    main()