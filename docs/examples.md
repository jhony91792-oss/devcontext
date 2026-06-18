# Examples

Practical examples of DevContext usage.

## Quick Examples

### Basic Usage

```bash
# Generate context for current directory
devcontext generate .

# Output to file
devcontext generate . -o context.json

# Compact format for AI prompts
devcontext generate . -f compact
```

### With AI Assistants

**ChatGPT:**
```bash
devcontext generate . -f compact | pbcopy
# Paste to ChatGPT with your question
```

**Claude:**
```bash
devcontext generate . -f compact | pbcopy
# Paste to Claude with your question
```

**GitHub Copilot:**
```bash
devcontext generate . -o copilot-context.json
```

## Advanced Usage

### Limited Depth
```bash
# Only scan top 3 levels
devcontext generate . --max-depth 3
```

### Specific Directory
```bash
# Only scan src directory
devcontext generate ./src

# Only scan lib directory  
devcontext generate ./lib -f md
```

### With Analysis
```bash
# Enable code analysis
devcontext generate . -a -o analysis.json
```

### Watch Mode
```bash
# Auto-regenerate on file changes
devcontext watch . -i 10
```

## CI/CD Examples

### GitHub Actions
```yaml
name: Generate Context
on: [push, pull_request]

jobs:
  context:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install DevContext
        run: pip install devcontext
      - name: Generate Context
        run: devcontext generate . -o context.json
      - name: Upload Context
        uses: actions/upload-artifact@v4
        with:
          name: context
          path: context.json
```

### GitLab CI
```yaml
generate-context:
  stage: analyze
  script:
    - pip install devcontext
    - devcontext generate . -o context.json
  artifacts:
    paths:
      - context.json
```

## Integration Examples

### Python Script
```python
from devcontext import DevContextClient

client = DevContextClient()
context = client.generate(".", format="json")

# Use context...
print(f"Found {len(context['files'])} files")
```

### Shell Alias
```bash
# Add to ~/.bashrc
alias dc='devcontext generate . -f compact'

# Use
dc | pbcopy
```

### Pre-commit Hook
```bash
#!/bin/bash
# .git/hooks/pre-commit
devcontext generate . -o .devcontext.json
```