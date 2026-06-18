# Audit module for verifying DevContext installation

import os
import sys
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime


class AuditResult:
    """Result of an audit check."""
    
    def __init__(self, name: str, passed: bool, message: str = "", details: Any = None):
        self.name = name
        self.passed = passed
        self.message = message
        self.details = details
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "passed": self.passed,
            "message": self.message,
            "details": self.details
        }


def audit_filesystem(root: str = ".") -> List[AuditResult]:
    """Audit filesystem structure."""
    results = []
    root_path = Path(root)
    
    # Check critical files exist
    critical_files = [
        "README.md",
        "LICENSE",
        "pyproject.toml",
        "setup.py",
        "src/devcontext/__init__.py",
        "src/devcontext/cli.py",
    ]
    
    for f in critical_files:
        path = root_path / f
        results.append(AuditResult(
            f"File exists: {f}",
            path.exists(),
            "Found" if path.exists() else "Missing"
        ))
    
    return results


def audit_dependencies() -> List[AuditResult]:
    """Audit Python dependencies."""
    results = []
    
    # Check Python version
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    results.append(AuditResult(
        "Python version",
        sys.version_info >= (3, 8),
        f"Python {py_version} (requires 3.8+)"
    ))
    
    # Check critical imports
    critical_modules = ["json", "pathlib", "urllib", "re"]
    for module in critical_modules:
        try:
            __import__(module)
            results.append(AuditResult(f"Module: {module}", True, "Available"))
        except ImportError:
            results.append(AuditResult(f"Module: {module}", False, "Not available"))
    
    return results


def audit_github_integration() -> List[AuditResult]:
    """Audit GitHub-specific features."""
    results = []
    
    # Check if .git exists
    git_path = Path(".git")
    results.append(AuditResult(
        ".git directory",
        git_path.exists(),
        "Found" if git_path.exists() else "Not a git repository"
    ))
    
    # Check GitHub Actions
    actions_path = Path(".github/workflows")
    if actions_path.exists():
        workflows = list(actions_path.glob("*.yml")) + list(actions_path.glob("*.yaml"))
        results.append(AuditResult(
            "GitHub Actions",
            len(workflows) > 0,
            f"Found {len(workflows)} workflows"
        ))
    else:
        results.append(AuditResult(
            "GitHub Actions",
            False,
            "No workflows found"
        ))
    
    return results


def audit_permissions() -> List[AuditResult]:
    """Audit file permissions."""
    results = []
    
    # Check if we can write to current directory
    test_file = Path(".audit_test")
    try:
        test_file.touch()
        test_file.unlink()
        results.append(AuditResult("Write permission", True, "Can write to current directory"))
    except OSError:
        results.append(AuditResult("Write permission", False, "Cannot write to current directory"))
    
    # Check if CLI is executable
    cli_path = Path("src/devcontext/cli.py")
    if cli_path.exists():
        is_exec = os.access(cli_path, os.X_OK)
        results.append(AuditResult(
            "CLI executable",
            is_exec,
            "Executable" if is_exec else "Not executable (run chmod +x)"
        ))
    
    return results


def run_full_audit(root: str = ".") -> Dict[str, Any]:
    """Run complete audit."""
    all_results = []
    
    all_results.extend(audit_filesystem(root))
    all_results.extend(audit_dependencies())
    all_results.extend(audit_github_integration())
    all_results.extend(audit_permissions())
    
    passed = sum(1 for r in all_results if r.passed)
    failed = sum(1 for r in all_results if not r.passed)
    
    return {
        "timestamp": datetime.now().isoformat(),
        "total_checks": len(all_results),
        "passed": passed,
        "failed": failed,
        "score": (passed / len(all_results) * 100) if all_results else 0,
        "results": [r.to_dict() for r in all_results]
    }


def print_audit_report(audit: Dict[str, Any]):
    """Print audit report in human-readable format."""
    print("=" * 60)
    print("DEVCONTEXT AUDIT REPORT")
    print("=" * 60)
    print(f"Timestamp: {audit['timestamp']}")
    print(f"Score: {audit['score']:.1f}% ({audit['passed']}/{audit['total_checks']} passed)")
    print()
    
    current_category = None
    for result in audit['results']:
        # Extract category from name
        name = result['name']
        if ':' in name:
            category = name.split(':')[0]
        else:
            category = name
        
        if category != current_category:
            print(f"\n[{category}]")
            current_category = category
        
        status = "✅" if result['passed'] else "❌"
        print(f"  {status} {result['name']}: {result['message']}")
    
    print()
    print("=" * 60)
    if audit['failed'] == 0:
        print("🎉 All checks passed!")
    else:
        print(f"⚠️  {audit['failed']} checks failed")
    print("=" * 60)


# CLI
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Audit DevContext installation")
    parser.add_argument("-p", "--path", default=".", help="Path to audit")
    parser.add_argument("--json", action="store_true", help="JSON output")
    
    args = parser.parse_args()
    
    audit = run_full_audit(args.path)
    
    if args.json:
        print(json.dumps(audit, indent=2))
    else:
        print_audit_report(audit)
    
    return 0 if audit['failed'] == 0 else 1


if __name__ == "__main__":
    exit(main())