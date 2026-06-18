# DevContext Integrations

## Overview

DevContext integrates with popular tools and platforms.

## GitHub Actions

### Auto-generate context on push
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
          name: codebase-context
          path: context.json
```

## VS Code

### tasks.json
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

### Recommended Extensions
- GitHub Copilot
- GitHub Actions
- Python

## JetBrains IDEs

Coming soon — see [Roadmap](ROADMAP.md).

## Slack

Use with Slackbot:
```
/devcontext generate ./project -o context.json
```

## Docker

```dockerfile
FROM python:3.11-slim
RUN pip install devcontext
COPY . /app
WORKDIR /app
CMD ["devcontext", "generate", "."]
```

Run:
```bash
docker run --rm -v $(pwd):/app devcontext generate /app
```

## Git Hooks

### Pre-commit
```bash
#!/bin/bash
# .git/hooks/pre-commit
devcontext generate . -o .devcontext.json
```

### Pre-push
```bash
#!/bin/bash
# .git/hooks/pre-push
devcontext generate . -o .pre-push-context.json
```

## CI/CD Pipelines

### GitLab CI
```yaml
generate-context:
  image: python:3.11
  before_script:
    - pip install devcontext
  script:
    - devcontext generate . -o context.json
  artifacts:
    paths:
      - context.json
```

### Jenkins
```groovy
pipeline {
    agent any
    stages {
        stage('Generate Context') {
            steps {
                sh 'pip install devcontext'
                sh 'devcontext generate . -o context.json'
            }
        }
    }
}
```

## Desktop Apps

Coming soon — see [Roadmap](ROADMAP.md).