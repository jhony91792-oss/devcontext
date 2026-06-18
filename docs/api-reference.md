# API Reference

Complete API documentation for DevContext.

## DevContextClient

Main Python client for programmatic access.

```python
from devcontext import DevContextClient

client = DevContextClient()
```

### Methods

#### `generate(path, format, **kwargs)`

Generate context for a codebase.

```python
context = client.generate(".", format="json")
```

**Parameters:**
- `path` (str): Project path
- `format` (str): Output format (`json`, `md`, `html`, `compact`)
- `**kwargs`: Additional options

**Returns:** Dict with context data

---

#### `tree(path, max_depth)`

Get file tree.

```python
tree = client.tree(".", max_depth=3)
```

---

#### `parse(file_path)`

Parse a single file.

```python
info = client.parse("main.py")
```

---

## Module Functions

### `from devcontext.tree import FileTree, scan_directory`

```python
from devcontext.tree import FileTree, scan_directory

# FileTree class
tree = FileTree(path, max_depth=10)
nodes = tree.scan()

# Convenience function
nodes = scan_directory(path)
```

### `from devcontext.parser import detect_language, parse_file`

```python
from devcontext.parser import detect_language, parse_file

# Detect language
lang = detect_language("main.py")  # "python"

# Parse file
info = parse_file("main.py")
# Returns: {'path': ..., 'language': ..., 'functions': [...], 'classes': [...]}
```

### `from devcontext.output import format_json, format_markdown`

```python
from devcontext.output import format_json, format_markdown, format_compact

output = format_json(context)
output = format_markdown(context)
output = format_compact(context)
```

## Data Structures

### Context

```python
{
    "version": "0.1.0",
    "generated": "2026-06-18T12:00:00",
    "files": {
        "path/to/file.py": {
            "language": "python",
            "lines": 100,
            "functions": ["func1", "func2"],
            "classes": ["Class1"],
            "imports": ["os", "sys"]
        }
    },
    "metadata": {
        "total_files": 50,
        "languages": ["python", "javascript"]
    }
}
```

### FileInfo

```python
{
    "path": "src/main.py",
    "language": "python",
    "lines": 100,
    "functions": ["main", "helper"],
    "classes": ["App"],
    "imports": ["os", "sys"],
    "exports": []
}
```