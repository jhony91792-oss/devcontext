# Developer Guide

## Setting Up DevContext for Development

### Prerequisites
- Python 3.8+
- Git

### Clone and Setup
```bash
git clone https://github.com/jhony91792-oss/devcontext.git
cd devcontext
pip install -e .
```

### Running Tests
```bash
python3 test_runner.py
```

### Project Structure
```
devcontext/
├── src/devcontext/     # Main source code
│   ├── cli.py         # Entry point
│   ├── tree.py        # File scanning
│   ├── parser.py      # Language parsing
│   ├── output.py      # Output formatters
│   ├── analyzer.py    # Code analysis
│   └── ...            # Other modules
├── docs/              # Documentation
├── tests/             # Test files
└── .github/           # GitHub config
```

## Adding New Language Support

1. Edit `src/devcontext/parser.py`
2. Add extension to `LANG_MAP`
3. Add regex patterns for functions/classes
4. Add test case
5. Submit PR

## Adding New Output Format

1. Edit `src/devcontext/output.py`
2. Add formatter function
3. Update CLI in `cli.py`
4. Add test
5. Submit PR

## Code Style

- PEP 8 compliant
- Type hints encouraged
- Docstrings for public functions
- Small, focused functions

## Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Add tests
5. Ensure all tests pass
6. Update documentation
7. Submit PR

## Release Process

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create git tag
4. Push to GitHub
5. GitHub Actions will publish to PyPI

## Architecture

See [architecture.md](architecture.md) for detailed architecture documentation.

## Debugging

```python
# Enable verbose output
devcontext generate . --format json -o debug.json

# Check generated output
cat debug.json
```

## Performance Profiling

```bash
python3 -m cProfile -o profile.stats -m devcontext generate .
python3 -m pstats profile.stats
```