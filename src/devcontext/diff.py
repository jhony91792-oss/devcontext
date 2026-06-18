# Diff module for DevContext - context comparison

import json
from typing import Dict, Any, List, Optional


class ContextDiff:
    """Compare two DevContext contexts."""
    
    def __init__(self, old: Dict[str, Any], new: Dict[str, Any]):
        self.old = old
        self.new = new
    
    def get_added_files(self) -> List[str]:
        """Get files that were added."""
        old_files = set(self.old.get("files", {}).keys())
        new_files = set(self.new.get("files", {}).keys())
        return sorted(list(new_files - old_files))
    
    def get_removed_files(self) -> List[str]:
        """Get files that were removed."""
        old_files = set(self.old.get("files", {}).keys())
        new_files = set(self.new.get("files", {}).keys())
        return sorted(list(old_files - new_files))
    
    def get_changed_files(self) -> List[str]:
        """Get files that were modified."""
        common = set(self.old.get("files", {}).keys()) & set(self.new.get("files", {}).keys())
        changed = []
        
        for f in common:
            old_info = self.old["files"][f]
            new_info = self.new["files"][f]
            if old_info != new_info:
                changed.append(f)
        
        return sorted(changed)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "added": self.get_added_files(),
            "removed": self.get_removed_files(),
            "changed": self.get_changed_files(),
            "summary": {
                "added_count": len(self.get_added_files()),
                "removed_count": len(self.get_removed_files()),
                "changed_count": len(self.get_changed_files()),
            }
        }


def compare_contexts(old: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
    """Compare two contexts."""
    diff = ContextDiff(old, new)
    return diff.to_dict()


# CLI
def main():
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description="Compare DevContext contexts")
    parser.add_argument("old", help="Old context JSON file")
    parser.add_argument("new", help="New context JSON file")
    
    args = parser.parse_args()
    
    with open(args.old) as f:
        old = json.load(f)
    with open(args.new) as f:
        new = json.load(f)
    
    diff = ContextDiff(old, new)
    print(json.dumps(diff.to_dict(), indent=2))


if __name__ == "__main__":
    main()