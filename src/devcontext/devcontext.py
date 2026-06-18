# Main DevContext class

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional, List


class DevContext:
    """Main DevContext class for generating context from codebases."""
    
    def __init__(self, path: str = ".", max_depth: int = 10):
        self.path = Path(path)
        self.max_depth = max_depth
        self.ignore_patterns = [".git", "node_modules", "__pycache__", ".pyc", ".venv", ".venv39"]
    
    def generate(self, format: str = "json") -> Any:
        """Generate context from codebase."""
        context = self._build_context()
        
        if format == "json":
            return json.dumps(context, indent=2)
        elif format == "md" or format == "markdown":
            return self._to_markdown(context)
        elif format == "html":
            return self._to_html(context)
        elif format == "compact":
            return json.dumps(context, separators=(',', ':'))
        
        return context
    
    def _build_context(self) -> Dict[str, Any]:
        """Build context dictionary."""
        files = {}
        languages = set()
        total_files = 0
        
        for root, dirs, filenames in os.walk(self.path):
            # Filter directories
            dirs[:] = [d for d in dirs if not any(p in d for p in self.ignore_patterns)]
            
            # Check depth
            depth = root[len(str(self.path)):].count(os.sep)
            if depth >= self.max_depth:
                continue
            
            for filename in filenames:
                # Skip ignored
                if any(p in filename for p in self.ignore_patterns):
                    continue
                
                filepath = Path(root) / filename
                rel_path = str(filepath.relative_to(self.path))
                
                ext = filepath.suffix.lower()
                language = self._detect_language(ext)
                if language != "unknown":
                    languages.add(language)
                
                files[rel_path] = {
                    "language": language,
                    "size": filepath.stat().st_size if filepath.exists() else 0
                }
                
                total_files += 1
        
        return {
            "version": "0.1.0",
            "metadata": {
                "name": self.path.name,
                "total_files": total_files,
                "languages": sorted(list(languages))
            },
            "files": files
        }
    
    def _detect_language(self, ext: str) -> str:
        """Detect language from extension."""
        lang_map = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".jsx": "javascript",
            ".tsx": "typescript",
            ".java": "java",
            ".c": "c",
            ".cpp": "cpp",
            ".h": "c",
            ".go": "go",
            ".rs": "rust",
            ".rb": "ruby",
            ".php": "php",
            ".swift": "swift",
            ".kt": "kotlin",
            ".cs": "csharp",
            ".md": "markdown",
            ".json": "json",
            ".yaml": "yaml",
            ".yml": "yaml",
        }
        return lang_map.get(ext, "unknown")
    
    def _to_markdown(self, context: Dict[str, Any]) -> str:
        """Convert to markdown."""
        lines = ["# Code Context", ""]
        
        meta = context.get("metadata", {})
        files = context.get("files", {})
        
        lines.append(f"**Files:** {len(files)}")
        lines.append(f"**Languages:** {', '.join(meta.get('languages', []))}")
        lines.append("")
        lines.append("## Files")
        
        for path in sorted(files.keys()):
            lines.append(f"- `{path}`")
        
        return "\n".join(lines)
    
    def _to_html(self, context: Dict[str, Any]) -> str:
        """Convert to HTML."""
        md = self._to_markdown(context)
        
        html = md
        html = html.replace("# ", "<h1>").replace("\n# ", "</h1>\n<h1>")
        html = html.replace("## ", "<h2>").replace("\n## ", "</h2>\n<h2>")
        html = html.replace("**", "<strong>").replace("**", "</strong>")
        html = html.replace("- ", "<li>").replace("\n- ", "</li>\n<li>")
        
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>DevContext</title>
</head>
<body>{html}</body>
</html>"""


# Export main class
__all__ = ["DevContext"]