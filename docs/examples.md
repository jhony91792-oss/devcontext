# Examples

This document shows real-world use cases for DevContext.

## 1. AI Pair Programming with Claude

**Scenario:** You're debugging a complex authentication bug in your Django app.

**Before DevContext:**
You spend 5-10 minutes explaining your project structure, models, auth flow...

**With DevContext:**
```bash
devcontext generate . -f compact | pbcopy
# Paste into Claude
```

Claude now knows your exact project structure, functions, and relationships instantly.

---

## 2. Code Review Automation

**Scenario:** Submit a PR and want AI to review it.

```bash
# Generate context
devcontext generate . -o context.json

# Pass to your AI review tool
cat context.json | your-ai-review-tool
```

---

## 3. New Developer Onboarding

**Scenario:** New team member needs to understand the codebase.

```bash
# Generate comprehensive overview
devcontext generate /path/to/project -f md > overview.md

# Share the overview.md with the new developer
```

---

## 4. GitHub Actions CI/CD

**.github/workflows/ai-review.yml**
```yaml
name: AI Code Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Generate Context
        run: |
          pip install devcontext
          devcontext generate . -o context.json
          
      - name: AI Review
        run: |
          # Your AI review integration
          echo "Review context:"
          cat context.json
```

---

## 5. Documentation Generation

**Scenario:** Generate structure docs for your README.

```bash
devcontext generate . -f md > STRUCTURE.md
# Then embed parts into your README
```

---

## 6. Multiple Project Context

**Scenario:** Working across multiple microservices.

```bash
# Generate context for each service
devcontext generate ./auth-service -o auth-context.json
devcontext generate ./user-service -o user-context.json
devcontext generate ./payment-service -o payment-context.json

# Combine for full system view
cat auth-context.json user-context.json payment-context.json > full-system.json
```

---

## 7. Debugging Session

**Scenario:** Paste context into AI when asking debugging help.

```bash
# Terminal
devcontext generate . --format compact

# Copy output, paste to AI:
# "Help me debug this error: [error message]
# Here's my codebase context: [paste]"
```

---

## 8. API Usage (Programmatic)

```python
import json
from devcontext.tree import scan_directory
from devcontext.parser import parse_file
from devcontext.output import format_json

# Scan codebase
files = scan_directory('./myproject')
parsed = [parse_file(f) for f in files if f.is_file()]

# Generate AI-ready output
context = {
    'tool': 'DevContext',
    'version': '0.1.0',
    'files': parsed
}

print(format_json(context))
```

---

## 9. VS Code Task

**tasks.json:**
```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Generate AI Context",
            "type": "shell",
            "command": "devcontext generate . -o .devcontext.json",
            "problemMatcher": []
        }
    ]
}
```

---

## 10. Docker Integration

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

RUN pip install devcontext

# Generate context during build
COPY . /app
RUN devcontext generate /app -o /app/context.json

CMD ["bash"]
```

---

## Tips

1. **Use `--format compact`** for AI prompts (shorter, cleaner)
2. **Use `-f md`** for human-readable documentation
3. **Add to `.gitignore`**: `*.devcontext.json` (generated files)
4. **Combine with clipboard**: `devcontext generate . | pbcopy` (macOS) or `xclip` (Linux)

---

*Submit more examples via PR!*