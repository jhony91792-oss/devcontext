# Snapshot module for DevContext - track project evolution over time

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime


class SnapshotManager:
    """Manage project snapshots for tracking changes."""
    
    def __init__(self, snapshots_dir: Optional[str] = None):
        if snapshots_dir is None:
            from devcontext.compat import get_cache_dir
            snapshots_dir = str(Path(get_cache_dir()) / "snapshots")
        
        self.snapshots_dir = Path(snapshots_dir)
        self.snapshots_dir.mkdir(parents=True, exist_ok=True)
        self.manifest_file = self.snapshots_dir / "manifest.json"
        self.manifest = self._load_manifest()
    
    def _load_manifest(self) -> Dict[str, Any]:
        """Load snapshot manifest."""
        if self.manifest_file.exists():
            with open(self.manifest_file) as f:
                return json.load(f)
        return {"snapshots": []}
    
    def _save_manifest(self):
        """Save snapshot manifest."""
        with open(self.manifest_file, 'w') as f:
            json.dump(self.manifest, f, indent=2)
    
    def take_snapshot(self, context: Dict[str, Any], tag: str = None) -> str:
        """Take a snapshot of current state."""
        timestamp = datetime.now().isoformat()
        
        if tag is None:
            # Generate tag from timestamp
            tag = f"snap_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        snapshot_id = f"{tag}_{len(self.manifest['snapshots'])}"
        snapshot_file = self.snapshots_dir / f"{snapshot_id}.json"
        
        # Add metadata
        snapshot = {
            "id": snapshot_id,
            "tag": tag,
            "timestamp": timestamp,
            "context": context,
            "file_count": context.get("metadata", {}).get("total_files", len(context.get("files", {})))
        }
        
        with open(snapshot_file, 'w') as f:
            json.dump(snapshot, f, indent=2)
        
        self.manifest["snapshots"].append({
            "id": snapshot_id,
            "tag": tag,
            "timestamp": timestamp,
            "file": str(snapshot_file)
        })
        self._save_manifest()
        
        return snapshot_id
    
    def get_snapshot(self, snapshot_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific snapshot."""
        snapshot_file = self.snapshots_dir / f"{snapshot_id}.json"
        
        if not snapshot_file.exists():
            return None
        
        with open(snapshot_file) as f:
            return json.load(f)
    
    def list_snapshots(self) -> List[Dict[str, Any]]:
        """List all snapshots."""
        return self.manifest.get("snapshots", [])
    
    def compare_snapshots(self, id1: str, id2: str) -> Dict[str, Any]:
        """Compare two snapshots."""
        snap1 = self.get_snapshot(id1)
        snap2 = self.get_snapshot(id2)
        
        if not snap1 or not snap2:
            return {"error": "Snapshot not found"}
        
        files1 = set(snap1.get("context", {}).get("files", {}).keys())
        files2 = set(snap2.get("context", {}).get("files", {}).keys())
        
        added = files2 - files1
        removed = files1 - files2
        
        return {
            "snapshot1": id1,
            "snapshot2": id2,
            "timestamp1": snap1.get("timestamp"),
            "timestamp2": snap2.get("timestamp"),
            "files_added": list(added),
            "files_removed": list(removed),
            "net_change": len(added) - len(removed)
        }
    
    def delete_snapshot(self, snapshot_id: str) -> bool:
        """Delete a snapshot."""
        snapshot_file = self.snapshots_dir / f"{snapshot_id}.json"
        
        if snapshot_file.exists():
            snapshot_file.unlink()
            
            # Remove from manifest
            self.manifest["snapshots"] = [
                s for s in self.manifest["snapshots"]
                if s["id"] != snapshot_id
            ]
            self._save_manifest()
            return True
        
        return False


def take_snapshot(context: Dict[str, Any], tag: str = None) -> str:
    """Quick snapshot function."""
    manager = SnapshotManager()
    return manager.take_snapshot(context, tag)


# CLI
def main():
    import argparse
    parser = argparse.ArgumentParser(description="DevContext snapshots")
    sub = parser.add_subparsers(dest="command")
    
    take = sub.add_parser("take", help="Take snapshot")
    take.add_argument("-t", "--tag", help="Snapshot tag")
    
    list_cmd = sub.add_parser("list", help="List snapshots")
    
    compare = sub.add_parser("compare", help="Compare snapshots")
    compare.add_argument("id1", help="First snapshot ID")
    compare.add_argument("id2", help="Second snapshot ID")
    
    args = parser.parse_args()
    
    manager = SnapshotManager()
    
    if args.command == "take":
        # Would need context input
        print("Run: devcontext generate . | devcontext snapshot take")
    
    elif args.command == "list":
        snapshots = manager.list_snapshots()
        print(f"Snapshots: {len(snapshots)}")
        for s in snapshots[-10:]:
            print(f"  {s['id']} - {s['timestamp'][:10]}")
    
    elif args.command == "compare":
        result = manager.compare_snapshots(args.id1, args.id2)
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()