"""DevContext CLI - Main entry point."""

import os
import sys
import argparse
from pathlib import Path

# Import all modules
from devcontext.tree import FileTree, scan_directory
from devcontext.parser import detect_language, parse_file
from devcontext.output import format_json, format_markdown, format_compact, format_html
from devcontext.analyzer import analyze_codebase
from devcontext import __version__


def generate_context(args):
    """Generate context for a codebase."""
    path = Path(args.path).resolve()
    
    if not path.exists():
        print(f"Error: Path '{path}' does not exist", file=sys.stderr)
        return 1
    
    # Scan directory
    tree = FileTree(path, max_depth=args.max_depth)
    nodes = tree.scan()
    
    # Parse files
    files = {}
    for node in nodes:
        if node['type'] == 'file':
            try:
                info = parse_file(node['path'])
                files[node['path']] = info
            except Exception:
                pass
    
    # Analyze if requested
    metadata = {
        'total_files': len(files),
        'languages': list(set(f.get('language') for f in files.values() if f.get('language'))),
    }
    
    if args.analyze:
        analysis = analyze_codebase({'files': files, 'metadata': metadata})
        metadata.update(analysis)
    
    context = {
        'version': __version__,
        'generated': str(Path(path).name),
        'files': files,
        'metadata': metadata,
    }
    
    # Format output
    if args.format == 'json':
        output = format_json(context)
    elif args.format == 'md':
        output = format_markdown(context)
    elif args.format == 'html':
        output = format_html(context)
    else:
        output = format_compact(context)
    
    # Write or print
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Context written to {args.output}")
    else:
        print(output)
    
    return 0


def show_tree(args):
    """Show file tree."""
    path = Path(args.path).resolve()
    
    if not path.exists():
        print(f"Error: Path '{path}' does not exist", file=sys.stderr)
        return 1
    
    tree = FileTree(path, max_depth=args.max_depth)
    nodes = tree.scan()
    
    for node in nodes:
        depth = node.get('depth', 0)
        indent = "  " * depth
        name = Path(node['path']).name
        if node['type'] == 'dir':
            print(f"{indent}📁 {name}/")
        else:
            lang = detect_language(node['path'])
            if args.show_lang:
                print(f"{indent}📄 {name} ({lang})")
            else:
                print(f"{indent}📄 {name}")
    
    return 0


def parse_single_file(args):
    """Parse a single file."""
    path = Path(args.file).resolve()
    
    if not path.exists():
        print(f"Error: File '{path}' does not exist", file=sys.stderr)
        return 1
    
    info = parse_file(path)
    
    if args.format == 'json':
        print(format_json({'files': {str(path): info}}))
    else:
        print(f"Language: {info.get('language', 'unknown')}")
        print(f"Lines: {info.get('lines', 0)}")
        if info.get('functions'):
            print(f"\nFunctions ({len(info['functions'])}):")
            for f in info['functions'][:10]:
                print(f"  - {f}")
        if info.get('classes'):
            print(f"\nClasses ({len(info['classes'])}):")
            for c in info['classes'][:10]:
                print(f"  - {c}")
        if info.get('imports'):
            print(f"\nImports ({len(info['imports'])}):")
            for imp in info['imports'][:10]:
                print(f"  - {imp}")
    
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="DevContext - AI-Ready Context Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  devcontext generate . -f compact
  devcontext tree . --max-depth 3
  devcontext parse main.py

For more help: https://github.com/jhony91792-oss/devcontext
        """
    )
    
    parser.add_argument("--version", action="version", version=f"DevContext {__version__}")
    
    sub = parser.add_subparsers(dest="command", help="Commands")
    
    # generate command
    gen = sub.add_parser("generate", help="Generate context for a codebase")
    gen.add_argument("path", nargs="?", default=".", help="Project path (default: .)")
    gen.add_argument("-o", "--output", help="Output file")
    gen.add_argument("-f", "--format", choices=["json", "md", "html", "compact"],
                     default="json", help="Output format")
    gen.add_argument("--max-depth", type=int, default=10, help="Max directory depth")
    gen.add_argument("--no-stats", dest="stats", action="store_false", default=True,
                     help="Don't show statistics")
    gen.add_argument("-a", "--analyze", action="store_true", help="Enable code analysis")
    
    # tree command
    tree = sub.add_parser("tree", help="Show project file tree")
    tree.add_argument("path", nargs="?", default=".", help="Project path (default: .)")
    tree.add_argument("--max-depth", type=int, default=10, help="Max directory depth")
    tree.add_argument("--show-lang", action="store_true", help="Show language per file")
    
    # parse command
    parse = sub.add_parser("parse", help="Parse a single file")
    parse.add_argument("file", help="File to parse")
    parse.add_argument("-f", "--format", choices=["json", "text"],
                       default="text", help="Output format")
    
    args = parser.parse_args()
    
    if args.command == "generate":
        return generate_context(args)
    elif args.command == "tree":
        return show_tree(args)
    elif args.command == "parse":
        return parse_single_file(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main() or 0)