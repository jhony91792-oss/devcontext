# Search module for DevContext - search within codebase

import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Pattern


class CodeSearcher:
    """Search within code files."""
    
    def __init__(self, root: str = "."):
        self.root = Path(root).resolve()
        self.results = []
    
    def search_content(self, pattern: str, 
                       file_types: Optional[List[str]] = None,
                       case_sensitive: bool = False) -> List[Dict[str, Any]]:
        """Search for pattern in file contents."""
        results = []
        
        if file_types is None:
            file_types = ['.py', '.js', '.ts', '.go', '.rs', '.java', '.rb', '.php']
        
        flags = 0 if case_sensitive else re.IGNORECASE
        compiled: Pattern = re.compile(pattern, flags)
        
        for path in self.root.rglob('*'):
            if path.is_file() and any(str(path).endswith(ext) for ext in file_types):
                try:
                    content = path.read_text(errors='ignore')
                    for i, line in enumerate(content.split('\n'), 1):
                        if compiled.search(line):
                            results.append({
                                'file': str(path.relative_to(self.root)),
                                'line': i,
                                'text': line.strip(),
                                'path': str(path)
                            })
                except Exception:
                    pass
        
        self.results = results
        return results
    
    def search_by_name(self, pattern: str) -> List[str]:
        """Search for files by name pattern."""
        results = []
        flags = 0 if pattern.islower() else re.IGNORECASE
        compiled = re.compile(pattern, flags)
        
        for path in self.root.rglob('*'):
            if path.is_file() and compiled.search(path.name):
                results.append(str(path.relative_to(self.root)))
        
        return results
    
    def find_functions(self, name: str = None) -> List[Dict[str, Any]]:
        """Find all function definitions, optionally filtered by name."""
        from devcontext.parser import parse_file, extract_structure
        
        results = []
        
        for path in self.root.rglob('*.py'):
            try:
                info = parse_file(path)
                for func in info.get('functions', []):
                    if name is None or name.lower() in func.lower():
                        results.append({
                            'file': str(path.relative_to(self.root)),
                            'function': func
                        })
            except Exception:
                pass
        
        return results
    
    def find_classes(self, name: str = None) -> List[Dict[str, Any]]:
        """Find all class definitions, optionally filtered by name."""
        from devcontext.parser import parse_file
        
        results = []
        
        for path in self.root.rglob('*.py'):
            try:
                info = parse_file(path)
                for cls in info.get('classes', []):
                    if name is None or name.lower() in cls.lower():
                        results.append({
                            'file': str(path.relative_to(self.root)),
                            'class': cls
                        })
            except Exception:
                pass
        
        return results


def search_codebase(pattern: str, root: str = ".") -> List[Dict[str, Any]]:
    """Quick search function."""
    searcher = CodeSearcher(root)
    return searcher.search_content(pattern)


# CLI
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Search DevContext codebase")
    parser.add_argument("pattern", help="Pattern to search")
    parser.add_argument("-r", "--root", default=".", help="Root directory")
    parser.add_argument("-t", "--type", help="File types (comma-separated)")
    parser.add_argument("-i", "--case-insensitive", action="store_true")
    parser.add_argument("-n", "--name-only", action="store_true")
    
    args = parser.parse_args()
    
    searcher = CodeSearcher(args.root)
    
    if args.name_only:
        results = searcher.search_by_name(args.pattern)
        for r in results:
            print(r)
    else:
        file_types = args.type.split(',') if args.type else None
        results = searcher.search_content(args.pattern, file_types, not args.case_insensitive)
        
        for r in results:
            print(f"{r['file']}:{r['line']}: {r['text'][:80]}")
    
    print(f"\nFound {len(results)} matches")


if __name__ == "__main__":
    main()