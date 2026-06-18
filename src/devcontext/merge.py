# Merge module for DevContext - merge multiple contexts

import json
from typing import Dict, Any, List, Optional
from pathlib import Path


class ContextMerger:
    """Merge multiple context files into one."""
    
    def __init__(self):
        self.contexts: List[Dict[str, Any]] = []
    
    def add_context(self, context: Dict[str, Any]):
        """Add a context to merge."""
        self.contexts.append(context)
    
    def add_from_file(self, filepath: str) -> bool:
        """Load and add context from file."""
        try:
            with open(filepath) as f:
                context = json.load(f)
            self.contexts.append(context)
            return True
        except Exception as e:
            print(f"Failed to load {filepath}: {e}")
            return False
    
    def merge(self) -> Dict[str, Any]:
        """Merge all contexts into one."""
        if not self.contexts:
            return {"error": "No contexts to merge"}
        
        # Start with first context
        merged = {
            "version": "0.1.0",
            "merged": True,
            "sources": len(self.contexts),
            "files": {},
            "metadata": {
                "total_files": 0,
                "languages": []
            }
        }
        
        all_languages = set()
        
        for context in self.contexts:
            files = context.get("files", {})
            
            for path, info in files.items():
                if path not in merged["files"]:
                    merged["files"][path] = info
                    
                    if isinstance(info, dict) and info.get("language"):
                        all_languages.add(info["language"])
            
            meta = context.get("metadata", {})
            if meta:
                merged["metadata"]["total_files"] += meta.get("total_files", 0)
        
        merged["metadata"]["languages"] = sorted(list(all_languages))
        
        return merged
    
    def merge_to_file(self, output_path: str) -> bool:
        """Merge and save to file."""
        try:
            merged = self.merge()
            with open(output_path, 'w') as f:
                json.dump(merged, f, indent=2)
            return True
        except Exception as e:
            print(f"Failed to write {output_path}: {e}")
            return False


def merge_contexts(files: List[str], output: str = None) -> Optional[Dict[str, Any]]:
    """Quick merge function."""
    merger = ContextMerger()
    
    for filepath in files:
        merger.add_from_file(filepath)
    
    if output:
        merger.merge_to_file(output)
        return None
    
    return merger.merge()


# CLI
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Merge DevContext files")
    parser.add_argument("files", nargs="+", help="Context files to merge")
    parser.add_argument("-o", "--output", help="Output file")
    
    args = parser.parse_args()
    
    merger = ContextMerger()
    
    for filepath in args.files:
        if merger.add_from_file(filepath):
            print(f"✅ Added {filepath}")
        else:
            print(f"❌ Failed to add {filepath}")
    
    if args.output:
        if merger.merge_to_file(args.output):
            print(f"\n✅ Merged to {args.output}")
    else:
        merged = merger.merge()
        print(json.dumps(merged, indent=2))


if __name__ == "__main__":
    main()