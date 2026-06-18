# Documentation generator for DevContext

import os
from pathlib import Path
from typing import Dict, Any, List, Optional


class DocGenerator:
    """Generate documentation from context."""
    
    def __init__(self, context: Dict[str, Any]):
        self.context = context
        self.files = context.get("files", {})
    
    def generate_api_docs(self) -> str:
        """Generate API documentation from context."""
        lines = ["# API Documentation", ""]
        
        for path, info in sorted(self.files.items()):
            if not isinstance(info, dict):
                continue
            
            lang = info.get("language", "unknown")
            
            lines.append(f"## `{path}`")
            lines.append(f"*Language: {lang}*")
            lines.append("")
            
            if info.get("functions"):
                lines.append("### Functions")
                for func in info["functions"]:
                    lines.append(f"- `{func}()`")
                lines.append("")
            
            if info.get("classes"):
                lines.append("### Classes")
                for cls in info["classes"]:
                    lines.append(f"- `{cls}`")
                lines.append("")
            
            if info.get("imports"):
                lines.append("### Imports")
                for imp in info["imports"][:10]:
                    lines.append(f"- `{imp}`")
                if len(info["imports"]) > 10:
                    lines.append(f"- ... and {len(info['imports']) - 10} more")
                lines.append("")
            
            lines.append("---")
            lines.append("")
        
        return "\n".join(lines)
    
    def generate_readme_section(self) -> str:
        """Generate project structure section for README."""
        lines = ["## Project Structure", ""]
        
        # Group files by directory
        dirs = {}
        for path in self.files.keys():
            parts = path.split("/")
            if len(parts) > 1:
                dir_name = parts[0]
                if dir_name not in dirs:
                    dirs[dir_name] = []
                dirs[dir_name].append("/".join(parts[1:]))
            else:
                if "." not in dirs:
                    dirs["."] = []
                dirs["."].append(path)
        
        for dir_name, files in sorted(dirs.items()):
            lines.append(f"### {dir_name}/")
            for f in sorted(files)[:10]:
                lines.append(f"- `{f}`")
            if len(files) > 10:
                lines.append(f"- ... and {len(files) - 10} more")
            lines.append("")
        
        return "\n".join(lines)
    
    def generate_index(self) -> str:
        """Generate documentation index."""
        lines = ["# Documentation Index", ""]
        
        modules = sorted(set(
            f.split("/")[0] for f in self.files.keys()
            if "/" in f
        ))
        
        lines.append("## Modules")
        for module in modules:
            lines.append(f"- [{module}](#{module})")
        
        lines.append("")
        lines.append("## Files")
        
        for path in sorted(self.files.keys()):
            lines.append(f"- `{path}`")
        
        return "\n".join(lines)
    
    def generate_all(self) -> Dict[str, str]:
        """Generate all documentation."""
        return {
            "api.md": self.generate_api_docs(),
            "structure.md": self.generate_readme_section(),
            "index.md": self.generate_index(),
        }


def generate_docs(context: Dict[str, Any], output_dir: str = "docs/generated") -> bool:
    """Generate all documentation files."""
    generator = DocGenerator(context)
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    docs = generator.generate_all()
    
    for filename, content in docs.items():
        (output_path / filename).write_text(content)
    
    return True


# CLI
def main():
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description="Generate documentation")
    parser.add_argument("input", help="Context JSON file")
    parser.add_argument("-o", "--output", default="docs/generated", help="Output directory")
    
    args = parser.parse_args()
    
    with open(args.input) as f:
        context = json.load(f)
    
    if generate_docs(context, args.output):
        print(f"Documentation generated in {args.output}/")


if __name__ == "__main__":
    main()