# Advanced Usage

## Complexity Analysis

DevContext can analyze code complexity:

```python
from devcontext.analyzer import calculate_complexity, detect_frameworks

code = open('main.py').read()
metrics = calculate_complexity(code)
print(f"Complexity score: {metrics['complexity_score']}")
print(f"Functions: {metrics['functions']}")
print(f"Classes: {metrics['classes']}")
```

## Framework Detection

Automatically detect frameworks used in your codebase:

```python
from devcontext.analyzer import detect_frameworks

code = open('app.py').read()
frameworks = detect_frameworks(code)
print(f"Frameworks: {frameworks}")
# Output: ['django', 'requests']
```

## API Usage

```python
from devcontext.tree import scan_directory
from devcontext.parser import parse_file
from devcontext.output import format_json

# Full pipeline
files = scan_directory('./project')
parsed = [parse_file(f) for f in files if f.is_file()]
print(format_json({'files': parsed}))
```

## Integration Examples

### VS Code Task
Add to `.vscode/tasks.json`:
```json
{
    "label": "Generate AI Context",
    "type": "shell",
    "command": "devcontext generate . -o .devcontext.json",
    "problemMatcher": []
}
```

### GitHub Actions
```yaml
- name: Generate Code Context
  run: |
    pip install devcontext
    devcontext generate . -o context.json
    
- name: AI Review
  uses: your-ai-tool@v1
  with:
    context: ${{ env.context }}
```

### Pre-commit Hook
Add to `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: local
    hooks:
      - id: devcontext
        name: Generate AI Context
        entry: devcontext generate . -o .devcontext.json
        language: system
```

## Tips

1. **For AI prompts**: Use `--format compact` for shorter output
2. **For documentation**: Use `-f md` for readable Markdown
3. **For large projects**: Increase `--max-depth` for deeper scanning
4. **CI/CD**: Add to workflow for automated context generation