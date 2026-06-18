# Plugin System

Extend DevContext with custom plugins.

## Overview

DevContext supports plugins that can:
- Modify context after generation
- Transform output formats
- Add custom analysis to files

## Installation

Plugins are stored in `~/.config/devcontext/plugins/`.

```bash
mkdir -p ~/.config/devcontext/plugins
```

## Writing a Plugin

Create a Python file in the plugins directory:

```python
from devcontext.plugins import Plugin

class MyPlugin(Plugin):
    name = "my-plugin"
    version = "0.1.0"
    
    def on_generate(self, context):
        # Modify context here
        context["custom_field"] = "value"
        return context
```

## Available Hooks

### on_generate(context)

Called after context is generated.

```python
def on_generate(self, context):
    context["total_functions"] = sum(
        len(f.get("functions", [])) for f in context["files"].values()
    )
    return context
```

### on_format(output, format_type)

Called during output formatting.

```python
def on_format(self, output, format_type):
    if format_type == "markdown":
        output = output.replace("#", "##")
    return output
```

### on_file_analyze(filepath, info)

Called for each file analyzed.

```python
def on_file_analyze(self, filepath, info):
    if filepath.endswith(".py"):
        info["python_version"] = "3.x"
    return info
```

## Loading Plugins

```bash
devcontext plugins list
```

## Removing Plugins

Simply delete the plugin file from the plugins directory.