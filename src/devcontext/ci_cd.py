# Format converters for DevContext

import json
import base64
from typing import Dict, Any, Optional


def json_to_markdown(context: Dict[str, Any]) -> str:
    """Convert JSON context to Markdown."""
    lines = ["# Codebase Context", ""]
    
    meta = context.get("metadata", {})
    if meta:
        lines.append("## Summary")
        for key, value in meta.items():
            lines.append(f"- **{key}**: {value}")
        lines.append("")
    
    files = context.get("files", {})
    if files:
        lines.append("## Files")
        for path, info in sorted(files.items()):
            lines.append(f"### `{path}`")
            if isinstance(info, dict):
                if info.get("language"):
                    lines.append(f"- Language: {info['language']}")
                if info.get("functions"):
                    lines.append(f"- Functions: {', '.join(info['functions'][:5])}")
                if info.get("classes"):
                    lines.append(f"- Classes: {', '.join(info['classes'][:5])}")
            lines.append("")
    
    return "\n".join(lines)


def markdown_to_json(md: str) -> Dict[str, Any]:
    """Convert Markdown back to JSON (basic)."""
    # Simple conversion - just extract what we can
    return {
        "version": "0.1.0",
        "converted_from": "markdown",
        "content": md
    }


def json_to_html(context: Dict[str, Any], title: str = "Codebase Context") -> str:
    """Convert JSON context to HTML."""
    md = json_to_markdown(context)
    
    # Basic markdown to HTML
    html = md
    html = html.replace("# ", "<h1>").replace("\n# ", "</h1>\n<h1>")
    html = html.replace("## ", "<h2>").replace("\n## ", "</h2>\n<h2>")
    html = html.replace("### ", "<h3>").replace("\n### ", "</h3>\n<h3>")
    html = html.replace("**", "<strong>").replace("**", "</strong>")
    html = html.replace("- ", "<li>").replace("\n- ", "</li>\n<li>")
    
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
               max-width: 900px; margin: 0 auto; padding: 2rem; }}
        code {{ background: #f4f4f4; padding: 0.2rem 0.4rem; border-radius: 3px; }}
        pre {{ background: #f4f4f4; padding: 1rem; overflow-x: auto; border-radius: 5px; }}
        h1, h2, h3 {{ color: #333; margin-top: 1.5rem; }}
    </style>
</head>
<body>
{html}
</body>
</html>"""


def json_to_yaml(context: Dict[str, Any]) -> str:
    """Convert JSON context to YAML (approximate)."""
    import yaml
    return yaml.dump(context, default_flow_style=False)


def yaml_to_json(yaml_str: str) -> Dict[str, Any]:
    """Convert YAML string to JSON dict."""
    import yaml
    return yaml.safe_load(yaml_str)


def json_to_csv(context: Dict[str, Any]) -> str:
    """Convert JSON context to CSV."""
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


def compact_to_verbose(compact: str) -> Dict[str, Any]:
    """Convert compact format back to full JSON."""
    # Compact is just minified JSON
    return json.loads(compact)


def verbose_to_compact(context: Dict[str, Any]) -> str:
    """Convert full JSON to compact format."""
    return json.dumps(context, separators=(',', ':'))


# CLI
def main():
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description="Convert between formats")
    parser.add_argument("input", help="Input file")
    parser.add_argument("-f", "--from", dest="fmt_from", choices=["json", "md", "yaml", "csv"],
                        default="json")
    parser.add_argument("-t", "--to", dest="fmt_to", choices=["json", "md", "html", "yaml", "csv", "compact"],
                        default="md")
    parser.add_argument("-o", "--output", help="Output file")
    
    args = parser.parse_args()
    
    # Read input
    with open(args.input) as f:
        content = f.read()
    
    # Parse input
    if args.fmt_from == "json":
        data = json.loads(content)
    elif args.fmt_from == "yaml":
        import yaml
        data = yaml.safe_load(content)
    elif args.fmt_from == "md":
        data = markdown_to_json(content)
    else:
        data = {"content": content}
    
    # Convert
    if args.fmt_to == "json":
        output = json.dumps(data, indent=2)
    elif args.fmt_to == "md":
        output = json_to_markdown(data)
    elif args.fmt_to == "html":
        output = json_to_html(data)
    elif args.fmt_to == "yaml":
        output = json_to_yaml(data)
    elif args.fmt_to == "csv":
        output = json_to_csv(data)
    elif args.fmt_to == "compact":
        output = verbose_to_compact(data)
    
    # Output
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()