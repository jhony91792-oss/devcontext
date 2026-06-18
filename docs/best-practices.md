# Best Practices

Recommendations for using DevContext effectively.

## Getting Started

### 1. Quick Context Generation

For daily use, generate compact context:

```bash
devcontext generate . -f compact | pbcopy
```

Then paste directly into ChatGPT/Claude.

### 2. Regular Updates

Regenerate context after significant changes:

```bash
# After adding new features
devcontext generate . -o context.json
```

### 3. CI Integration

Add context generation to your CI:

```yaml
- name: Generate Context
  run: |
    pip install devcontext
    devcontext generate . -o context.json
```

## Configuration

### Skip Unnecessary Files

```json
{
    "skip_dirs": [".git", "node_modules", "__pycache__", ".venv", "dist", "build"],
    "skip_files": ["*.pyc", "*.log", "*.tmp"]
}
```

### Set Max Depth

For large projects, limit depth:

```bash
devcontext generate . --max-depth 5
```

## Output Formats

### JSON
Best for: Automation, API integration

### Markdown
Best for: Documentation, code reviews

### HTML
Best for: Sharing with non-technical stakeholders

### Compact
Best for: AI prompts, quick sharing

## Performance Tips

1. **Use ignore patterns** - Skip build artifacts
2. **Limit depth** - Don't scan deeper than needed
3. **Cache results** - Use `-o` to save output
4. **Watch mode** - Use `devcontext watch` for real-time updates

## Workflows

### Debugging Flow
```bash
devcontext generate . -f compact > /tmp/ctx.txt
# Paste to AI with: "Help me debug this error: [error]"
```

### Code Review Flow
```bash
devcontext generate . -a -o review.json
# Share with team for review
```

### Onboarding Flow
```bash
devcontext generate . -f md > PROJECT_OVERVIEW.md
# New team member reads this first
```