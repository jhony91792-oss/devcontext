# Tips and Tricks

## Maximize AI Context Quality

1. **Use `--format compact`** for AI prompts — shorter, cleaner output
2. **Combine with clipboard** — `devcontext generate . | pbcopy` (macOS) or `xclip` (Linux)
3. **Focus on specific modules** — `devcontext generate ./src` for focused context
4. **Use with `--max-depth`** to control how deep the scan goes

## Productivity Hacks

### Daily Standup
```bash
# Get context for today's work
devcontext generate ./recent-changes -o standup.json
```

### Code Review
```bash
# Generate context before asking for review
devcontext generate . -f md > review-context.md
```

### Debugging
```bash
# Quick context for AI debugging
devcontext generate . -f compact | pbcopy
# Then paste to ChatGPT with your error message
```

### Onboarding
```bash
# Generate full project overview for new team members
devcontext generate . -f md > PROJECT_OVERVIEW.md
```

## Workflow Integration

### Shell Alias
```bash
# Add to ~/.bashrc or ~/.zshrc
alias dc='devcontext generate . -f compact'
```

### Git Pre-commit Hook
```bash
# .git/hooks/pre-commit
#!/bin/bash
devcontext generate . -o .devcontext.json
```

### VS Code Task
Add to `.vscode/tasks.json`:
```json
{
    "label": "AI Context",
    "type": "shell",
    "command": "devcontext generate . -o .context.json",
    "problemMatcher": []
}
```

## Advanced Usage

### Filter by Pattern
```bash
# Focus on specific file types
devcontext generate . --files "*.py"
```

### Exclude Directories
```bash
# For large monorepos
devcontext generate . --max-depth 3
```

### CI/CD Integration
```yaml
# GitHub Actions
- name: Generate Context
  run: |
    pip install devcontext
    devcontext generate . -o context.json
    echo "context=$(cat context.json)" >> $GITHUB_ENV
```

## Pro Tips

1. **Don't include generated files in git** — Add to `.gitignore`:
   ```
   *.devcontext.json
   context.json
   ```

2. **Version your contexts** — Useful for tracking project evolution:
   ```bash
   devcontext generate . -o contexts/v1.0.json
   ```

3. **Combine contexts** — For microservices:
   ```bash
   cat auth-context.json user-context.json > full-system.json
   ```

4. **Use with AI code review tools** — Pass context as input for better results

5. **Schedule regular context generation** — Track how your project evolves

## Sharing

If DevContext saves you time, please:
- ⭐ Star the repo
- 🐛 Report bugs
- 📝 Share with colleagues
- 📢 Post on social media

Every star helps this project grow!