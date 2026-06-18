"""File tree builder for DevContext."""

import os
from pathlib import Path
from typing import Any


# Directories to skip during traversal
SKIP_DIRS = {
    '.git', '__pycache__', 'node_modules', '.venv', 'venv',
    '.pytest_cache', '.mypy_cache', 'dist', 'build', '.tox',
    '.idea', '.vscode', 'vendor', 'target', '.cache', '.npm',
    '.parcel', '.next', '.nuxt', '.svelte-kit', '__snapshots__',
    'coverage', '.nyc_output', 'tmp', 'temp', '.tmp'
}

# File extensions to include
CODE_EXTS = {
    '.py', '.js', '.mjs', '.cjs', '.ts', '.tsx', '.jsx',
    '.go', '.rs', '.java', '.c', '.cpp', '.h', '.hpp', '.cs',
    '.rb', '.php', '.swift', '.kt', '.scala', '.vue', '.svelte',
    '.md', '.rst', '.yaml', '.yml', '.toml', '.json', '.txt',
    '.sh', '.bash', '.zsh', '.fish', '.ps1', '.sql', '.graphql',
    '.html', '.css', '.scss', '.sass', '.less',
}

# Files to skip (not by extension, by exact name)
SKIP_FILES = {
    'package-lock.json', 'yarn.lock', 'poetry.lock',
    'Pipfile.lock', 'Gemfile.lock', 'composer.lock',
    'pnpm-lock.yaml', '.gitignore', '.gitattributes',
    'Thumbs.db', '.DS_Store', 'desktop.ini',
}

# Files that contain important metadata
KEY_FILES = {
    'README.md', 'README.rst', 'README.txt',
    'pyproject.toml', 'setup.py', 'setup.cfg', 'Makefile',
    'package.json', 'Cargo.toml', 'go.mod', 'go.sum',
    'requirements.txt', 'requirements-dev.txt', 'Pipfile',
    'Dockerfile', 'docker-compose.yml', 'docker-compose.yaml',
    '.env.example', '.env.template',
}


class FileTree:
    """Builds a tree representation of a codebase."""
    
    def __init__(self, root: Path, max_depth: int = 5):
        self.root = Path(root).resolve()
        self.max_depth = max_depth
        self.nodes = []
    
    def scan(self) -> list[dict[str, Any]]:
        """Scan the codebase and return a list of all relevant files."""
        self._walk(self.root, 0)
        return self.nodes
    
    def _walk(self, path: Path, depth: int):
        """Recursively walk directory."""
        if depth > self.max_depth:
            return
        
        try:
            for item in sorted(path.iterdir()):
                name = item.name
                
                # Skip hidden files/dirs except allowed ones
                if name.startswith('.') and name not in {'.gitignore', '.env.example'}:
                    continue
                
                # Skip known non-source directories
                if item.is_dir():
                    if name in SKIP_DIRS:
                        continue
                    self.nodes.append({
                        'path': str(item.relative_to(self.root)),
                        'type': 'dir',
                        'depth': depth
                    })
                    self._walk(item, depth + 1)
                else:
                    if name in SKIP_FILES:
                        continue
                    
                    ext = item.suffix.lower()
                    if ext in CODE_EXTS or name in KEY_FILES or name.startswith('Dockerfile'):
                        rel = str(item.relative_to(self.root))
                        self.nodes.append({
                            'path': rel,
                            'type': 'file',
                            'ext': ext or 'none',
                            'size': item.stat().st_size,
                            'depth': depth
                        })
        except PermissionError:
            pass
    
    def get_tree_string(self) -> str:
        """Return a nice tree representation."""
        lines = []
        for node in self.nodes:
            indent = '  ' * node['depth']
            if node['type'] == 'dir':
                lines.append(f"{indent}📁 {node['path']}/")
            else:
                lines.append(f"{indent}📄 {node['path']} ({node['size']} bytes)")
        return '\n'.join(lines)


def scan_directory(path: Path, max_depth: int = 5) -> list[dict[str, Any]]:
    """Convenience function to scan a directory."""
    tree = FileTree(path, max_depth)
    return tree.scan()