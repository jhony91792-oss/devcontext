# Validation utilities for DevContext

import os
import re
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple


class ValidationError(Exception):
    """Validation error with details."""
    def __init__(self, message: str, errors: List[str] = None):
        super().__init__(message)
        self.errors = errors or []


def validate_path(path: str) -> Tuple[bool, Optional[str]]:
    """Validate that a path exists and is accessible."""
    try:
        p = Path(path)
        if not p.exists():
            return False, f"Path does not exist: {path}"
        if not os.access(p, os.R_OK):
            return False, f"Path is not readable: {path}"
        return True, None
    except Exception as e:
        return False, f"Invalid path: {e}"


def validate_output_format(format: str) -> bool:
    """Check if output format is supported."""
    return format in ["json", "md", "compact", "html"]


def validate_language(lang: str) -> bool:
    """Check if language is supported."""
    valid_langs = {
        "python", "javascript", "typescript", "go", "rust",
        "java", "c", "cpp", "csharp", "ruby", "php", "swift",
        "kotlin", "scala", "html", "css", "sql", "shell"
    }
    return lang.lower() in valid_langs


def validate_context_structure(context: Dict[str, Any]) -> List[str]:
    """Validate context dictionary structure. Returns list of errors."""
    errors = []
    
    required_fields = ["version", "files"]
    for field in required_fields:
        if field not in context:
            errors.append(f"Missing required field: {field}")
    
    if "files" in context:
        if not isinstance(context["files"], dict):
            errors.append("'files' must be a dictionary")
    
    if "metadata" in context:
        if not isinstance(context["metadata"], dict):
            errors.append("'metadata' must be a dictionary")
    
    return errors


def validate_file_extension(filename: str, allowed: List[str] = None) -> bool:
    """Check if file extension is allowed."""
    if allowed is None:
        return True  # Allow all if not specified
    
    ext = os.path.splitext(filename)[1].lower()
    return ext in [e.lower() if e.startswith(".") else f".{e.lower()}" for e in allowed]


def validate_gitignore_pattern(pattern: str) -> bool:
    """Check if a gitignore pattern is valid."""
    if not pattern or pattern.strip() == "":
        return False
    
    # Check for obviously invalid patterns
    if pattern.startswith("#"):
        return False  # Comment
    
    if pattern.startswith("!"):
        return False  # Negation (allowed but we skip for simplicity)
    
    return True


def validate_config(config: Dict[str, Any]) -> List[str]:
    """Validate configuration dictionary. Returns list of errors."""
    errors = []
    
    if "max_depth" in config:
        if not isinstance(config["max_depth"], int):
            errors.append("max_depth must be an integer")
        elif config["max_depth"] < 1:
            errors.append("max_depth must be at least 1")
        elif config["max_depth"] > 100:
            errors.append("max_depth must be at most 100")
    
    if "skip_dirs" in config:
        if not isinstance(config["skip_dirs"], list):
            errors.append("skip_dirs must be a list")
    
    if "include_hidden" in config:
        if not isinstance(config["include_hidden"], bool):
            errors.append("include_hidden must be a boolean")
    
    if "output_format" in config:
        if not validate_output_format(config["output_format"]):
            errors.append(f"Invalid output format: {config['output_format']}")
    
    return errors


def validate_project_structure(root: str) -> Dict[str, Any]:
    """
    Validate that a project has a reasonable structure.
    Returns validation result with issues found.
    """
    result = {
        "valid": True,
        "issues": [],
        "warnings": [],
        "has_readme": False,
        "has_git": False,
        "has_tests": False,
        "has_docs": False,
        "language": None
    }
    
    root_path = Path(root)
    
    # Check for README
    readme_candidates = ["README.md", "README.txt", "README.rst", "readme.md"]
    for candidate in readme_candidates:
        if (root_path / candidate).exists():
            result["has_readme"] = True
            break
    
    if not result["has_readme"]:
        result["warnings"].append("No README found")
    
    # Check for .git
    if (root_path / ".git").exists():
        result["has_git"] = True
    
    # Check for tests
    test_dirs = ["tests", "test", "spec", "__tests__"]
    for test_dir in test_dirs:
        if (root_path / test_dir).exists():
            result["has_tests"] = True
            break
    
    if not result["has_tests"]:
        result["warnings"].append("No test directory found")
    
    # Check for docs
    doc_dirs = ["docs", "doc", "documentation"]
    for doc_dir in doc_dirs:
        if (root_path / doc_dir).exists():
            result["has_docs"] = True
            break
    
    # Detect primary language
    extensions = {}
    for ext in ["py", "js", "ts", "go", "rs", "java", "rb", "php"]:
        count = len(list(root_path.rglob(f"*.{ext}")))
        if count > 0:
            extensions[ext] = count
    
    if extensions:
        result["language"] = max(extensions, key=extensions.get)
    
    # Overall validity
    if result["warnings"]:
        result["valid"] = False
    
    return result


# CLI validation command
def main():
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description="Validate DevContext output")
    parser.add_argument("path", nargs="?", default=".", help="Path to validate")
    parser.add_argument("--strict", action="store_true", help="Enable strict validation")
    
    args = parser.parse_args()
    
    # Validate path
    valid, error = validate_path(args.path)
    if not valid:
        print(f"❌ {error}")
        return 1
    
    # Check structure
    result = validate_project_structure(args.path)
    
    print("Project Validation Results:")
    print(f"  README: {'✅' if result['has_readme'] else '⚠️'}")
    print(f"  Git:    {'✅' if result['has_git'] else '⚠️'}")
    print(f"  Tests:  {'✅' if result['has_tests'] else '⚠️'}")
    print(f"  Docs:   {'✅' if result['has_docs'] else '⚠️'}")
    
    if result['language']:
        print(f"  Lang:   {result['language']}")
    
    if result['warnings']:
        print("\nWarnings:")
        for w in result['warnings']:
            print(f"  ⚠️ {w}")
    
    return 0


if __name__ == "__main__":
    exit(main() or 0)