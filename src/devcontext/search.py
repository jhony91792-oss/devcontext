# Search module for DevContext - search within context

import json
import re
from typing import Dict, Any, List, Optional


class ContextSearch:
    """Search within DevContext data."""
    
    def __init__(self, context: Dict[str, Any]):
        self.context = context
        self.files = context.get("files", {})
    
    def search_files(self, pattern: str, regex: bool = False) -> List[Dict[str, Any]]:
        """Search for files matching pattern."""
        results = []
        
        if regex:
            compiled = re.compile(pattern)
            for path in self.files:
                if compiled.search(path):
                    results.append({
                        "type": "file",
                        "path": path,
                        "match": path
                    })
        else:
            pattern_lower = pattern.lower()
            for path in self.files:
                if pattern_lower in path.lower():
                    results.append({
                        "type": "file",
                        "path": path,
                        "match": path
                    })
        
        return results
    
    def search_functions(self, pattern: str, regex: bool = False) -> List[Dict[str, Any]]:
        """Search for functions matching pattern."""
        results = []
        
        for path, info in self.files.items():
            if not isinstance(info, dict):
                continue
            
            funcs = info.get("functions", [])
            for func in funcs:
                if regex:
                    if re.search(pattern, func):
                        results.append({
                            "type": "function",
                            "file": path,
                            "name": func,
                            "match": func
                        })
                else:
                    if pattern.lower() in func.lower():
                        results.append({
                            "type": "function",
                            "file": path,
                            "name": func,
                            "match": func
                        })
        
        return results
    
    def search_classes(self, pattern: str, regex: bool = False) -> List[Dict[str, Any]]:
        """Search for classes matching pattern."""
        results = []
        
        for path, info in self.files.items():
            if not isinstance(info, dict):
                continue
            
            classes = info.get("classes", [])
            for cls in classes:
                if regex:
                    if re.search(pattern, cls):
                        results.append({
                            "type": "class",
                            "file": path,
                            "name": cls,
                            "match": cls
                        })
                else:
                    if pattern.lower() in cls.lower():
                        results.append({
                            "type": "class",
                            "file": path,
                            "name": cls,
                            "match": cls
                        })
        
        return results
    
    def search_all(self, pattern: str, regex: bool = False) -> List[Dict[str, Any]]:
        """Search everywhere."""
        results = []
        results.extend(self.search_files(pattern, regex))
        results.extend(self.search_functions(pattern, regex))
        results.extend(self.search_classes(pattern, regex))
        return results


def search_context(context: Dict[str, Any], pattern: str, **kwargs) -> List[Dict[str, Any]]:
    """Quick search function."""
    searcher = ContextSearch(context)
    return searcher.search_all(pattern, **kwargs)


# CLI
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Search DevContext")
    parser.add_argument("pattern", help="Search pattern")
    parser.add_argument("-f", "--files", action="store_true", help="Search files")
    parser.add_argument("-F", "--functions", action="store_true", help="Search functions")
    parser.add_argument("-C", "--classes", action="store_true", help="Search classes")
    parser.add_argument("-r", "--regex", action="store_true", help="Use regex")
    parser.add_argument("input", help="Context JSON file")
    
    args = parser.parse_args()
    
    with open(args.input) as f:
        context = json.load(f)
    
    searcher = ContextSearch(context)
    
    search_files = args.files or not (args.functions or args.classes)
    search_funcs = args.functions or not (args.files or args.classes)
    search_classes = args.classes or not (args.files or args.functions)
    
    results = []
    
    if search_files:
        results.extend(searcher.search_files(args.pattern, args.regex))
    if search_funcs:
        results.extend(searcher.search_functions(args.pattern, args.regex))
    if search_classes:
        results.extend(searcher.search_classes(args.pattern, args.regex))
    
    print(f"Found {len(results)} results:")
    for r in results[:20]:
        print(f"  [{r['type']}] {r.get('file', '')}: {r['name']}")
    
    if len(results) > 20:
        print(f"  ... and {len(results) - 20} more")


if __name__ == "__main__":
    main()