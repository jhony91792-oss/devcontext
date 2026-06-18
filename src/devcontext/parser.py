"""Language-agnostic code parser for DevContext."""

import re
from pathlib import Path
from typing import Any


# Language detection based on file extension
LANG_MAP = {
    '.py': 'python',
    '.js': 'javascript',
    '.mjs': 'javascript',
    '.cjs': 'javascript',
    '.ts': 'typescript',
    '.tsx': 'typescript',
    '.jsx': 'javascript',
    '.go': 'go',
    '.rs': 'rust',
    '.java': 'java',
    '.c': 'c',
    '.cpp': 'cpp',
    '.h': 'c',
    '.hpp': 'cpp',
    '.cs': 'csharp',
    '.rb': 'ruby',
    '.php': 'php',
    '.swift': 'swift',
    '.kt': 'kotlin',
    '.scala': 'scala',
    '.vue': 'vue',
    '.svelte': 'svelte',
}

# Patterns for extracting code structure
PATTERNS = {
    'python': {
        'function': r'(?:^|\n)\s*(?:def|async def)\s+(\w+)\s*\(',
        'class': r'(?:^|\n)\s*class\s+(\w+)',
        'import': r'(?:^|\n)\s*(?:from\s+[\w.]+\s+)?import\s+',
        'decorator': r'@\w+',
        'comment': r'#\s*(.+)',
    },
    'javascript': {
        'function': r'(?:^|\n)\s*(?:function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=?\s*(?:async\s+)?\(|(\w+)\s*:\s*(?:async\s+)?\()',
        'class': r'(?:^|\n)\s*class\s+(\w+)',
        'import': r'(?:^|\n)\s*(?:import\s+.*?from\s+[\'"].*?[\'"])',
        'export': r'(?:^|\n)\s*export\s+',
    },
    'typescript': {
        'function': r'(?:^|\n)\s*(?:function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=?\s*(?:async\s+)?\(|(\w+)\s*:\s*(?:async\s+)?\()',
        'class': r'(?:^|\n)\s*class\s+(\w+)',
        'interface': r'(?:^|\n)\s*interface\s+(\w+)',
        'type': r'(?:^|\n)\s*type\s+(\w+)',
        'import': r'(?:^|\n)\s*(?:import\s+.*?from\s+[\'"].*?[\'"])',
        'export': r'(?:^|\n)\s*export\s+',
    },
    'go': {
        'function': r'(?:^|\n)\s*func\s+(?:\([^)]+\)\s+)?(\w+)\s*\(',
        'struct': r'(?:^|\n)\s*type\s+(\w+)\s+struct',
        'interface': r'(?:^|\n)\s*type\s+(\w+)\s+interface',
        'import': r'(?:^|\n)\s*import\s+',
        'package': r'(?:^|\n)\s*package\s+(\w+)',
    },
    'rust': {
        'function': r'(?:^|\n)\s*(?:pub\s+)?(?:async\s+)?fn\s+(\w+)\s*\(',
        'struct': r'(?:^|\n)\s*(?:pub\s+)?struct\s+(\w+)',
        'enum': r'(?:^|\n)\s*(?:pub\s+)?enum\s+(\w+)',
        'impl': r'(?:^|\n)\s*(?:pub\s+)?impl\s+',
        'use': r'(?:^|\n)\s*use\s+',
    },
}


def detect_language(path: str) -> str:
    """Detect programming language from file path."""
    ext = Path(path).suffix.lower()
    return LANG_MAP.get(ext, 'unknown')


def extract_structure(content: str, language: str) -> dict[str, Any]:
    """Extract code structure from file content."""
    result = {
        'language': language,
        'functions': [],
        'classes': [],
        'imports': [],
        'exports': [],
    }
    
    if language not in PATTERNS:
        return result
    
    patterns = PATTERNS[language]
    
    # Extract functions
    if 'function' in patterns:
        for match in re.finditer(patterns['function'], content, re.MULTILINE):
            name = match.group(1) or match.group(2) or match.group(3)
            if name:
                result['functions'].append(name)
    
    # Extract classes/structs/interfaces
    for key in ['class', 'struct', 'interface']:
        if key in patterns:
            for match in re.finditer(patterns[key], content, re.MULTILINE):
                result[key + 's'].append(match.group(1))
    
    # Extract imports
    if 'import' in patterns:
        for match in re.finditer(patterns['import'], content, re.MULTILINE):
            imp = match.group(0).strip()
            if len(imp) < 200:  # Skip very long imports
                result['imports'].append(imp[:100])
    
    # Extract exports
    if 'export' in patterns:
        result['exports'] = len(re.findall(patterns['export'], content, re.MULTILINE))
    
    return result


def parse_file(path: Path) -> dict[str, Any]:
    """Parse a single file and return its structure."""
    try:
        content = path.read_text(encoding='utf-8', errors='replace')
    except Exception:
        return {'error': 'Could not read file'}
    
    language = detect_language(str(path))
    structure = extract_structure(content, language)
    
    # Count lines
    lines = content.split('\n')
    
    return {
        'path': str(path),
        'language': language,
        'lines': len(lines),
        'size': len(content),
        **structure
    }


def parse_files(paths: list[Path]) -> list[dict[str, Any]]:
    """Parse multiple files."""
    return [parse_file(p) for p in paths if p.exists()]