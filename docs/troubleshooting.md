# Troubleshooting

Common issues and solutions.

## Installation Issues

### pip install fails
```
ERROR: Could not find a version that satisfies the requirement devcontext
```
**Solution:** Update pip and try again:
```bash
pip install --upgrade pip
pip install devcontext
```

### Permission denied
```
ERROR: Could not install packages due to permission error
```
**Solution:** Use `--user` flag or virtual environment:
```bash
pip install --user devcontext
# or
python -m venv venv && source venv/bin/activate && pip install devcontext
```

## Usage Issues

### Slow generation on large projects
**Problem:** Taking too long to scan large codebase

**Solutions:**
1. Use `--max-depth` to limit scan depth
2. Add large directories to skip list
3. Use ignore patterns in config

```bash
devcontext generate . --max-depth 5
```

### Empty or missing output
**Problem:** No files found in output

**Solutions:**
1. Check if path is correct
2. Ensure files have supported extensions
3. Try with `-a` flag for analysis

```bash
devcontext generate ./src -a
```

### Memory issues with very large projects
**Problem:** Out of memory errors

**Solutions:**
1. Scan subdirectories separately
2. Use compact format
3. Increase available memory

```bash
# Scan specific subdirectory
devcontext generate ./src/module1
```

## GitHub Issues

### Stars not updating
GitHub star counts can take a few minutes to update. Refresh the page after starring.

### Pages not building
Check:
1. Settings → Pages → Source is set to GitHub Actions
2. No YAML syntax errors in workflow files
3. Actions tab shows successful deployment

## Configuration Issues

### Config file not being read
DevContext looks for config in this order:
1. `.devcontextrc` (project root)
2. `.devcontextrc.json` (project root)
3. `devcontext.json` (project root)
4. `~/.config/devcontext/config.json` (home)

Make sure your config file exists and is valid JSON.

### Environment variables not working
Use prefix `DEVCONTEXT_`:
```bash
export DEVCONTEXT_CACHE=/custom/cache/path
export DEVCONTEXT_SKIP_DIRS=".git,node_modules"
```

## CI/CD Issues

### GitHub Actions failures
1. Check Actions tab for error logs
2. Verify Python version compatibility (3.8+)
3. Ensure all dependencies are installed

### GitLab CI issues
Verify:
1. Python image is available
2. pip install works
3. devcontext command is in PATH