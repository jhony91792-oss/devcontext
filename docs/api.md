# API Reference

Python API documentation for DevContext.

## DevContext

Main class for generating context.

```python
from devcontext import DevContext

dc = DevContext(path=".")
context = dc.generate()
```

### Constructor

```python
DevContext(path: str = ".", max_depth: int = 10)
```

Parameters:
- `path` (str): Directory to analyze
- `max_depth` (int): Maximum directory depth

### Methods

#### generate()

Generate context from codebase.

```python
context = dc.generate(format: str = "json")
```

Parameters:
- `format` (str): Output format - "json", "md", "html", "compact"

Returns:
- Dict containing context data

## Context Structure

```json
{
    "version": "0.1.0",
    "metadata": {
        "name": "project-name",
        "total_files": 42,
        "languages": ["python", "javascript"],
        "total_functions": 156,
        "total_classes": 23
    },
    "files": {
        "src/main.py": {
            "language": "python",
            "functions": ["main", "init"],
            "classes": ["App"],
            "lines": 150
        }
    }
}
```

## CLI Module

```python
from devcontext.cli import main

if __name__ == "__main__":
    main()
```

## Config

```python
from devcontext.config import Config

config = Config()
config.load()
config.set("max_depth", 5)
config.save()
```

## Reporter

```python
from devcontext.reporter import Reporter

reporter = Reporter(context)
report = reporter.generate_full_report()
```

## Search

```python
from devcontext.search import ContextSearch

searcher = ContextSearch(context)
results = searcher.search_functions("test")
```