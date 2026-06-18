# Analyzer module for DevContext - code analysis

import os
import re
from pathlib import Path
from typing import Dict, Any, List, Optional


class Analyzer:
    """Analyze source code files."""
    
    def __init__(self):
        self.results: Dict[str, Dict[str, Any]] = {}
    
    def analyze_file(self, filepath: str) -> Dict[str, Any]:
        """Analyze a single file."""
        try:
            with open(filepath) as f:
                content = f.read()
            
            ext = Path(filepath).suffix.lower()
            result = {
                "path": filepath,
                "language": self._detect_language(ext),
                "lines": len(content.split("\n")),
                "size": len(content),
                "functions": self._extract_functions(content, ext),
                "classes": self._extract_classes(content, ext),
                "imports": self._extract_imports(content, ext),
            }
            
            return result
        except Exception as e:
            return {
                "path": filepath,
                "error": str(e)
            }
    
    def _detect_language(self, ext: str) -> str:
        """Detect programming language from extension."""
        lang_map = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".tsx": "typescript",
            ".java": "java",
            ".c": "c",
            ".cpp": "cpp",
            ".h": "c",
            ".hpp": "cpp",
            ".go": "go",
            ".rs": "rust",
            ".rb": "ruby",
            ".php": "php",
            ".swift": "swift",
            ".kt": "kotlin",
            ".cs": "csharp",
            ".m": "objectivec",
            ".mm": "objectivec",
        }
        return lang_map.get(ext, "unknown")
    
    def _extract_functions(self, content: str, ext: str) -> List[str]:
        """Extract function names."""
        functions = []
        
        if ext == ".py":
            for match in re.finditer(r'def\s+(\w+)', content):
                functions.append(match.group(1))
        
        elif ext in [".js", ".mjs"]:
            for match in re.finditer(r'function\s+(\w+)', content):
                functions.append(match.group(1))
            for match in re.finditer(r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>', content):
                functions.append(match.group(1))
        
        elif ext in [".ts", ".tsx"]:
            for match in re.finditer(r'(?:function|const)\s+(\w+)\s*[=\(]', content):
                functions.append(match.group(1))
        
        elif ext in [".java", ".kt"]:
            for match in re.finditer(r'(?:public|private|protected)?\s*(?:static)?\s*\w+\s+(\w+)\s*\(', content):
                functions.append(match.group(1))
        
        elif ext in [".go", ".rs"]:
            for match in re.finditer(r'func(?:tion)?\s+(\w+)', content):
                functions.append(match.group(1))
        
        elif ext in [".rb", ".php"]:
            for match in re.finditer(r'def\s+(\w+)', content):
                functions.append(match.group(1))
        
        return functions
    
    def _extract_classes(self, content: str, ext: str) -> List[str]:
        """Extract class names."""
        classes = []
        
        patterns = {
            ".py": r'class\s+(\w+)',
            ".js": r'class\s+(\w+)',
            ".ts": r'class\s+(\w+)',
            ".java": r'class\s+(\w+)',
            ".go": r'type\s+(\w+)\s+struct',
            ".rs": r'struct\s+(\w+)',
            ".rb": r'class\s+(\w+)',
            ".php": r'class\s+(\w+)',
        }
        
        pattern = patterns.get(ext)
        if pattern:
            for match in re.finditer(pattern, content):
                classes.append(match.group(1))
        
        return classes
    
    def _extract_imports(self, content: str, ext: str) -> List[str]:
        """Extract import statements."""
        imports = []
        
        if ext == ".py":
            for match in re.finditer(r'^(?:import|from)\s+[\w.]+', content, re.MULTILINE):
                imports.append(match.group(0))
        
        elif ext in [".js", ".ts", ".tsx"]:
            for match in re.finditer(r'^import\s+.+\s+from\s+[\'"](.+)[\'"]', content, re.MULTILINE):
                imports.append(match.group(1))
        
        elif ext == ".go":
            for match in re.finditer(r'^import\s+"([^"]+)"', content, re.MULTILINE):
                imports.append(match.group(1))
        
        return imports


# CLI
def main():
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description="Analyze code files")
    parser.add_argument("file", help="File to analyze")
    parser.add_argument("-j", "--json", action="store_true")
    
    args = parser.parse_args()
    
    analyzer = Analyzer()
    result = analyzer.analyze_file(args.file)
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"File: {result['path']}")
        print(f"Language: {result.get('language', 'unknown')}")
        print(f"Lines: {result.get('lines', 0)}")
        print(f"Functions: {len(result.get('functions', []))}")
        print(f"Classes: {len(result.get('classes', []))}")


if __name__ == "__main__":
    main()