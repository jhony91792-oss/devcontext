# Diff functionality for DevContext

import os
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from difflib import unified_diff, context_diff


def compare_files(old: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
    """Compare two file trees and return differences."""
    old_files = set(old.get("files", {}).keys())
    new_files = set(new.get("files", {}).keys())
    
    added = new_files - old_files
    removed = old_files - new_files
    common = old_files & new_files
    
    modified = []
    for f in common:
        if old["files"][f].get("hash") != new["files"][f].get("hash"):
            modified.append(f)
    
    return {
        "added": sorted(added),
        "removed": sorted(removed),
        "modified": sorted(modified),
        "stats": {
            "added": len(added),
            "removed": len(removed),
            "modified": len(modified),
            "total_changes": len(added) + len(removed) + len(modified)
        }
    }


def generate_diff(old_context: Dict, new_context: Dict, format: str = "unified") -> str:
    """Generate human-readable diff between two contexts."""
    diff_result = compare_files(old_context, new_context)
    
    if format == "summary":
        return format_summary(diff_result)
    elif format == "json":
        return json.dumps(diff_result, indent=2)
    else:
        return format_summary(diff_result)


def format_summary(diff: Dict[str, Any]) -> str:
    """Format diff as human-readable summary."""
    lines = ["# DevContext Diff Summary", ""]
    
    stats = diff.get("stats", {})
    lines.append(f"**Total changes:** {stats.get('total_changes', 0)}")
    lines.append("")
    
    if diff.get("added"):
        lines.append(f"## ➕ Added ({len(diff['added'])})")
        for f in diff["added"][:20]:
            lines.append(f"  + {f}")
        if len(diff["added"]) > 20:
            lines.append(f"  ... and {len(diff['added']) - 20} more")
        lines.append("")
    
    if diff.get("removed"):
        lines.append(f"## ➖ Removed ({len(diff['removed'])})")
        for f in diff["removed"][:20]:
            lines.append(f"  - {f}")
        if len(diff["removed"]) > 20:
            lines.append(f"  ... and {len(diff['removed']) - 20} more")
        lines.append("")
    
    if diff.get("modified"):
        lines.append(f"## ✏️ Modified ({len(diff['modified'])})")
        for f in diff["modified"][:20]:
            lines.append(f"  ~ {f}")
        if len(diff["modified"]) > 20:
            lines.append(f"  ... and {len(diff['modified']) - 20} more")
        lines.append("")
    
    return "\n".join(lines)


def patch_context(original: Dict, diff_result: Dict) -> Dict:
    """Apply diff to create patched context."""
    patched = {
        "version": original.get("version", "0.1.0"),
        "generated": original.get("generated"),
        "files": dict(original.get("files", {})),
        "metadata": dict(original.get("metadata", {}))
    }
    
    # Remove deleted files
    for f in diff_result.get("removed", []):
        if f in patched["files"]:
            del patched["files"][f]
    
    # Note: Modified and added files need new content from new_context
    # This is a placeholder - full implementation would need file content
    
    return patched


# CLI integration
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Compare DevContext outputs")
    parser.add_argument("old", help="Old context file (JSON)")
    parser.add_argument("new", help="New context file (JSON)")
    parser.add_argument("-f", "--format", choices=["summary", "json"], default="summary",
                        help="Output format")
    
    args = parser.parse_args()
    
    try:
        with open(args.old) as f:
            old = json.load(f)
        with open(args.new) as f:
            new = json.load(f)
        
        diff = compare_files(old, new)
        
        if args.format == "json":
            print(json.dumps(diff, indent=2))
        else:
            print(format_summary(diff))
            
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        return 1
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON - {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())