# Advanced Usage

Advanced DevContext techniques and workflows.

## Combining with AI

### ChatGPT Workflow
```bash
# Generate context
devcontext generate . -f compact > /tmp/ctx.txt

# Copy to clipboard
cat /tmp/ctx.txt | pbcopy

# In ChatGPT, paste with your question:
# "Help me understand and refactor this codebase: [paste]"
```

### Claude Workflow
```bash
# Generate detailed context
devcontext generate . -a -f md > /tmp/ctx.md

# Use in Claude:
# /read /tmp/ctx.md
# "Analyze this code and suggest improvements"
```

## CI/CD Advanced

### GitHub Actions with Artifacts
```yaml
- name: Generate Context
  run: |
    devcontext generate . -o context.json
  
- name: Upload Context
  uses: actions/upload-artifact@v4
  with:
    name: code-context
    path: context.json
```

### Scheduled Context Generation
```yaml
on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight

jobs:
  context:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Generate
        run: devcontext generate . -o context.json
```

## Programmatic Usage

### Python API
```python
from devcontext import DevContext

dc = DevContext("./myproject")
context = dc.generate(format="json")

# Process context
for path, info in context["files"].items():
    print(f"{path}: {len(info.get('functions', []))} functions")
```

### Using Context Data
```python
# Find large files
large_files = [
    (path, info) 
    for path, info in context["files"].items()
    if info.get("lines", 0) > 500
]

# Find most complex files
complex_files = sorted(
    context["files"].items(),
    key=lambda x: len(x[1].get("functions", [])),
    reverse=True
)[:10]
```

## Custom Analyzers

```python
from devcontext.analyzer import Analyzer

class MyAnalyzer(Analyzer):
    def analyze_file(self, filepath, content):
        result = super().analyze_file(filepath, content)
        
        # Add custom analysis
        if filepath.endswith(".py"):
            result["custom"] = analyze_python_specific(content)
        
        return result
```

## Performance Tuning

### For Large Repos
```bash
# Scan only src, limited depth
devcontext generate ./src --max-depth 4

# Skip large directories
devcontext generate . --skip-dirs node_modules,.venv,dist
```

### Caching
```bash
# Generate and save
devcontext generate . -o context.json

# Later, load cached version
devcontext load context.json
```