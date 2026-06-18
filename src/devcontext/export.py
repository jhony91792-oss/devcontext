# Export module for DevContext - export in various formats

import json
from typing import Dict, Any, List, Optional


def export_to_json(context: Dict[str, Any], pretty: bool = True) -> str:
    """Export to JSON."""
    if pretty:
        return json.dumps(context, indent=2)
    return json.dumps(context, separators=(',', ':'))


def export_to_markdown(context: Dict[str, Any]) -> str:
    """Export to Markdown format."""
    lines = ["# Project Context", ""]
    
    meta = context.get("metadata", {})
    files = context.get("files", {})
    
    # Summary
    lines.append("## Summary")
    lines.append(f"- **Project**: {meta.get('name', 'Unknown')}")
    lines.append(f"- **Files**: {meta.get('total_files', len(files))}")
    lines.append(f"- **Languages**: {', '.join(meta.get('languages', []))}")
    lines.append("")
    
    # Files
    lines.append("## Files")
    for path in sorted(files.keys())[:50]:
        info = files[path]
        lines.append(f"### `{path}`")
        if isinstance(info, dict):
            if info.get("language"):
                lines.append(f"- Language: {info['language']}")
            if info.get("functions"):
                lines.append(f"- Functions: {', '.join(info['functions'][:5])}")
            if info.get("classes"):
                lines.append(f"- Classes: {', '.join(info['classes'][:5])}")
        lines.append("")
    
    if len(files) > 50:
        lines.append(f"*... and {len(files) - 50} more files*")
    
    return "\n".join(lines)


def export_to_html(context: Dict[str, Any], title: str = "Project Context") -> str:
    """Export to HTML format."""
    md = export_to_markdown(context)
    
    # Simple markdown to HTML conversion
    html = md
    html = html.replace("# ", "<h1>").replace("\n# ", "</h1>\n<h1>")
    html = html.replace("## ", "<h2>").replace("\n## ", "</h2>\n<h2>")
    html = html.replace("### ", "<h3>").replace("\n### ", "</h3>\n<h3>")
    html = html.replace("**", "<strong>").replace("**", "</strong>")
    html = html.replace("- ", "<li>").replace("\n- ", "</li>\n<li>")
    html = html.replace("\n\n", "</li>\n\n<li>")
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
               max-width: 900px; margin: 0 auto; padding: 2rem; line-height: 1.6; }}
        code {{ background: #f4f4f4; padding: 0.2rem 0.4rem; border-radius: 3px; font-size: 0.9em; }}
        pre {{ background: #f4f4f4; padding: 1rem; border-radius: 5px; overflow-x: auto; }}
        h1, h2, h3 {{ color: #333; margin-top: 1.5rem; }}
        li {{ margin: 0.5rem 0; }}
    </style>
</head>
<body>
{html}
</body>
</html>"""


def export_to_text(context: Dict[str, Any]) -> str:
    """Export to plain text format."""
    lines = ["PROJECT CONTEXT", "=" * 50, ""]
    
    meta = context.get("metadata", {})
    files = context.get("files", {})
    
    lines.append(f"Project: {meta.get('name', 'Unknown')}")
    lines.append(f"Files: {meta.get('total_files', len(files))}")
    lines.append(f"Languages: {', '.join(meta.get('languages', []))}")
    lines.append("")
    lines.append("FILES:")
    lines.append("-" * 50)
    
    for path in sorted(files.keys()):
        lines.append(path)
    
    return "\n".join(lines)


def export_to_csv(context: Dict[str, Any]) -> str:
    """Export to CSV format."""
    files = context.get("files", {})
    
    lines = ["path,language,functions,classes,lines"]
    
    for path, info in sorted(files.items()):
        if isinstance(info, dict):
            lang = info.get("language", "")
            funcs = len(info.get("functions", []))
            classes = len(info.get("classes", []))
            lines_count = info.get("lines", 0)
            lines.append(f'"{path}",{lang},{funcs},{classes},{lines_count}')
    
    return "\n".join(lines)


def export_to_compact(context: Dict[str, Any]) -> str:
    """Export to compact JSON format."""
    return json.dumps(context, separators=(',', ':'))


# CLI
def main():
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description="Export context to various formats")
    parser.add_argument("input", nargs="?", help="Input context file (or stdin)")
    parser.add_argument("-f", "--format", choices=["json", "md", "html", "txt", "csv", "compact"],
                        default="md", help="Export format")
    parser.add_argument("-o", "--output", help="Output file")
    parser.add_argument("--title", default="Project Context", help="HTML title")
    
    args = parser.parse_args()
    
    # Read input
    if args.input:
        with open(args.input) as f:
            context = json.load(f)
    else:
        context = json.load(sys.stdin)
    
    # Export
    if args.format == "json":
        output = export_to_json(context)
    elif args.format == "md":
        output = export_to_markdown(context)
    elif args.format == "html":
        output = export_to_html(context, args.title)
    elif args.format == "txt":
        output = export_to_text(context)
    elif args.format == "csv":
        output = export_to_csv(context)
    elif args.format == "compact":
        output = export_to_compact(context)
    
    # Write output
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Exported to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()