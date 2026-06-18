# Visualization module for DevContext - generate charts/graphs

import json
from typing import Dict, Any, List, Optional


def generate_language_chart(context: Dict[str, Any]) -> str:
    """Generate ASCII chart of language distribution."""
    files = context.get("files", {})
    
    lang_counts = {}
    for info in files.values():
        if isinstance(info, dict) and info.get("language"):
            lang = info["language"]
            lang_counts[lang] = lang_counts.get(lang, 0) + 1
    
    if not lang_counts:
        return "No language data"
    
    total = sum(lang_counts.values())
    lines = ["Language Distribution:", ""]
    
    for lang, count in sorted(lang_counts.items(), key=lambda x: x[1], reverse=True):
        pct = (count / total) * 100
        bars = "█" * int(pct / 3)
        lines.append(f"  {lang:15} {count:3} ({pct:5.1f}%) {bars}")
    
    return "\n".join(lines)


def generate_complexity_chart(context: Dict[str, Any]) -> str:
    """Generate chart of file complexities."""
    files = context.get("files", {})
    
    complexities = []
    for path, info in files.items():
        if isinstance(info, dict):
            funcs = len(info.get("functions", []))
            classes = len(info.get("classes", []))
            complexity = funcs + (classes * 2)
            if complexity > 0:
                complexities.append((path, complexity))
    
    if not complexities:
        return "No complexity data"
    
    lines = ["Complexity Hotspots:", ""]
    
    for path, complexity in sorted(complexities, key=lambda x: x[1], reverse=True)[:15]:
        bars = "█" * min(complexity, 20)
        filename = path.split("/")[-1]
        lines.append(f"  {filename:20} {bars} ({complexity})")
    
    return "\n".join(lines)


def generate_file_size_chart(context: Dict[str, Any]) -> str:
    """Generate chart of file sizes."""
    files = context.get("files", {})
    
    sizes = []
    for path, info in files.items():
        if isinstance(info, dict):
            lines = info.get("lines", 0)
            if lines > 0:
                sizes.append((path, lines))
    
    if not sizes:
        return "No size data"
    
    max_size = max(s for _, s in sizes)
    
    lines = ["File Sizes:", ""]
    
    for path, size in sorted(sizes, key=lambda x: x[1], reverse=True)[:15]:
        pct = size / max_size if max_size > 0 else 0
        bars = "█" * int(pct * 30)
        filename = path.split("/")[-1]
        lines.append(f"  {filename:20} {bars} ({size} lines)")
    
    return "\n".join(lines)


def generate_structure_tree(context: Dict[str, Any], max_depth: int = 3) -> str:
    """Generate ASCII tree of project structure."""
    files = context.get("files", {})
    
    # Build tree
    tree = {}
    for path in files.keys():
        parts = path.split("/")
        node = tree
        for part in parts:
            if part not in node:
                node[part] = {}
            node = node[part]
    
    lines = ["Project Structure:", ""]
    
    def print_tree(node: Dict, prefix: str = "", depth: int = 0):
        indent = "  " * depth
        keys = sorted(node.keys())
        for i, key in enumerate(keys):
            is_last = i == len(keys) - 1
            connector = "└── " if is_last else "├── "
            lines.append(f"{prefix}{connector}{key}/")
            
            if depth < max_depth and node[key]:
                extension = "    " if is_last else "│   "
                print_tree(node[key], prefix + extension, depth + 1)
    
    print_tree(tree)
    
    return "\n".join(lines)


def generate_summary_dashboard(context: Dict[str, Any]) -> str:
    """Generate complete dashboard."""
    lines = [
        "=" * 60,
        "DEVCONTEXT ANALYSIS DASHBOARD",
        "=" * 60,
        "",
    ]
    
    meta = context.get("metadata", {})
    
    lines.append(f"Files:      {meta.get('total_files', 0)}")
    lines.append(f"Languages:  {', '.join(meta.get('languages', []))}")
    lines.append(f"Functions:  {meta.get('total_functions', 'N/A')}")
    lines.append(f"Classes:    {meta.get('total_classes', 'N/A')}")
    lines.append("")
    
    lines.append(generate_language_chart(context))
    lines.append("")
    lines.append(generate_complexity_chart(context))
    lines.append("")
    lines.append("=" * 60)
    
    return "\n".join(lines)


# CLI
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Visualize DevContext output")
    parser.add_argument("file", help="Context JSON file")
    parser.add_argument("-t", "--type", choices=["lang", "complex", "size", "tree", "full"],
                        default="full", help="Chart type")
    
    args = parser.parse_args()
    
    with open(args.file) as f:
        context = json.load(f)
    
    if args.type == "lang":
        print(generate_language_chart(context))
    elif args.type == "complex":
        print(generate_complexity_chart(context))
    elif args.type == "size":
        print(generate_file_size_chart(context))
    elif args.type == "tree":
        print(generate_structure_tree(context))
    else:
        print(generate_summary_dashboard(context))


if __name__ == "__main__":
    main()