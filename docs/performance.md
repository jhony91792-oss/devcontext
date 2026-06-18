# Performance Guide

Optimize DevContext for large projects.

## Benchmarks

Typical generation times:
- Small project (< 100 files): 0.5-1s
- Medium project (100-1000 files): 1-5s
- Large project (1000-10000 files): 5-30s

## Optimization Tips

### 1. Limit Depth
```bash
devcontext generate . --max-depth 3
```

### 2. Use Ignore Patterns
```json
{
    "skip_dirs": [".git", "node_modules", "__pycache__", ".venv", "dist", "build"],
    "skip_files": ["*.pyc", "*.pyo", "*.log"]
}
```

### 3. Use Compact Format
```bash
devcontext generate . -f compact
```
Faster and uses less memory.

### 4. Cache Results
```bash
# Save to file
devcontext generate . -o context.json

# Reuse
devcontext load context.json
```

## Memory Optimization

For very large projects:
1. Process subdirectories separately
2. Increase available memory
3. Use `-f compact` format

## Profiling

```bash
devcontext profile benchmark -p ./myproject -i 10
```

## Performance Tips

1. **Skip unnecessary directories**: node_modules, .git, __pycache__
2. **Limit scan depth**: Use `--max-depth` for large codebases
3. **Use caching**: Save context to file for reuse
4. **Filter file types**: Only scan relevant files