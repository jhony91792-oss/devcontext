# Integrations

Connect DevContext with your tools.

## GitHub Actions

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

## GitLab CI

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

## VS Code

Add to `.vscode/tasks.json`:
```json
{
    "version": "2.0.0",
    "tasks": [{
        "label": "Generate DevContext",
        "command": "devcontext",
        "args": ["generate", "."],
        "problemMatcher": []
    }]
}
```

## JetBrains IDEs

1. Settings → Tools → External Tools
2. Add new tool:
   - Name: DevContext
   - Program: devcontext
   - Arguments: generate $ProjectFileDir$

## Slack Integration

```bash
# In Slack webhook configuration
devcontext generate . -f compact | curl -X POST -H 'Content-type: application/json' \
  --data '{"text": "'"$(cat)"'"}' $SLACK_WEBHOOK_URL
```

## Discord Integration

```bash
devcontext generate . | python3 -c "
import sys, json
import requests
data = {'content': sys.stdin.read()}
requests.post(DISCORD_WEBHOOK, json=data)
"
```

## Text Editors

### Vim/Neovim
```vim
" Generate and copy context
command! DevContext silent! execute '!devcontext generate . -f compact | xclip -selection clipboard'
```

### Emacs
```elisp
(defun devcontext-generate ()
  (interactive)
  (shell-command "devcontext generate . -f compact | xclip -selection clipboard"))
```

## CI/CD Systems

### Jenkins
```groovy
pipeline {
    stage('Context') {
        steps {
            sh 'pip install devcontext'
            sh 'devcontext generate . -o context.json'
        }
    }
}
```

### CircleCI
```yaml
- run:
    name: Generate Context
    command: |
      pip install devcontext
      devcontext generate . -o context.json
```