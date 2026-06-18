#!/usr/bin/env python3
"""
DevContext CLI — AI-Ready Codebase Context Generator

Usage:
    devcontext generate <path> [--output FILE] [--format json|md|compact]
    devcontext tree <path> [--max-depth N]
    devcontext parse <path> [--files GLOB]
    devcontext --version
"""

import argparse
import json
import sys
from pathlib import Path

from devcontext import __version__
from devcontext.tree import FileTree, scan_directory
from devcontext.parser import parse_file, detect_language
from devcontext.output import format_json, format_markdown, format_compact


def generate_context(root: Path, max_depth: int = 5) -> dict:
    """Generate full context for a codebase."""
    # Scan file tree
    tree = FileTree(root, max_depth)
    nodes = tree.scan()
    
    # Parse key source files
    structure = {}
    key_content = {}
    
    for node in nodes:
        if node['type'] != 'file':
            continue
        
        fpath = root / node['path']
        if not fpath.exists():
            continue
        
        # Parse source files
        ext = node.get('ext', '')
        if ext in {'.py', '.js', '.ts', '.go', '.rs', '.java', '.rb', '.php'}:
            parsed = parse_file(fpath)
            structure[node['path']] = {
                'language': parsed.get('language'),
                'functions': parsed.get('functions', [])[:20],  # Limit per file
                'classes': parsed.get('classes', []),
                'imports': parsed.get('imports', [])[:10],
            }
        
        # Extract key file content
        key_files = {'README.md', 'pyproject.toml', 'setup.py', 'package.json', 
                     'Cargo.toml', 'go.mod', 'requirements.txt', 'Dockerfile'}
        if node['path'] in key_files:
            try:
                content = fpath.read_text(encoding='utf-8', errors='replace')
                key_content[node['path']] = {
                    'type': node['path'].split('.')[-1],
                    'preview': content[:2000]
                }
            except Exception:
                pass
    
    # Count files by language
    lang_counts = {}
    for path, info in structure.items():
        lang = info.get('language', 'unknown')
        lang_counts[lang] = lang_counts.get(lang, 0) + 1
    
    return {
        'tool': 'DevContext',
        'version': __version__,
        'root': str(root),
        'file_tree': nodes,
        'structure': structure,
        'key_files': key_content,
        'summary': {
            'total_files': len([n for n in nodes if n['type'] == 'file']),
            'total_dirs': len([n for n in nodes if n['type'] == 'dir']),
            'by_language': lang_counts,
        }
    }


def cmd_generate(args: argparse.Namespace):
    """Generate context command."""
    if not args.path.exists():
        print(f"Error: Path not found: {args.path}", file=sys.stderr)
        sys.exit(1)
    
    ctx = generate_context(args.path, max_depth=args.max_depth)
    
    if args.format == 'json':
        output = format_json(ctx)
    elif args.format == 'compact':
        output = format_compact(ctx)
    else:
        output = format_markdown(ctx)
    
    if args.output:
        args.output.write_text(output)
        print(f"✅ Context saved to {args.output}")
    else:
        print(output)


def cmd_tree(args: argparse.Namespace):
    """Show file tree command."""
    if not args.path.exists():
        print(f"Error: Path not found: {args.path}", file=sys.stderr)
        sys.exit(1)
    
    tree = FileTree(args.path, args.max_depth)
    nodes = tree.scan()
    
    for node in nodes:
        indent = "  " * node.get('depth', 0)
        if node['type'] == 'dir':
            print(f"{indent}📁 {node['path']}/")
        else:
            print(f"{indent}📄 {node['path']}")


def cmd_parse(args: argparse.Namespace):
    """Parse files command."""
    if not args.path.exists():
        print(f"Error: Path not found: {args.path}", file=sys.stderr)
        sys.exit(1)
    
    if args.path.is_file():
        result = parse_file(args.path)
        print(json.dumps(result, indent=2))
    else:
        # Parse all files in directory
        nodes = scan_directory(args.path, max_depth=args.max_depth)
        files = [args.path / n['path'] for n in nodes if n['type'] == 'file']
        
        results = []
        for f in files[:50]:  # Limit to 50 files
            result = parse_file(f)
            results.append({
                'path': result['path'],
                'language': result.get('language'),
                'functions': result.get('functions', [])[:10],
                'classes': result.get('classes', []),
            })
        
        print(json.dumps(results, indent=2))


def main():
    parser = argparse.ArgumentParser(
        prog="devcontext",
        description="🔮 DevContext — AI-Ready Codebase Context Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  devcontext generate .                    Generate context for current directory
  devcontext generate . -o context.json    Save to file
  devcontext generate . -f md              Output as Markdown
  devcontext tree . --max-depth 3          Show file tree only
  devcontext parse . --files "*.py"        Parse Python files
        """
    )
    
    parser.add_argument('--version', action='store_true', help='Show version')
    
    sub = parser.add_subparsers(dest='command', help='Commands')
    
    # generate command
    gen = sub.add_parser('generate', help='Generate context from codebase')
    gen.add_argument('path', type=Path, help='Path to codebase')
    gen.add_argument('-o', '--output', type=Path, help='Output file')
    gen.add_argument('-f', '--format', choices=['json', 'md', 'compact'], 
                     default='json', help='Output format')
    gen.add_argument('--max-depth', type=int, default=5, help='Max tree depth')
    gen.set_defaults(func=cmd_generate)
    
    # tree command
    tree = sub.add_parser('tree', help='Show file tree')
    tree.add_argument('path', type=Path, help='Path to codebase')
    tree.add_argument('--max-depth', type=int, default=5, help='Max depth')
    tree.set_defaults(func=cmd_tree)
    
    # parse command
    parse = sub.add_parser('parse', help='Parse code structure')
    parse.add_argument('path', type=Path, help='Path to file or directory')
    parse.add_argument('--files', help='File filter (e.g. "*.py")')
    parse.add_argument('--max-depth', type=int, default=5, help='Max depth')
    parse.set_defaults(func=cmd_parse)
    
    args = parser.parse_args()
    
    if args.version:
        print(f"DevContext v{__version__}")
        return
    
    if args.command is None:
        parser.print_help()
        return
    
    args.func(args)


if __name__ == '__main__':
    main()