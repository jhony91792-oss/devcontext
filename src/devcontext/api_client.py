# API client module for DevContext - programmatic API

import json
from typing import Dict, Any, Optional, List


class DevContextClient:
    """Python API client for DevContext."""
    
    def __init__(self, path: str = ".", max_depth: int = 10):
        self.path = path
        self.max_depth = max_depth
    
    def generate(self, path: str = None, format: str = "json") -> Dict[str, Any]:
        """Generate context from path."""
        from devcontext import DevContext
        
        target = path or self.path
        dc = DevContext(target, max_depth=self.max_depth)
        
        return dc.generate(format=format)
    
    def search(self, context: Dict[str, Any], pattern: str, **kwargs) -> List[Dict[str, Any]]:
        """Search within context."""
        from devcontext.search import ContextSearch
        
        searcher = ContextSearch(context)
        return searcher.search_all(pattern, **kwargs)
    
    def compare(self, context1: Dict[str, Any], context2: Dict[str, Any]) -> Dict[str, Any]:
        """Compare two contexts."""
        from devcontext.diff import compare_contexts
        return compare_contexts(context1, context2)
    
    def merge(self, contexts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Merge multiple contexts."""
        from devcontext.merge import ContextMerger
        
        merger = ContextMerger()
        for ctx in contexts:
            merger.add_context(ctx)
        
        return merger.merge()
    
    def get_stats(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get statistics from context."""
        meta = context.get("metadata", {})
        files = context.get("files", {})
        
        total_funcs = sum(
            len(info.get("functions", [])) 
            for info in files.values() 
            if isinstance(info, dict)
        )
        
        total_classes = sum(
            len(info.get("classes", [])) 
            for info in files.values() 
            if isinstance(info, dict)
        )
        
        return {
            "total_files": len(files),
            "total_functions": total_funcs,
            "total_classes": total_classes,
            "languages": meta.get("languages", [])
        }


# CLI
def main():
    import argparse
    parser = argparse.ArgumentParser(description="DevContext Python client")
    parser.add_argument("command", choices=["generate", "search", "compare", "stats"])
    parser.add_argument("path", nargs="?", default=".", help="Path to analyze")
    
    args = parser.parse_args()
    
    client = DevContextClient()
    
    if args.command == "generate":
        result = client.generate(args.path)
        print(json.dumps(result, indent=2))
    
    elif args.command == "stats":
        context = client.generate(args.path)
        stats = client.get_stats(context)
        print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()