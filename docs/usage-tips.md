# Usage Tips

Short tips for getting the most out of DevContext.

## Daily Workflows

### Quick Context
```bash
alias dc='devcontext generate . -f compact'
dc | pbcopy
```

### Before Code Review
```bash
devcontext generate . -a -o review-context.json
```

### After Major Changes
```bash
devcontext generate . -o context_$(date +%Y%m%d).json
```

## Git Integration

### Pre-commit Hook
Add to `.git/hooks/pre-commit`:
```bash
#!/bin/bash
devcontext generate . -o .devcontext.json
git add .devcontext.json
```

### Post-merge Hook
```bash
#!/bin/bash
if [ -f .devcontext.json ]; then
    devcontext generate . -o .devcontext.json
fi
```

## Shell Aliases

Add to `~/.bashrc` or `~/.zshrc`:
```bash
# Quick context
alias dc='devcontext generate . -f compact'

# Full analysis
alias dca='devcontext generate . -a -o context.json'

# Watch mode
alias dcw='devcontext watch . -i 30'
```

## Vim/Neovim Integration

Add to `.vimrc`:
```vim
" Generate context for current project
command! DevContext silent! execute '!devcontext generate . -f compact | xclip -selection clipboard'
```

## tmux Integration

```bash
# In tmux.conf
bind-key g run-shell "devcontext generate . -f compact | xclip -selection clipboard"
```

## Keyboard Shortcuts (macOS)

Create Automator Quick Action to:
1. Run `devcontext generate . -f compact`
2. Copy output to clipboard