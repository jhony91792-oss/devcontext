# Troubleshooting Guide

## Common Issues

### Installation Issues

#### "pip: command not found"
```bash
# Try with python3 -m pip
python3 -m pip install devcontext

# Or ensure pip is in your PATH
export PATH="$HOME/.local/bin:$PATH"
```

#### "Permission denied" error
```bash
# Use --user flag
pip install --user devcontext

# Or use a virtual environment
python3 -m venv venv
source venv/bin/activate
pip install devcontext
```

#### "Python version not supported"
DevContext requires Python 3.8+. Check your version:
```bash
python3 --version
```

If below 3.8, upgrade Python or use a different environment.

### Usage Issues

#### "No output" or "empty context"
This usually means the path doesn't exist or has no recognized files:
```bash
# Verify path exists
ls -la /path/to/project

# Try current directory
devcontext generate .

# Check with verbose output
devcontext tree . --max-depth 3
```

#### "Missing language support"
If your language isn't recognized:
1. Check if it's in the [supported languages list](languages.md)
2. File an issue for support request
3. Use `--format md` for basic file listing

#### "File not found" errors
Make sure you're running from the correct directory:
```bash
cd /path/to/your/project
devcontext generate .
```

### Performance Issues

#### "Slow on large projects"
For projects with 10k+ files:
```bash
# Reduce depth
devcontext generate . --max-depth 3

# Exclude specific directories
# (edit code to add to SKIP_DIRS in tree.py)
```

#### "High memory usage"
DevContext is designed to be memory-efficient, but very large codebases may use significant RAM. No fix currently available — consider using `--max-depth` to limit scan.

### CI/CD Issues

#### "Tests failing in GitHub Actions"
Check the workflow runs at: https://github.com/jhony91792-oss/devcontext/actions

Common fixes:
- Ensure Python version matches (3.8+)
- Check if tests pass locally: `python3 test_runner.py`

#### "PyPI release failed"
1. Ensure `PYPI_API_TOKEN` secret is set in repo settings
2. Check tag format: must be `v*` (e.g., `v0.1.0`)
3. Verify package builds locally: `pip install build && python -m build`

## Getting Help

1. Check existing [Issues](https://github.com/jhony91792-oss/devcontext/issues)
2. Create a new issue with the bug report template
3. Include:
   - Python version
   - DevContext version (`devcontext --version`)
   - Error message
   - Steps to reproduce
   - OS/environment

## Known Limitations

1. **Binary files**: Not supported (images, executables, etc.)
2. **Very large files**: Files >1MB may cause memory issues
3. **Encrypted code**: Cannot parse encrypted or obfuscated code
4. **Dynamic code**: Code generated at runtime won't be detected