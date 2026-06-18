# Validation module for DevContext

import json
import re
from typing import Dict, Any, List, Tuple, Optional
from pathlib import Path


class ValidationError:
    """Represents a validation error."""
    
    def __init__(self, code: str, message: str, severity: str = "error"):
        self.code = code
        self.message = message
        self.severity = severity
    
    def __repr__(self):
        return f"[{self.severity.upper()}] {self.code}: {self.message}"


class ContextValidator:
    """Validate context data."""
    
    def __init__(self):
        self.errors: List[ValidationError] = []
        self.warnings: List[ValidationError] = []
    
    def validate(self, context: Dict[str, Any]) -> Tuple[bool, List[ValidationError]]:
        """Validate a context object."""
        self.errors = []
        self.warnings = []
        
        # Check required fields
        if "version" not in context:
            self.errors.append(ValidationError("MISSING_VERSION", "Context is missing 'version' field"))
        
        if "files" not in context:
            self.errors.append(ValidationError("MISSING_FILES", "Context is missing 'files' field"))
        elif not isinstance(context["files"], dict):
            self.errors.append(ValidationError("INVALID_FILES", "'files' must be a dictionary"))
        
        # Check files
        if "files" in context:
            self._validate_files(context["files"])
        
        # Check metadata
        if "metadata" in context:
            self._validate_metadata(context["metadata"])
        
        is_valid = len(self.errors) == 0
        return is_valid, self.errors + self.warnings
    
    def _validate_files(self, files: Dict[str, Any]):
        """Validate files section."""
        if not files:
            self.warnings.append(ValidationError("EMPTY_FILES", "No files in context", "warning"))
            return
        
        for path, info in files.items():
            if not isinstance(path, str):
                self.errors.append(ValidationError("INVALID_PATH", f"File path must be string: {path}"))
            
            if not isinstance(info, dict):
                self.warnings.append(
                    ValidationError("INVALID_FILE_INFO", f"File info for '{path}' should be a dict", "warning")
                )
    
    def _validate_metadata(self, metadata: Dict[str, Any]):
        """Validate metadata section."""
        if "total_files" in metadata:
            if not isinstance(metadata["total_files"], int):
                self.errors.append(ValidationError("INVALID_TOTAL_FILES", "'total_files' must be an integer"))
        
        if "languages" in metadata:
            if not isinstance(metadata["languages"], list):
                self.errors.append(ValidationError("INVALID_LANGUAGES", "'languages' must be a list"))
    
    def validate_file_path(self, path: str) -> bool:
        """Check if file path is safe."""
        # Prevent path traversal
        if ".." in path:
            self.errors.append(ValidationError("PATH_TRAVERSAL", f"Path contains '..': {path}"))
            return False
        
        # Check for absolute paths
        if path.startswith("/"):
            self.warnings.append(
                ValidationError("ABSOLUTE_PATH", f"Path is absolute: {path}", "warning")
            )
        
        return True


def validate_context(context: Dict[str, Any]) -> Tuple[bool, List[ValidationError]]:
    """Quick validation of context."""
    validator = ContextValidator()
    return validator.validate(context)


def is_valid_json(text: str) -> bool:
    """Check if text is valid JSON."""
    try:
        json.loads(text)
        return True
    except:
        return False


# CLI
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Validate DevContext output")
    parser.add_argument("file", help="Context JSON file to validate")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show all errors/warnings")
    
    args = parser.parse_args()
    
    with open(args.file) as f:
        context = json.load(f)
    
    validator = ContextValidator()
    is_valid, issues = validator.validate(context)
    
    if is_valid:
        print("✅ Context is valid")
    else:
        print("❌ Context has errors:")
        for issue in issues:
            if issue.severity == "error":
                print(f"  ❌ {issue.code}: {issue.message}")
    
    if args.verbose:
        warnings = [i for i in issues if i.severity == "warning"]
        if warnings:
            print(f"\n⚠️  Warnings ({len(warnings)}):")
            for warning in warnings:
                print(f"  ⚠️ {warning.code}: {warning.message}")


if __name__ == "__main__":
    main()