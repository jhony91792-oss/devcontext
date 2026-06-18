# Parser module for DevContext - language-specific parsing

import os
import re
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable


class BaseParser:
    """Base class for language parsers."""
    
    extensions: List[str] = []
    
    def parse(self, filepath: str, content: str) -> Dict[str, Any]:
        """Parse file content."""
        return {
            "language": self.__class__.__name__,
            "functions": [],
            "classes": [],
            "imports": []
        }


class PythonParser(BaseParser):
    """Python source code parser."""
    
    extensions = [".py"]
    
    def parse(self, filepath: str, content: str) -> Dict[str, Any]:
        """Parse Python file."""
        result = {
            "language": "python",
            "functions": [],
            "classes": [],
            "imports": [],
            "decorators": []
        }
        
        lines = content.split("\n")
        
        for line in lines:
            stripped = line.strip()
            
            # Imports
            if stripped.startswith("import ") or stripped.startswith("from "):
                match = re.match(r'(?:from\s+([\w.]+)\s+)?import\s+(.+)', stripped)
                if match:
                    result["imports"].append(stripped)
            
            # Classes
            class_match = re.match(r'class\s+(\w+)', stripped)
            if class_match:
                result["classes"].append(class_match.group(1))
            
            # Functions
            func_match = re.match(r'def\s+(\w+)', stripped)
            if func_match:
                result["functions"].append(func_match.group(1))
            
            # Decorators
            if stripped.startswith("@"):
                result["decorators"].append(stripped)
        
        return result


class JavaScriptParser(BaseParser):
    """JavaScript source code parser."""
    
    extensions = [".js", ".mjs"]
    
    def parse(self, filepath: str, content: str) -> Dict[str, Any]:
        """Parse JavaScript file."""
        result = {
            "language": "javascript",
            "functions": [],
            "classes": [],
            "imports": []
        }
        
        # Functions
        func_patterns = [
            r'function\s+(\w+)',
            r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>',
            r'(\w+)\s*:\s*function\s*\(',
        ]
        
        for pattern in func_patterns:
            for match in re.finditer(pattern, content):
                result["functions"].append(match.group(1))
        
        # Classes
        for match in re.finditer(r'class\s+(\w+)', content):
            result["classes"].append(match.group(1))
        
        # Imports
        for match in re.finditer(r'import\s+.+\s+from\s+[\'"](.+)[\'"]', content):
            result["imports"].append(match.group(1))
        
        return result


class TypeScriptParser(BaseParser):
    """TypeScript source code parser."""
    
    extensions = [".ts", ".tsx"]
    
    def parse(self, filepath: str, content: str) -> Dict[str, Any]:
        """Parse TypeScript file."""
        result = {
            "language": "typescript",
            "functions": [],
            "classes": [],
            "interfaces": [],
            "imports": []
        }
        
        # Functions
        for match in re.finditer(r'(?:function|const)\s+(\w+)\s*[=\(]', content):
            result["functions"].append(match.group(1))
        
        # Classes
        for match in re.finditer(r'class\s+(\w+)', content):
            result["classes"].append(match.group(1))
        
        # Interfaces
        for match in re.finditer(r'interface\s+(\w+)', content):
            result["interfaces"].append(match.group(1))
        
        # Imports
        for match in re.finditer(r'import\s+.+\s+from\s+[\'"](.+)[\'"]', content):
            result["imports"].append(match.group(1))
        
        return result


class ParserManager:
    """Manage all parsers."""
    
    def __init__(self):
        self.parsers: Dict[str, BaseParser] = {}
        self._register_default_parsers()
    
    def _register_default_parsers(self):
        """Register default parsers."""
        self.register(PythonParser())
        self.register(JavaScriptParser())
        self.register(TypeScriptParser())
    
    def register(self, parser: BaseParser):
        """Register a parser."""
        for ext in parser.extensions:
            self.parsers[ext] = parser
    
    def get_parser(self, filepath: str) -> Optional[BaseParser]:
        """Get parser for file."""
        ext = Path(filepath).suffix.lower()
        return self.parsers.get(ext)
    
    def parse(self, filepath: str) -> Dict[str, Any]:
        """Parse a file."""
        parser = self.get_parser(filepath)
        
        if not parser:
            return {"language": "unknown"}
        
        try:
            with open(filepath) as f:
                content = f.read()
            return parser.parse(filepath, content)
        except:
            return {"language": "unknown", "error": "Failed to parse"}


# CLI
def main():
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description="Parse source files")
    parser.add_argument("file", help="File to parse")
    parser.add_argument("-j", "--json", action="store_true")
    
    args = parser.parse_args()
    
    manager = ParserManager()
    result = manager.parse(args.file)
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Language: {result.get('language', 'unknown')}")
        if result.get('functions'):
            print(f"Functions: {', '.join(result['functions'][:10])}")
        if result.get('classes'):
            print(f"Classes: {', '.join(result['classes'][:10])}")


if __name__ == "__main__":
    main()