# Hooks module for DevContext - git integration hooks

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional


class GitHooks:
    """Git hooks integration."""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.hooks_dir = self.repo_path / ".git" / "hooks"
    
    def is_git_repo(self) -> bool:
        """Check if directory is a git repository."""
        return (self.repo_path / ".git").exists()
    
    def install_hook(self, hook_name: str, script: str) -> bool:
        """Install a git hook."""
        if not self.is_git_repo():
            return False
        
        self.hooks_dir.mkdir(parents=True, exist_ok=True)
        hook_path = self.hooks_dir / hook_name
        
        with open(hook_path, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write(script)
        
        os.chmod(hook_path, 0o755)
        return True
    
    def install_pre_commit(self) -> bool:
        """Install pre-commit hook."""
        script = '''#!/bin/bash
# DevContext pre-commit hook
devcontext generate . -o .devcontext.json
git add .devcontext.json
'''
        return self.install_hook("pre-commit", script)
    
    def install_post_commit(self) -> bool:
        """Install post-commit hook."""
        script = '''#!/bin/bash
# DevContext post-commit hook
if [ -f .devcontext.json ]; then
    devcontext generate . -o .devcontext.json
fi
'''
        return self.install_hook("post-commit", script)
    
    def install_all(self) -> Dict[str, bool]:
        """Install all hooks."""
        return {
            "pre-commit": self.install_pre_commit(),
            "post-commit": self.install_post_commit(),
        }
    
    def remove_hook(self, hook_name: str) -> bool:
        """Remove a hook."""
        hook_path = self.hooks_dir / hook_name
        if hook_path.exists():
            hook_path.unlink()
            return True
        return False
    
    def list_hooks(self) -> List[str]:
        """List installed hooks."""
        if not self.hooks_dir.exists():
            return []
        return [f.name for f in self.hooks_dir.iterdir() if f.is_file()]


# CLI
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Git hooks for DevContext")
    sub = parser.add_subparsers(dest="command")
    
    install_cmd = sub.add_parser("install", help="Install hooks")
    install_cmd.add_argument("-t", "--type", choices=["pre-commit", "post-commit", "all"],
                             default="all")
    
    remove_cmd = sub.add_parser("remove", help="Remove hook")
    remove_cmd.add_argument("name")
    
    list_cmd = sub.add_parser("list", help="List installed hooks")
    
    args = parser.parse_args()
    
    hooks = GitHooks()
    
    if args.command == "install":
        if args.type == "all":
            results = hooks.install_all()
            for name, success in results.items():
                print(f"{'✅' if success else '❌'} {name}")
        else:
            if args.type == "pre-commit":
                success = hooks.install_pre_commit()
            else:
                success = hooks.install_post_commit()
            print(f"{'✅' if success else '❌'} {args.type}")
    
    elif args.command == "remove":
        if hooks.remove_hook(args.name):
            print(f"Removed {args.name}")
        else:
            print(f"Hook {args.name} not found")
    
    elif args.command == "list":
        hook_list = hooks.list_hooks()
        print(f"Installed hooks: {len(hook_list)}")
        for h in hook_list:
            print(f"  - {h}")


if __name__ == "__main__":
    main()