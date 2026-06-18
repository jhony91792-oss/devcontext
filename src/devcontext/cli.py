# CLI module for DevContext

import sys
import argparse
from pathlib import Path


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="DevContext - Generate AI-ready context from codebases",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  devcontext generate .                  Generate context for current directory
  devcontext generate ./src -f json      Generate JSON output
  devcontext generate . -f compact       Generate compact for AI prompts
  devcontext tree .                      Show project structure
  devcontext parse main.py               Parse single file
  devcontext --version                   Show version
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # generate command
    gen_parser = subparsers.add_parser("generate", help="Generate context from codebase")
    gen_parser.add_argument("path", nargs="?", default=".", help="Directory to analyze")
    gen_parser.add_argument("-o", "--output", help="Output file")
    gen_parser.add_argument("-f", "--format", choices=["json", "md", "html", "compact"],
                           default="json", help="Output format")
    gen_parser.add_argument("--max-depth", type=int, default=10, help="Maximum depth")
    gen_parser.add_argument("-a", "--analyze", action="store_true", help="Enable analysis")
    gen_parser.add_argument("--no-stats", action="store_true", help="Hide stats")
    
    # tree command
    tree_parser = subparsers.add_parser("tree", help="Show project tree")
    tree_parser.add_argument("path", nargs="?", default=".", help="Directory to display")
    tree_parser.add_argument("-d", "--max-depth", type=int, default=10, help="Maximum depth")
    tree_parser.add_argument("--show-lang", action="store_true", help="Show language")
    
    # parse command
    parse_parser = subparsers.add_parser("parse", help="Parse single file")
    parse_parser.add_argument("file", help="File to parse")
    parse_parser.add_argument("-f", "--format", choices=["json", "text"], default="text")
    
    # config command
    config_parser = subparsers.add_parser("config", help="Configuration management")
    config_parser.add_argument("action", choices=["show", "set", "reset"], default="show")
    config_parser.add_argument("key", nargs="?", help="Config key")
    config_parser.add_argument("value", nargs="?", help="Config value")
    
    # plugins command
    plugins_parser = subparsers.add_parser("plugins", help="Plugin management")
    plugins_parser.add_argument("action", choices=["list", "init"], default="list")
    
    # version
    parser.add_argument("--version", action="version", version="DevContext 0.1.0")
    
    args = parser.parse_args()
    
    if args.command is None:
        # No subcommand, show help
        parser.print_help()
        return
    
    # Handle commands
    if args.command == "generate":
        from devcontext import DevContext
        dc = DevContext(args.path, max_depth=args.max_depth)
        context = dc.generate(format=args.format)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(context if isinstance(context, str) else str(context))
            print(f"Written to {args.output}")
        else:
            print(context if isinstance(context, str) else str(context))
    
    elif args.command == "tree":
        from devcontext.tree import get_tree_structure
        tree = get_tree_structure(args.path, args.max_depth)
        print(tree)
    
    elif args.command == "parse":
        from devcontext.parser import ParserManager
        manager = ParserManager()
        result = manager.parse(args.file)
        
        if args.format == "json":
            import json
            print(json.dumps(result, indent=2))
        else:
            print(f"Language: {result.get('language', 'unknown')}")
            if result.get('functions'):
                print(f"Functions: {', '.join(result['functions'][:10])}")
    
    elif args.command == "config":
        from devcontext.config import Config
        config = Config()
        
        if args.action == "show":
            import json
            if args.key:
                print(config.get(args.key))
            else:
                print(json.dumps(config.to_dict(), indent=2))
        
        elif args.action == "set":
            if args.key and args.value:
                config.set(args.key, args.value)
                config.save()
                print(f"Set {args.key} = {args.value}")
    
    elif args.command == "plugins":
        from devcontext.plugins import load_plugins
        manager = load_plugins()
        
        if args.action == "list":
            print(f"Loaded plugins: {len(manager.plugins)}")
            for p in manager.plugins:
                print(f"  - {p.name} v{p.version}")


if __name__ == "__main__":
    main()