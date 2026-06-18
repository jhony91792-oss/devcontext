# Output module for DevContext - output formatting

import json
from typing import Dict, Any, Optional


class OutputFormatter:
    """Format context output."""
    
    def __init__(self, context: Dict[str, Any]):
        self.context = context
    
    def to_json(self, pretty: bool = True) -> str:
        """Format as JSON."""
        if pretty:
            return json.dumps(self.context, indent=2)
        return json.dumps(self.context, separators=(',', ':'))
    
    def to_markdown(self) -> str:
        """Format as Markdown."""
        lines = ["# Code Context", ""]
        
        meta = self.context.get("metadata", {})
        files = self.context.get("files", {})
        
        lines.append(f"**Files:** {len(files)}")
        lines.append(f"**Languages:** {', '.join(meta.get('languages', []))}")
        lines.append("")
        
        lines.append("## Files")
        
        for path, info in sorted(files.items())[:50]:
            lines.append(f"\n### `{path}`")
            if isinstance(info, dict):
                if info.get("language"):
                    lines.append(f"- Language: {info['language']}")
                if info.get("functions"):
                    funcs = info["functions"][:5]
                    lines.append(f"- Functions: {', '.join(funcs)}")
                if info.get("classes"):
                    lines.append(f"- Classes: {', '.join(info['classes'][:5])}")
        
        if len(files) > 50:
            lines.append(f"\n*... and {len(files) - 50} more files*")
        
        return "\n".join(lines)
    
    def to_html(self) -> str:
        """Format as HTML."""
        md = self.to_markdown()
        
        # Simple markdown to HTML
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
    <title>DevContext Output</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; max-width: 900px; margin: 2rem auto; }}
        code {{ background: #f4f4f4; padding: 0.2rem; border-radius: 3px; }}
        pre {{ background: #f4f4f4; padding: 1rem; border-radius: 5px; }}
    </style>
</head>
<body>
{html}
</body>
</html>"""
    
    def to_compact(self) -> str:
        """Format as compact JSON."""
        return json.dumps(self.context, separators=(',', ':'))


def format_output(context: Dict[str, Any], format: str = "json") -> str:
    """Quick output formatting."""
    formatter = OutputFormatter(context)
    
    if format == "json":
        return formatter.to_json()
    elif format == "md" or format == "markdown":
        return formatter.to_markdown()
    elif format == "html":
        return formatter.to_html()
    elif format == "compact":
        return formatter.to_compact()
    
    return formatter.to_json()


# CLI
def main():
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description="Format DevContext output")
    parser.add_argument("-f", "--format", choices=["json", "md", "html", "compact"],
                        default="json")
    
    args = parser.parse_args()
    
    context = json.load(sys.stdin)
    formatter = OutputFormatter(context)
    
    if args.format == "json":
        print(formatter.to_json())
    elif args.format == "md":
        print(formatter.to_markdown())
    elif args.format == "html":
        print(formatter.to_html())
    elif args.format == "compact":
        print(formatter.to_compact())


if __name__ == "__main__":
    main()