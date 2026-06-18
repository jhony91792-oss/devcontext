# Git hooks integration for DevContext

import os
import sys
from pathlib import Path
from typing import Optional

GIT_HOOKS_DIR = ".git" + os.sep + "hooks"
HOOK_TEMPLATE = """#!/bin/bash
# DevContext hook - auto-generated
# Run: devcontext generate . -o .devcontext.json
devcontext generate . -o .devcontext.json
"""


def install_hook(hook_type: str = "pre-commit") -> bool:
    """Install DevContext git hook."""
    hook_path = Path(GIT_HOOKS_DIR) / hook_type
    
    try:
        hook_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(hook_path, 'w') as f:
            f.write(HOOK_TEMPLATE)
        
        # Make executable
        os.chmod(hook_path, 0o755)
        return True
    except OSError:
        return False


def uninstall_hook(hook_type: str = "pre-commit") -> bool:
    """Remove DevContext git hook."""
    hook_path = Path(GIT_HOOKS_DIR) / hook_type
    
    try:
        if hook_path.exists():
            hook_path.unlink()
        return True
    except OSError:
        return False


def is_hook_installed(hook_type: str = "pre-commit") -> bool:
    """Check if DevContext hook is installed."""
    hook_path = Path(GIT_HOOKS_DIR) / hook_type
    
    if not hook_path.exists():
        return False
    
    try:
        with open(hook_path) as f:
            content = f.read()
        return "devcontext generate" in content
    except OSError:
        return False


def install_all_hooks() -> dict:
    """Install hooks for common git events."""
    hooks = ["pre-commit", "pre-push", "post-checkout", "post-merge"]
    results = {}
    
    for hook in hooks:
        results[hook] = install_hook(hook)
    
    return results


def get_hook_status() -> dict:
    """Get status of all hooks."""
    hooks = ["pre-commit", "pre-push", "post-checkout", "post-merge"]
    results = {}
    
    for hook in hooks:
        results[hook] = {
            "installed": is_hook_installed(hook),
            "path": str(Path(GIT_HOOKS_DIR) / hook)
        }
    
    return results


# CLI integration
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Manage DevContext git hooks")
    sub = parser.add_subcommands()
    
    install_parser = sub.add_parser("install", help="Install hook")
    install_parser.add_argument("type", nargs="?", default="pre-commit", help="Hook type")
    
    uninstall_parser = sub.add_parser("uninstall", help="Uninstall hook")
    uninstall_parser.add_argument("type", nargs="?", default="pre-commit", help="Hook type")
    
    status_parser = sub.add_parser("status", help="Show hook status")
    
    args = parser.parse_args()
    
    if hasattr(args, 'type'):
        if args.command == "install":
            success = install_hook(args.type)
            print(f"{'✅' if success else '❌'} {'Installed' if success else 'Failed'} {args.type} hook")
        elif args.command == "uninstall":
            success = uninstall_hook(args.type)
            print(f"{'✅' if success else '❌'} {'Removed' if success else 'Failed'} {args.type} hook")
    else:
        status = get_hook_status()
        for hook, info in status.items():
            state = "✅ installed" if info["installed"] else "❌ not installed"
            print(f"  {hook}: {state}")


if __name__ == "__main__":
    main()