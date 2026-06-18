# Showcase

Real-world examples of DevContext in action.

## Quick Examples

### Generate Context for Any Project

```bash
$ devcontext generate . -f compact
```

**Output:**
```json
{
  "version": "0.1.0",
  "files": 47,
  "languages": ["python", "javascript"],
  "structure": {
    "src/main.py": {"functions": ["main", "init"], "classes": ["App"]},
    "src/utils.py": {"functions": ["helper", "format"]},
    ...
  }
}
```

### Use with ChatGPT

```bash
# Copy context
devcontext generate . -f compact | pbcopy

# Paste to ChatGPT with:
# "Help me debug this error in my project"
```

### CI/CD Integration

```yaml
# .github/workflows/context.yml
- name: Generate Context
  run: |
    pip install devcontext
    devcontext generate . -o context.json
```

---

## Supported Languages

### Python Project
```
src/
├── main.py          # main(), init_app()
├── utils.py         # helper(), format_date()
├── models/
│   ├── __init__.py  # User, Post
│   └── user.py      # User class
```

### JavaScript/TypeScript
```
src/
├── index.ts         # main, App
├── components/      # React components
└── utils/           # helper functions
```

---

## Before vs After

### Before DevContext
- Manually explain project: 10-15 min
- Inconsistent context
- Important details missed

### After DevContext
- One command: 3 seconds
- Complete context
- Never miss anything

---

## User Stories

### Developer Daily Workflow
1. `devcontext generate . -f compact | pbcopy`
2. Open ChatGPT/Claude
3. Paste context + question
4. Get instant relevant help

### Code Review
1. Generate context before PR
2. Share with team for review
3. Better feedback, faster turnaround

### Onboarding
1. `devcontext generate . -f md > OVERVIEW.md`
2. Share with new team member
3. Faster understanding of codebase