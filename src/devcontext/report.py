# Report generation module for DevContext

import json
from typing import Dict, Any, List
from datetime import datetime


def generate_summary_report(context: Dict[str, Any]) -> str:
    """Generate project summary report."""
    lines = [
        "=" * 60,
        "PROJECT SUMMARY REPORT",
        "=" * 60,
        ""
    ]
    
    meta = context.get("metadata", {})
    
    lines.append(f"Project: {meta.get('name', 'Unknown')}")
    lines.append(f"Generated: {datetime.now().isoformat()}")
    lines.append("")
    
    lines.append("## Metrics")
    lines.append(f"- Total Files: {meta.get('total_files', 0)}")
    lines.append(f"- Languages: {', '.join(meta.get('languages', []))}")
    lines.append(f"- Total Functions: {meta.get('total_functions', 'N/A')}")
    lines.append(f"- Total Classes: {meta.get('total_classes', 'N/A')}")
    lines.append("")
    
    return "\n".join(lines)


def generate_file_report(context: Dict[str, Any]) -> str:
    """Generate detailed file report."""
    lines = ["=" * 60, "FILE REPORT", "=" * 60, ""]
    
    files = context.get("files", {})
    
    # Sort by complexity
    file_scores = []
    for path, info in files.items():
        if isinstance(info, dict):
            score = len(info.get("functions", [])) + len(info.get("classes", [])) * 2
            file_scores.append((path, score, info))
    
    file_scores.sort(key=lambda x: x[1], reverse=True)
    
    lines.append(f"{'File':<40} {'Functions':<10} {'Classes':<10}")
    lines.append("-" * 60)
    
    for path, score, info in file_scores[:20]:
        funcs = len(info.get("functions", []))
        classes = len(info.get("classes", []))
        lines.append(f"{path:<40} {funcs:<10} {classes:<10}")
    
    return "\n".join(lines)


def generate_language_report(context: Dict[str, Any]) -> str:
    """Generate language distribution report."""
    files = context.get("files", {})
    
    lang_stats = {}
    for info in files.values():
        if isinstance(info, dict) and info.get("language"):
            lang = info["language"]
            if lang not in lang_stats:
                lang_stats[lang] = {"count": 0, "functions": 0, "classes": 0}
            lang_stats[lang]["count"] += 1
            lang_stats[lang]["functions"] += len(info.get("functions", []))
            lang_stats[lang]["classes"] += len(info.get("classes", []))
    
    lines = ["=" * 60, "LANGUAGE REPORT", "=" * 60, ""]
    lines.append(f"{'Language':<15} {'Files':<10} {'Functions':<12} {'Classes':<10}")
    lines.append("-" * 60)
    
    for lang in sorted(lang_stats.keys(), key=lambda x: lang_stats[x]["count"], reverse=True):
        stats = lang_stats[lang]
        lines.append(f"{lang:<15} {stats['count']:<10} {stats['functions']:<12} {stats['classes']:<10}")
    
    return "\n".join(lines)


def generate_full_report(context: Dict[str, Any]) -> str:
    """Generate complete report."""
    parts = [
        generate_summary_report(context),
        "",
        generate_file_report(context),
        "",
        generate_language_report(context),
    ]
    
    return "\n".join(parts)


# CLI
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate reports from context")
    parser.add_argument("input", help="Context JSON file")
    parser.add_argument("-t", "--type", choices=["summary", "files", "lang", "full"],
                        default="full", help="Report type")
    parser.add_argument("-o", "--output", help="Output file")
    
    args = parser.parse_args()
    
    with open(args.input) as f:
        context = json.load(f)
    
    if args.type == "summary":
        report = generate_summary_report(context)
    elif args.type == "files":
        report = generate_file_report(context)
    elif args.type == "lang":
        report = generate_language_report(context)
    else:
        report = generate_full_report(context)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"Report written to {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()