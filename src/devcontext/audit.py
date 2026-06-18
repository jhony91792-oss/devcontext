# Audit module for DevContext - check installation health

import os
import sys
import json
import subprocess
from typing import Dict, Any, List


class AuditChecker:
    """Check DevContext installation health."""
    
    def __init__(self):
        self.issues: List[Dict[str, Any]] = []
        self.checks: List[Dict[str, Any]] = []
    
    def check_python_version(self) -> bool:
        """Check Python version."""
        version = sys.version_info
        is_valid = version.major >= 3 and version.minor >= 8
        
        self.checks.append({
            "name": "Python Version",
            "status": "pass" if is_valid else "fail",
            "message": f"Python {version.major}.{version.minor}.{version.micro}"
        })
        
        return is_valid
    
    def check_devcontext_installed(self) -> bool:
        """Check if DevContext is installed."""
        try:
            result = subprocess.run(
                ["devcontext", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            is_installed = result.returncode == 0
            
            self.checks.append({
                "name": "DevContext Installed",
                "status": "pass" if is_installed else "fail",
                "message": result.stdout.strip() if is_installed else "Not found"
            })
            
            return is_installed
        except:
            self.checks.append({
                "name": "DevContext Installed",
                "status": "fail",
                "message": "Not found"
            })
            return False
    
    def check_dependencies(self) -> bool:
        """Check required dependencies."""
        required = ["json", "pathlib", "urllib", "hashlib"]
        all_present = True
        
        for dep in required:
            present = dep in sys.modules or dep in dir(__builtins__)
            if not present:
                all_present = False
                self.issues.append(f"Missing dependency: {dep}")
        
        self.checks.append({
            "name": "Dependencies",
            "status": "pass" if all_present else "fail",
            "message": "All present" if all_present else "Some missing"
        })
        
        return all_present
    
    def check_permissions(self) -> bool:
        """Check file permissions."""
        home = os.path.expanduser("~")
        config_dir = os.path.join(home, ".config", "devcontext")
        
        try:
            os.makedirs(config_dir, exist_ok=True)
            is_writable = os.access(config_dir, os.W_OK)
            
            self.checks.append({
                "name": "Config Directory",
                "status": "pass" if is_writable else "warn",
                "message": config_dir
            })
            
            return is_writable
        except:
            self.checks.append({
                "name": "Config Directory",
                "status": "fail",
                "message": "Cannot create config directory"
            })
            return False
    
    def run_all_checks(self) -> Dict[str, Any]:
        """Run all audit checks."""
        self.checks = []
        self.issues = []
        
        self.check_python_version()
        self.check_devcontext_installed()
        self.check_dependencies()
        self.check_permissions()
        
        passed = sum(1 for c in self.checks if c["status"] == "pass")
        failed = sum(1 for c in self.checks if c["status"] == "fail")
        warnings = sum(1 for c in self.checks if c["status"] == "warn")
        
        return {
            "total_checks": len(self.checks),
            "passed": passed,
            "failed": failed,
            "warnings": warnings,
            "checks": self.checks,
            "issues": self.issues
        }


def run_audit() -> Dict[str, Any]:
    """Run full audit."""
    checker = AuditChecker()
    return checker.run_all_checks()


# CLI
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Audit DevContext installation")
    parser.add_argument("-j", "--json", action="store_true", help="JSON output")
    
    args = parser.parse_args()
    
    result = run_audit()
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("DevContext Audit")
        print("=" * 50)
        print(f"Checks: {result['total_checks']}")
        print(f"  ✅ Passed: {result['passed']}")
        print(f"  ❌ Failed: {result['failed']}")
        print(f"  ⚠️  Warnings: {result['warnings']}")
        print()
        
        for check in result["checks"]:
            status_icon = "✅" if check["status"] == "pass" else "❌" if check["status"] == "fail" else "⚠️"
            print(f"{status_icon} {check['name']}: {check['message']}")
        
        if result["issues"]:
            print("\nIssues:")
            for issue in result["issues"]:
                print(f"  - {issue}")


if __name__ == "__main__":
    main()