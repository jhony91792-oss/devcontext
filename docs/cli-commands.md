# CLI Commands Reference

Complete reference for DevContext CLI commands.

## devcontext generate

Generate context from codebase.

```bash
devcontext generate [PATH] [OPTIONS]
```

### Options

| Short | Long | Description |
|-------|------|-------------|
| `-o` | `--output FILE` | Write to file |
| `-f` | `--format FORMAT` | json, md, html, compact |
| | `--max-depth N` | Maximum depth (default: 10) |
| `-a` | `--analyze` | Enable analysis |
| | `--no-stats` | Hide stats |

### Examples

```bash
devcontext generate .
devcontext generate ./src -f json -o context.json
devcontext generate . -f compact | pbcopy
devcontext generate . --max-depth 3
```

## devcontext tree

Show project file tree.

```bash
devcontext tree [PATH] [OPTIONS]
```

### Options

| Short | Long | Description |
|-------|------|-------------|
| `-d` | `--max-depth N` | Maximum depth |
| | `--show-lang` | Show language icons |

### Examples

```bash
devcontext tree .
devcontext tree ./src --max-depth 2
```

## devcontext parse

Parse a single file.

```bash
devcontext parse FILE [OPTIONS]
```

### Options

| Short | Long | Description |
|-------|------|-------------|
| `-f` | `--format` | json or text |

### Examples

```bash
devcontext parse main.py
devcontext parse utils.py -f json
```

## devcontext config

Configuration management.

```bash
devcontext config [ACTION] [KEY] [VALUE]
```

### Actions

- `show` - Show config (default)
- `set KEY VALUE` - Set value
- `reset` - Reset to defaults

### Examples

```bash
devcontext config show
devcontext config set max_depth 5
devcontext config reset
```

## devcontext plugins

Plugin management.

```bash
devcontext plugins [ACTION]
```

### Actions

- `list` - List plugins (default)
- `init` - Create example plugin

### Examples

```bash
devcontext plugins list
devcontext plugins init my_plugin.py
```

## Global Options

| Option | Description |
|--------|-------------|
| `--version` | Show version |
| `--help` | Show help |