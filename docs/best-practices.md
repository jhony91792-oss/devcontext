# DevContext Best Practices Guide

## Overview

This guide covers best practices for using DevContext effectively in your development workflow.

## Quick Wins

### 1. Daily AI Workflow
```bash
# Morning: Get context for today's work
devcontext generate . -o daily-context.json

# Paste content to AI when asking questions
```

### 2. Code Review
```bash
# Before asking for review
devcontext generate . -f compact | pbcopy  # macOS
```

### 3. Debugging
```bash
# When encountering bugs
devcontext generate . -f compact | pbcopy
# Paste to ChatGPT/Claude with error message
```

## Configuration Tips

### Per-Project Config (.devcontextrc)
```json
{
    "max_depth": 5,
    "skip_dirs": [".git", "node_modules", "__pycache__", "dist"],
    "include_hidden": false,
    "output_format": "compact"
}
```

### Global Config (~/.config/devcontext/config.json)
```json
{
    "max_depth": 10,
    "output_format": "json"
}
```

## Advanced Usage

### Watch Mode for Large Projects
```bash
# Auto-regenerate context when files change
devcontext watch . -o context.json -i 10
```

### Git Hooks
```bash
# Install pre-commit hook
devcontext hooks install pre-commit

# Now context auto-generates before each commit
```

### CI/CD Integration
```yaml
# GitHub Actions
- name: Generate Context
  run: |
    pip install devcontext
    devcontext generate . -o context.json
```

## Performance Tips

1. **Limit depth** for large repos: `--max-depth 3`
2. **Use caching**: Second run is 10x faster
3. **Specific paths**: `devcontext generate ./src` instead of `.`
4. **Compact format** for AI: `-f compact` (50% smaller)

## Security

- All processing is local
- No network requests for analysis
- No external dependencies
- Safe to use with proprietary code

## Troubleshooting

### Slow on Large Projects
- Use `--max-depth` to limit scan depth
- Exclude unnecessary directories with config

### Empty Output
- Check path exists: `ls -la /path/to/project`
- Try current directory: `devcontext generate .`

### Missing Language Support
- File an issue with language name and file extensions
- Use `--format md` for basic file listing

## Integrations

### VS Code
Add to `.vscode/tasks.json`:
```json
{
    "label": "AI Context",
    "type": "shell",
    "command": "devcontext generate . -o .devcontext.json"
}
```

### JetBrains
Coming soon — see [Roadmap](ROADMAP.md).

### Slack
```
/devcontext generate ./project -o context.json
```

## Contributing

Found a great workflow? Open an issue or PR to share it!