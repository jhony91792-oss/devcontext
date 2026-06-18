# Merge functionality for combining multiple context files

import json
from pathlib import Path
from typing import Dict, Any, List, Optional


def merge_contexts(contexts: List[Dict[str, Any]], strategy: str = "combine") -> Dict[str, Any]:
    """
    Merge multiple context dictionaries.
    
    Strategies:
    - "combine": Combine all files, deduplicate by path
    - " newest": Use newest version of each file
    - "largest": Use file with most content
    """
    if not contexts:
        return {}
    
    if len(contexts) == 1:
        return contexts[0]
    
    result = {
        "version": contexts[0].get("version", "0.1.0"),
        "generated": contexts[-1].get("generated"),
        "files": {},
        "metadata": contexts[0].get("metadata", {}).copy()
    }
    
    # Combine all files
    for ctx in contexts:
        ctx_files = ctx.get("files", {})
        for path, info in ctx_files.items():
            if path not in result["files"]:
                result["files"][path] = info
            elif strategy == "newest":
                # Use newer file (would need timestamps)
                result["files"][path] = info
            elif strategy == "largest":
                # Use larger content
                current = result["files"][path]
                if isinstance(info, dict) and isinstance(current, dict):
                    info_size = len(str(info.get("content", "")))
                    curr_size = len(str(current.get("content", "")))
                    if info_size > curr_size:
                        result["files"][path] = info
    
    # Merge metadata
    total_files = sum(m.get("total_files", 0) for m in [c.get("metadata", {}) for c in contexts])
    result["metadata"]["total_files"] = total_files
    
    return result


def merge_from_files(files: List[str], strategy: str = "combine") -> Dict[str, Any]:
    """Load contexts from files and merge them."""
    contexts = []
    
    for filepath in files:
        try:
            with open(filepath) as f:
                contexts.append(json.load(f))
        except (FileNotFoundError, json.JSONDecodeError):
            pass
    
    return merge_contexts(contexts, strategy)


def split_context(context: Dict[str, Any], chunk_size: int = 100) -> List[Dict[str, Any]]:
    """Split a large context into chunks."""
    files = context.get("files", {})
    paths = list(files.keys())
    
    chunks = []
    for i in range(0, len(paths), chunk_size):
        chunk_paths = paths[i:i + chunk_size]
        chunk_files = {p: files[p] for p in chunk_paths}
        
        chunk = {
            "version": context.get("version", "0.1.0"),
            "generated": context.get("generated"),
            "chunk": i // chunk_size + 1,
            "total_chunks": (len(paths) + chunk_size - 1) // chunk_size,
            "files": chunk_files,
            "metadata": {
                **context.get("metadata", {}),
                "chunk_files": len(chunk_files)
            }
        }
        chunks.append(chunk)
    
    return chunks


# CLI
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Merge DevContext files")
    parser.add_argument("files", nargs="+", help="Context files to merge")
    parser.add_argument("-o", "--output", help="Output file")
    parser.add_argument("-s", "--strategy", choices=["combine", "newest", "largest"],
                        default="combine", help="Merge strategy")
    
    args = parser.parse_args()
    
    result = merge_from_files(args.files, args.strategy)
    output = json.dumps(result, indent=2)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Merged to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()