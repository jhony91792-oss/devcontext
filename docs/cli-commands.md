# Command Reference

Complete reference for all DevContext CLI commands.

## Global Options

```
--version    Show version
--help       Show help
```

## devcontext generate

Generate AI-ready context from a codebase.

```bash
devcontext generate [PATH] [OPTIONS]
```

### Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `PATH` | Project path | `.` (current directory) |

### Options

| Option | Description |
|--------|-------------|
| `-o, --output FILE` | Write output to file |
| `-f, --format FORMAT` | Output format: `json`, `md`, `html`, `compact` |
| `--max-depth N` | Maximum directory depth |
| `-a, --analyze` | Enable code analysis |
| `--no-stats` | Hide statistics |

### Examples

```bash
# Basic usage
devcontext generate .

# JSON output
devcontext generate . -f json -o context.json

# Compact format for AI
devcontext generate . -f compact | pbcopy

# Limited depth
devcontext generate . --max-depth 3

# With analysis
devcontext generate . -a
```

---

## devcontext tree

Display project file tree.

```bash
devcontext tree [PATH] [OPTIONS]
```

### Options

| Option | Description |
|--------|-------------|
| `--max-depth N` | Maximum depth to display |
| `--show-lang` | Show programming language per file |

### Examples

```bash
devcontext tree .
devcontext tree ./src --max-depth 2
devcontext tree . --show-lang
```

---

## devcontext parse

Parse a single file and show structure.

```bash
devcontext parse FILE [OPTIONS]
```

### Arguments

| Argument | Description |
|----------|-------------|
| `FILE` | File to parse (required) |

### Options

| Option | Description |
|--------|-------------|
| `-f, --format FORMAT` | Output format: `json`, `text` |

### Examples

```bash
devcontext parse main.py
devcontext parse utils.py -f json
```

---

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | Error (path not found, parse error, etc.) |

---

## Configuration

DevContext reads from `.devcontextrc` in the project root:

```json
{
    "max_depth": 10,
    "skip_dirs": [".git", "node_modules", "__pycache__"],
    "output_format": "json"
}
```