# Migration module - import from similar tools

import json
from typing import Dict, Any, List, Optional


# Mapping of other tool contexts to DevContext format
TOOL_MAPPINGS = {
    "copilot-context": {
        "version": "0.1.0",
        "files": {},
        "metadata": {}
    }
}


def migrate_copilot(context: Dict[str, Any]) -> Dict[str, Any]:
    """Migrate Copilot Context format to DevContext."""
    return {
        "version": "0.1.0",
        "generated": context.get("generated"),
        "files": context.get("files", {}),
        "metadata": {
            "migrated_from": "copilot-context",
            **context.get("metadata", {})
        }
    }


def migrate_from_file(filepath: str, source_format: str) -> Optional[Dict[str, Any]]:
    """Migrate context from another tool."""
    try:
        with open(filepath) as f:
            content = json.load(f)
        
        if source_format == "copilot":
            return migrate_copilot(content)
        else:
            # Generic migration - assume same structure
            return content
    except Exception:
        return None


def detect_format(context: Dict[str, Any]) -> str:
    """Detect source format of context."""
    if "files" in context and "metadata" in context:
        return "devcontext"
    if "sourceFiles" in context:
        return "copilot"
    if "tree" in context:
        return "tree-sitter"
    return "unknown"


def convert_to_devcontext(context: Dict[str, Any]) -> Dict[str, Any]:
    """Convert any format to DevContext format."""
    detected = detect_format(context)
    
    if detected == "devcontext":
        return context
    elif detected == "copilot":
        return migrate_copilot(context)
    else:
        # Return as-is with version marker
        return {
            "version": "0.1.0",
            "migrated_from": detected,
            **context
        }


# CLI
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Migrate context from other tools")
    parser.add_argument("file", help="Context file to migrate")
    parser.add_argument("-f", "--from", dest="source", choices=["copilot", "tree-sitter", "auto"],
                        default="auto", help="Source format")
    parser.add_argument("-o", "--output", help="Output file")
    
    args = parser.parse_args()
    
    with open(args.file) as f:
        content = json.load(f)
    
    if args.source == "auto":
        result = convert_to_devcontext(content)
    else:
        result = migrate_from_file(args.file, args.source)
    
    if result:
        output = json.dumps(result, indent=2)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"Migrated to {args.output}")
        else:
            print(output)
    else:
        print("Migration failed")


if __name__ == "__main__":
    main()