# Git integration module for DevContext

import subprocess
import json
from pathlib import Path
from typing import Dict, Any, List, Optional


class GitIntegration:
    """Git integration utilities."""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
    
    def is_git_repo(self) -> bool:
        """Check if directory is a git repository."""
        return (self.repo_path / ".git").exists()
    
    def get_current_branch(self) -> Optional[str]:
        """Get current branch name."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout.strip() if result.returncode == 0 else None
        except:
            return None
    
    def get_recent_commits(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get recent commits."""
        try:
            result = subprocess.run(
                ["git", "log", f"-{count}", "--pretty=format:%H|%s|%an|%ad", "--date=iso"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            commits = []
            for line in result.stdout.strip().split("\n"):
                if "|" in line:
                    parts = line.split("|")
                    if len(parts) >= 4:
                        commits.append({
                            "hash": parts[0][:7],
                            "message": parts[1],
                            "author": parts[2],
                            "date": parts[3]
                        })
            
            return commits
        except:
            return []
    
    def get_diff(self, ref: str = "HEAD") -> str:
        """Get diff of uncommitted changes."""
        try:
            result = subprocess.run(
                ["git", "diff", ref],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout
        except:
            return ""
    
    def get_changed_files(self) -> List[str]:
        """Get list of changed files."""
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            return [f for f in result.stdout.strip().split("\n") if f]
        except:
            return []
    
    def generate_git_context(self) -> Dict[str, Any]:
        """Generate git-specific context."""
        return {
            "branch": self.get_current_branch(),
            "recent_commits": self.get_recent_commits(5),
            "changed_files": self.get_changed_files(),
            "has_uncommitted": bool(self.get_changed_files())
        }


# CLI
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Git integration")
    sub = parser.add_subparsers(dest="command")
    
    branch_cmd = sub.add_parser("branch", help="Show current branch")
    
    commits_cmd = sub.add_parser("commits", help="Show recent commits")
    commits_cmd.add_argument("-n", type=int, default=10)
    
    diff_cmd = sub.add_parser("diff", help="Show uncommitted changes")
    
    status_cmd = sub.add_parser("status", help="Git context summary")
    
    args = parser.parse_args()
    
    git = GitIntegration()
    
    if args.command == "branch":
        branch = git.get_current_branch()
        print(f"Current branch: {branch}")
    
    elif args.command == "commits":
        commits = git.get_recent_commits(args.n)
        for c in commits:
            print(f"{c['hash']} | {c['message'][:50]} | {c['author']}")
    
    elif args.command == "diff":
        print(git.get_diff())
    
    elif args.command == "status":
        ctx = git.generate_git_context()
        print(json.dumps(ctx, indent=2))


if __name__ == "__main__":
    main()