# Security utilities for DevContext

import hashlib
import re
from typing import Dict, Any, List, Set


class SecurityScanner:
    """Scan for security issues in code."""
    
    def __init__(self):
        self.issues: List[Dict[str, Any]] = []
        
        # Patterns for common vulnerabilities
        self.patterns = {
            "hardcoded_secret": [
                (r'password\s*=\s*["\'][^"\']+["\']', "Hardcoded password"),
                (r'api[_-]?key\s*=\s*["\'][^"\']+["\']', "Hardcoded API key"),
                (r'secret\s*=\s*["\'][^"\']+["\']', "Hardcoded secret"),
                (r'token\s*=\s*["\'][^"\']{20,}["\']', "Potential hardcoded token"),
            ],
            "sql_injection": [
                (r'execute\s*\(\s*["\'].*%s', "Potential SQL injection"),
                (r'"\s*\+\s*["\'].*SELECT', "Potential SQL injection"),
            ],
            "command_injection": [
                (r'os\.system\s*\(', "Shell command injection risk"),
                (r'subprocess\.call\s*\(\s*shell\s*=\s*True', "Shell command injection risk"),
            ],
            "path_traversal": [
                (r'open\s*\(\s*[^,]+ \+ ', "Potential path traversal"),
            ],
            "eval_usage": [
                (r'\beval\s*\(', "Use of eval() is dangerous"),
                (r'\bexec\s*\(', "Use of exec() is dangerous"),
            ],
        }
    
    def scan_file(self, filepath: str, content: str) -> List[Dict[str, Any]]:
        """Scan a single file for security issues."""
        issues = []
        
        for category, patterns in self.patterns.items():
            for pattern, message in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    issues.append({
                        "file": filepath,
                        "category": category,
                        "message": message,
                        "pattern": pattern
                    })
        
        return issues
    
    def scan_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Scan context for security issues."""
        all_issues = []
        
        files = context.get("files", {})
        for path, info in files.items():
            if isinstance(info, dict) and "content" in info:
                issues = self.scan_file(path, info["content"])
                all_issues.extend(issues)
        
        return {
            "total_issues": len(all_issues),
            "by_category": self._group_by_category(all_issues),
            "issues": all_issues
        }
    
    def _group_by_category(self, issues: List[Dict[str, Any]]) -> Dict[str, int]:
        """Group issues by category."""
        categories = {}
        for issue in issues:
            cat = issue["category"]
            categories[cat] = categories.get(cat, 0) + 1
        return categories


def scan_security(context: Dict[str, Any]) -> Dict[str, Any]:
    """Quick security scan."""
    scanner = SecurityScanner()
    return scanner.scan_context(context)


# CLI
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Security scanner")
    parser.add_argument("file", help="File or context JSON to scan")
    
    args = parser.parse_args()
    
    if args.file.endswith(".json"):
        import json
        with open(args.file) as f:
            context = json.load(f)
        result = scan_security(context)
        print(json.dumps(result, indent=2))
    else:
        with open(args.file) as f:
            content = f.read()
        scanner = SecurityScanner()
        issues = scanner.scan_file(args.file, content)
        print(f"Found {len(issues)} issues:")
        for issue in issues:
            print(f"  [{issue['category']}] {issue['message']}")


if __name__ == "__main__":
    main()