# Diff module for comparing contexts

import json
from typing import Dict, Any, List


def compare_contexts(context1: Dict[str, Any], context2: Dict[str, Any]) -> Dict[str, Any]:
    """Compare two contexts and return differences."""
    files1 = set(context1.get("files", {}).keys())
    files2 = set(context2.get("files", {}).keys())
    
    added = files2 - files1
    removed = files1 - files2
    common = files1 & files2
    
    # Compare common files
    modified = []
    for path in common:
        info1 = context1["files"][path]
        info2 = context2["files"][path]
        
        if info1 != info2:
            modified.append(path)
    
    return {
        "added": list(added),
        "removed": list(removed),
        "modified": modified,
        "stats": {
            "added_count": len(added),
            "removed_count": len(removed),
            "modified_count": len(modified),
            "total_changes": len(added) + len(removed) + len(modified)
        }
    }


def generate_diff_report(context1: Dict[str, Any], context2: Dict[str, Any]) -> str:
    """Generate a human-readable diff report."""
    diff = compare_contexts(context1, context2)
    
    lines = [
        "=" * 60,
        "CONTEXT DIFF REPORT",
        "=" * 60,
        "",
        f"Added:     {diff['stats']['added_count']}",
        f"Removed:   {diff['stats']['removed_count']}",
        f"Modified:  {diff['stats']['modified_count']}",
        "",
    ]
    
    if diff["added"]:
        lines.append("Added files:")
        for path in diff["added"][:10]:
            lines.append(f"  + {path}")
        if len(diff["added"]) > 10:
            lines.append(f"  ... and {len(diff['added']) - 10} more")
        lines.append("")
    
    if diff["removed"]:
        lines.append("Removed files:")
        for path in diff["removed"][:10]:
            lines.append(f"  - {path}")
        if len(diff["removed"]) > 10:
            lines.append(f"  ... and {len(diff['removed']) - 10} more")
        lines.append("")
    
    if diff["modified"]:
        lines.append("Modified files:")
        for path in diff["modified"][:10]:
            lines.append(f"  M {path}")
        if len(diff["modified"]) > 10:
            lines.append(f"  ... and {len(diff['modified']) - 10} more")
    
    return "\n".join(lines)


# CLI
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Compare context files")
    parser.add_argument("file1", help="First context file")
    parser.add_argument("file2", help="Second context file")
    parser.add_argument("-o", "--output", help="Output file")
    parser.add_argument("-j", "--json", action="store_true", help="JSON output")
    
    args = parser.parse_args()
    
    with open(args.file1) as f:
        context1 = json.load(f)
    
    with open(args.file2) as f:
        context2 = json.load(f)
    
    if args.json:
        output = json.dumps(compare_contexts(context1, context2), indent=2)
    else:
        output = generate_diff_report(context1, context2)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()