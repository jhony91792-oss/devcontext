# DevContext Installation Guide

## Quick Install

```bash
pip install devcontext
```

## Verify Installation

```bash
devcontext --version
# Should output: DevContext v0.1.0
```

## Usage

```bash
# Generate context for current directory
devcontext generate .

# Save to file
devcontext generate . -o context.json

# Markdown output
devcontext generate . -f md

# Show file tree only
devcontext tree .

# Parse specific files
devcontext parse ./src
```

## Requirements

- Python 3.8+
- No external dependencies

## Troubleshooting

### Command not found
Make sure your pip bin directory is in PATH:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Permission error
```bash
pip install --user devcontext
```

### Upgrade
```bash
pip install --upgrade devcontext
```

## Docker

```bash
docker run --rm -v $(pwd):/code ghcr.io/jhony91792-oss/devcontext generate /code
```