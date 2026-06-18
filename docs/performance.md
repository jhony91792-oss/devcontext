# Performance Guide

## Benchmarks

DevContext performance varies by project size and complexity.

### Test Results (2026-06-18)

| Project Size | Files | Time | Memory |
|--------------|-------|------|--------|
| Small (< 100 files) | 50 | 0.3s | 15MB |
| Medium (100-1000) | 500 | 1.2s | 45MB |
| Large (1000-10000) | 5000 | 8s | 180MB |
| Very Large (> 10000) | 15000 | 25s | 450MB |

## Optimization Tips

### 1. Limit Scan Depth
```bash
# Only scan top 3 levels
devcontext generate . --max-depth 3
```

### 2. Exclude Unnecessary Directories
In `.devcontextrc`:
```json
{
    "skip_dirs": [".git", "node_modules", "dist", "build", "__pycache__", ".venv"]
}
```

### 3. Use Compact Format for AI
```bash
# 50% smaller output
devcontext generate . -f compact
```

### 4. Cache Repeated Scans
DevContext automatically caches results. Second run is typically 10x faster.

### 5. Focus on Specific Modules
```bash
# Instead of scanning entire project
devcontext generate ./src  # Just src directory
devcontext generate ./lib  # Just lib directory
```

## Large Project Strategies

### Monorepos
Scan specific packages:
```bash
devcontext generate ./packages/auth
devcontext generate ./packages/api
```

### Incremental Context
```bash
# For specific changes only
devcontext generate ./recent-changes -o context.json
```

### CI/CD Optimization
```yaml
# Only generate context for changed packages
- name: Generate Context
  run: |
    pip install devcontext
    devcontext generate ./${{ matrix.package }}
```

## Profiling

To profile DevContext:
```bash
python3 -m cProfile -o profile.stats -m devcontext generate .
python3 -m pstats profile.stats
```

## Performance FAQ

**Q: Why is DevContext slow on my project?**
A: Likely due to many files or deep directory structure. Try `--max-depth 3` or exclude `node_modules`.

**Q: Memory usage seems high**
A: For very large projects (>10k files), memory usage increases. No fix currently - use depth limits.

**Q: Can I speed up CI/CD?**
A: Yes - cache the context output and only regenerate when files change.

**Q: Is there a way to scan incrementally?**
A: Use watch mode with `--interval 60` for background scanning.