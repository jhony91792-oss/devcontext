# Configuration Guide

Customize DevContext behavior with configuration files.

## Configuration Files

DevContext looks for configuration in this order:
1. `.devcontextrc` (project root)
2. `.devcontextrc.json` (project root)
3. `devcontext.json` (project root)
4. `~/.config/devcontext/config.json` (user home)

## Options

```json
{
    "max_depth": 10,
    "skip_dirs": [".git", "node_modules", "__pycache__", ".venv"],
    "skip_files": ["*.pyc", "*.pyo", ".DS_Store"],
    "include_hidden": false,
    "output_format": "json",
    "show_stats": true,
    "languages": null,
    "exclude_patterns": [],
    "include_patterns": ["*"]
}
```

### max_depth

Maximum directory depth to scan.

```json
{ "max_depth": 5 }
```

### skip_dirs

Directories to exclude from scanning.

```json
{ "skip_dirs": ["node_modules", "dist", "build"] }
```

### skip_files

File patterns to exclude.

```json
{ "skip_files": ["*.log", "*.tmp", ".DS_Store"] }
```

### include_hidden

Include hidden files (starting with `.`).

```json
{ "include_hidden": false }
```

### output_format

Default output format.

```json
{ "output_format": "compact" }
```

## CLI Overrides

CLI options override configuration file settings:

```bash
devcontext generate . --max-depth 3 -f json
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `DEVCONTEXT_CONFIG` | Path to config file |
| `DEVCONTEXT_CACHE` | Cache directory |
| `DEVCONTEXT_SKIP_DIRS` | Comma-separated skip dirs |