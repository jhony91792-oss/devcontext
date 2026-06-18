# Backup/restore module for DevContext

import os
import json
import shutil
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime


class BackupManager:
    """Manage context backups."""
    
    def __init__(self, backup_dir: Optional[str] = None):
        if backup_dir is None:
            from devcontext.compat import get_cache_dir
            backup_dir = str(Path(get_cache_dir()) / "backups")
        
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def create_backup(self, context: Dict[str, Any], name: str = None) -> str:
        """Create a backup of context."""
        if name is None:
            name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        backup_file = self.backup_dir / f"{name}.json"
        
        with open(backup_file, 'w') as f:
            json.dump(context, f, indent=2)
        
        return str(backup_file)
    
    def restore_backup(self, name: str = None) -> Optional[Dict[str, Any]]:
        """Restore a backup."""
        if name is None:
            # Get latest backup
            backups = sorted(self.backup_dir.glob("backup_*.json"), key=lambda p: p.stat().st_mtime)
            if not backups:
                return None
            backup_file = backups[-1]
        else:
            backup_file = self.backup_dir / f"{name}.json"
        
        if not backup_file.exists():
            return None
        
        with open(backup_file) as f:
            return json.load(f)
    
    def list_backups(self) -> List[Dict[str, Any]]:
        """List all backups."""
        backups = []
        for f in sorted(self.backup_dir.glob("backup_*.json"), key=lambda p: p.stat().st_mtime, reverse=True):
            stat = f.stat()
            backups.append({
                "name": f.stem,
                "path": str(f),
                "size": stat.st_size,
                "created": datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
        return backups
    
    def delete_backup(self, name: str) -> bool:
        """Delete a backup."""
        backup_file = self.backup_dir / f"{name}.json"
        if backup_file.exists():
            backup_file.unlink()
            return True
        return False
    
    def cleanup_old(self, days: int = 30) -> int:
        """Delete backups older than N days."""
        count = 0
        cutoff = datetime.now().timestamp() - (days * 86400)
        
        for f in self.backup_dir.glob("backup_*.json"):
            if f.stat().st_mtime < cutoff:
                f.unlink()
                count += 1
        
        return count


def backup_context(context: Dict[str, Any], name: str = None) -> str:
    """Quick backup function."""
    manager = BackupManager()
    return manager.create_backup(context, name)


def restore_context(name: str = None) -> Optional[Dict[str, Any]]:
    """Quick restore function."""
    manager = BackupManager()
    return manager.restore_backup(name)


# CLI
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Manage DevContext backups")
    sub = parser.add_subparsers(dest="command")
    
    list_cmd = sub.add_parser("list", help="List backups")
    list_cmd.add_argument("--json", action="store_true")
    
    restore_cmd = sub.add_parser("restore", help="Restore backup")
    restore_cmd.add_argument("name", nargs="?", help="Backup name (latest if omitted)")
    restore_cmd.add_argument("-o", "--output", help="Output file")
    
    delete_cmd = sub.add_parser("delete", help="Delete backup")
    delete_cmd.add_argument("name", help="Backup name")
    
    cleanup_cmd = sub.add_parser("cleanup", help="Clean old backups")
    cleanup_cmd.add_argument("-d", "--days", type=int, default=30)
    
    args = parser.parse_args()
    
    manager = BackupManager()
    
    if args.command == "list":
        backups = manager.list_backups()
        if args.json:
            print(json.dumps(backups, indent=2))
        else:
            print(f"Backups: {len(backups)}")
            for b in backups[:10]:
                print(f"  {b['name']} - {b['size']} bytes - {b['created'][:10]}")
    
    elif args.command == "restore":
        context = manager.restore_backup(args.name)
        if context:
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(context, f, indent=2)
                print(f"Restored to {args.output}")
            else:
                print(json.dumps(context, indent=2))
        else:
            print("Backup not found")
    
    elif args.command == "delete":
        if manager.delete_backup(args.name):
            print("Deleted")
        else:
            print("Backup not found")
    
    elif args.command == "cleanup":
        count = manager.cleanup_old(args.days)
        print(f"Deleted {count} old backups")


if __name__ == "__main__":
    main()