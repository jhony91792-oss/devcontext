# Plugin Development Guide

## Overview

DevContext supports a plugin system that allows you to extend its functionality.

## Plugin Architecture

Plugins can hook into two points:
1. `on_context_generated` - Called after context is generated
2. `on_file_scanned` - Called for each file scanned

## Creating a Plugin

```python
from devcontext.api_client import DevContextPlugin

class MyPlugin(DevContextPlugin):
    name = "my-plugin"
    version = "1.0.0"
    
    def on_context_generated(self, context):
        # Modify or enhance context
        context["my_custom_field"] = "added by plugin"
        return context
    
    def on_file_scanned(self, file_info):
        # Modify file info
        return file_info
```

## Registering Plugins

```python
from devcontext.api_client import get_plugin_manager

manager = get_plugin_manager()
manager.register(MyPlugin())
```

## Example Plugins

### Security Scanner Plugin
```python
class SecurityScannerPlugin(DevContextPlugin):
    """Scan for security issues in code."""
    name = "security-scanner"
    
    def on_context_generated(self, context):
        issues = []
        files = context.get("files", {})
        
        for path, info in files.items():
            content = info.get("content", "")
            if "password =" in content or "api_key" in path:
                issues.append(f"Potential secret in {path}")
        
        context["security_issues"] = issues
        return context
```

### Complexity Analyzer Plugin
```python
class ComplexityPlugin(DevContextPlugin):
    """Calculate complexity metrics."""
    name = "complexity-analyzer"
    
    def on_file_scanned(self, file_info):
        content = file_info.get("content", "")
        lines = content.split("\n")
        
        # Simple cyclomatic complexity approximation
        complexity = sum(1 for line in lines if any(kw in line for kw in ["if", "for", "while", "and", "or"]))
        
        file_info["complexity"] = complexity
        return file_info
```

## Plugin Manager CLI

Coming soon - will support:
- `devcontext plugin list`
- `devcontext plugin enable <name>`
- `devcontext plugin disable <name>`

## Publishing Plugins

1. Create a separate repository
2. Follow naming convention: `devcontext-plugin-<name>`
3. Document installation process
4. Submit to [awesome-devcontext](https://github.com/jhony91792-oss/awesome-devcontext) list

## Best Practices

- Keep plugins focused and small
- Document configuration options
- Handle errors gracefully
- Support both JSON and MD output formats
- Test with large codebases

## Limitations

- Plugins run in the same process as DevContext
- No network access from plugins
- Plugins cannot add new CLI commands (yet)