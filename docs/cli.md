# DevContext CLI Reference

## Overview

DevContext provides a command-line interface for generating AI-ready context from any codebase.

## Commands

### `devcontext generate`

Generate context from a codebase.

```bash
devcontext generate <path> [options]
```

**Options:**
| Flag | Description | Default |
|------|-------------|---------|
| `-o, --output FILE` | Save output to file | stdout |
| `-f, --format FORMAT` | Output format: json, md, compact | json |
| `--max-depth N` | Maximum directory depth | 5 |

**Examples:**

```bash
# Basic usage
devcontext generate .

# Save to file
devcontext generate . -o context.json

# Markdown output
devcontext generate . -f md > context.md

# Compact output for AI prompts
devcontext generate . -f compact

# Deep scan (more files)
devcontext generate . --max-depth 10
```

### `devcontext tree`

Display file tree structure.

```bash
devcontext tree <path> [options]
```

**Options:**
| Flag | Description | Default |
|------|-------------|---------|
| `--max-depth N` | Maximum depth | 5 |

**Examples:**

```bash
# Show current directory
devcontext tree .

# Show with depth limit
devcontext tree . --max-depth 3

# Pipe to file
devcontext tree . > tree.txt
```

### `devcontext parse`

Parse code structure from files.

```bash
devcontext parse <path> [options]
```

**Options:**
| Flag | Description | Default |
|------|-------------|---------|
| `--files GLOB` | File filter pattern | * (all) |
| `--max-depth N` | Maximum depth | 5 |

**Examples:**

```bash
# Parse all files
devcontext parse .

# Parse only Python files
devcontext parse . --files "*.py"

# Parse specific file
devcontext parse ./main.py
```

### `devcontext --version`

Show version information.

```bash
devcontext --version
# Output: DevContext v0.1.0
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (path not found, etc.) |

## Environment Variables

DevContext does not require any environment variables to function.

## Configuration

DevContext uses sensible defaults. No configuration file needed.

## Tips

1. **Use `--format compact`** for AI prompts — shorter output
2. **Add to .gitignore**: `*.devcontext.json` (generated files)
3. **Combine with clipboard**: `devcontext generate . | pbcopy` (macOS)
4. **CI/CD**: Use in GitHub Actions for automated context generation