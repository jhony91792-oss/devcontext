# API Documentation

## Python API

DevContext can be used programmatically:

```python
from devcontext.tree import scan_directory, FileTree
from devcontext.parser import parse_file, detect_language
from devcontext.output import format_json, format_markdown
from pathlib import Path

# Scan a directory
files = scan_directory('./myproject')
# Returns: [{'path': 'main.py', 'type': 'file', ...}, ...]

# Parse a file
result = parse_file(Path('main.py'))
# Returns: {'path': 'main.py', 'language': 'python', 'functions': [...], 'classes': [...]}

# Format output
json_output = format_json({'version': '0.1.0', 'files': files})
md_output = format_markdown({'version': '0.1.0', 'files': files})
```

## CLI Reference

### `devcontext generate`

Generate AI-ready context from codebase.

```bash
devcontext generate <path> [options]
```

Options:
- `-o, --output FILE` — Save output to file
- `-f, --format [json|md|compact]` — Output format (default: json)
- `--max-depth N` — Maximum directory depth (default: 5)

### `devcontext tree`

Show file tree structure.

```bash
devcontext tree <path> [options]
```

Options:
- `--max-depth N` — Maximum depth (default: 5)

### `devcontext parse`

Parse code structure.

```bash
devcontext parse <path> [options]
```

Options:
- `--files GLOB` — File filter pattern
- `--max-depth N` — Maximum depth (default: 5)

## Return Types

### FileNode
```python
{
    'path': str,      # Relative path
    'type': str,      # 'file' or 'dir'
    'size': int,      # File size in bytes (files only)
    'depth': int,     # Directory depth
    'ext': str        # File extension (files only)
}
```

### ParseResult
```python
{
    'path': str,
    'language': str,    # e.g., 'python', 'javascript'
    'lines': int,
    'size': int,
    'functions': list,  # Function names
    'classes': list,    # Class names
    'imports': list     # Import statements
}
```