"""DevContext — Advanced code analysis module.

This module provides deeper code analysis capabilities:
- Complexity metrics
- Dependency graph
- Pattern detection
- Code quality indicators
"""

import re
from pathlib import Path
from typing import Any


def calculate_complexity(code: str) -> dict[str, Any]:
    """Calculate code complexity metrics.
    
    Returns:
        Dictionary with complexity metrics:
        - lines: total lines
        - functions: function count
        - classes: class count
        - conditionals: if/for/while statements
        - complexity_score: estimated complexity
    """
    lines = len(code.split('\n'))
    functions = len(re.findall(r'def\s+\w+', code))
    classes = len(re.findall(r'class\s+\w+', code))
    conditionals = len(re.findall(r'\b(if|for|while|except|and|or)\b', code))
    
    # Simple complexity scoring
    complexity = (functions * 1) + (classes * 2) + (conditionals * 0.5)
    
    return {
        'lines': lines,
        'functions': functions,
        'classes': classes,
        'conditionals': conditionals,
        'complexity_score': round(complexity, 2)
    }


def detect_frameworks(code: str) -> list[str]:
    """Detect which frameworks are used in the code."""
    frameworks = []
    
    patterns = {
        'django': r'from django\.|import django',
        'flask': r'from flask\.|import flask',
        'fastapi': r'from fastapi\.|import fastapi',
        'react': r'from react\.|import react',
        'vue': r'from vue\.|import vue',
        'angular': r'from @angular\.|import @angular',
        'nextjs': r'from next[_-]?js|import next',
        'express': r'from express\.|import express',
        'react_native': r'ReactNative|RN',
        'pandas': r'from pandas\.|import pandas',
        'numpy': r'from numpy\.|import numpy',
        'tensorflow': r'from tensorflow\.|import tensorflow',
        'pytorch': r'from torch\.|import torch',
        'sqlalchemy': r'from sqlalchemy\.|import sqlalchemy',
        'requests': r'from requests\.|import requests',
        'aiohttp': r'from aiohttp\.|import aiohttp',
    }
    
    for name, pattern in patterns.items():
        if re.search(pattern, code, re.IGNORECASE):
            frameworks.append(name)
    
    return frameworks


def extract_endpoints(code: str, language: str = 'python') -> list[dict[str, str]]:
    """Extract API endpoints from code.
    
    For Python/Flask/FastAPI:
        Looks for @app.route, @router.get, etc.
    For JavaScript/Node:
        Looks for app.get, router.post, etc.
    """
    endpoints = []
    
    if language == 'python':
        # Flask/FastAPI decorators
        patterns = [
            r'@(\w+)\.(get|post|put|patch|delete|options)\([\"\']([^\"\']+)[\"\']\)',
            r'@router\.(get|post|put|patch|delete|options)\([\"\']([^\"\']+)[\"\']\)',
            r'def\s+(\w+).*?\(.*?\):.*?\"\"\"([^\"]+)\"\"\"',
        ]
        
        for pattern in patterns:
            for match in re.finditer(pattern, code, re.MULTILINE):
                groups = match.groups()
                if len(groups) >= 2:
                    if groups[0] in ['get', 'post', 'put', 'patch', 'delete', 'options']:
                        endpoints.append({
                            'method': groups[0].upper(),
                            'path': groups[1],
                            'handler': 'decorator'
                        })
                    else:
                        endpoints.append({
                            'method': 'VIEW',
                            'path': groups[1] if len(groups) > 1 else 'unknown',
                            'handler': groups[0],
                            'doc': groups[2][:50] if len(groups) > 2 else ''
                        })
    
    elif language in ['javascript', 'typescript']:
        patterns = [
            r'(app|router)\.(get|post|put|patch|delete)\([\"\']([^\"\']+)[\"\']',
        ]
        
        for pattern in patterns:
            for match in re.finditer(pattern, code):
                groups = match.groups()
                if len(groups) >= 3:
                    endpoints.append({
                        'method': groups[1].upper(),
                        'path': groups[2],
                        'handler': groups[0]
                    })
    
    return endpoints


def build_dependency_graph(files: list[dict[str, Any]]) -> dict[str, list[str]]:
    """Build a simple dependency graph between files.
    
    Args:
        files: List of file info dicts with 'path' and 'imports'
    
    Returns:
        Dict mapping file paths to their dependencies
    """
    graph = {}
    
    for file_info in files:
        path = file_info.get('path', '')
        imports = file_info.get('imports', [])
        graph[path] = imports
    
    return graph


def detect_code_smells(code: str) -> list[dict[str, str]]:
    """Detect potential code quality issues.
    
    Returns:
        List of detected issues with description and line number
    """
    issues = []
    lines = code.split('\n')
    
    for i, line in enumerate(lines, 1):
        # Long lines
        if len(line) > 120:
            issues.append({
                'type': 'long_line',
                'line': i,
                'message': f'Line exceeds 120 characters ({len(line)})'
            })
        
        # TODO/FIXME comments
        if re.search(r'\b(TODO|FIXME|HACK|XXX)\b', line, re.IGNORECASE):
            issues.append({
                'type': 'marker',
                'line': i,
                'message': 'Contains marker comment'
            })
        
        # Hardcoded credentials
        if re.search(r'(password|secret|api_key|token)\s*=\s*[\"\'][\w\-]{8,}', line, re.IGNORECASE):
            issues.append({
                'type': 'security',
                'line': i,
                'message': 'Potential hardcoded credential'
            })
    
    return issues


def summarize_file(path: Path) -> dict[str, Any]:
    """Generate a summary of a single file."""
    try:
        content = path.read_text(encoding='utf-8', errors='replace')
    except Exception:
        return {'error': 'Could not read file'}
    
    from devcontext.parser import detect_language
    from devcontext.analyzer import calculate_complexity, detect_frameworks
    
    return {
        'path': str(path),
        'language': detect_language(str(path)),
        'size': len(content),
        'complexity': calculate_complexity(content),
        'frameworks': detect_frameworks(content),
        'lines': len(content.split('\n'))
    }