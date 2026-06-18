# Development Guide

Guide for developing and contributing to DevContext.

## Setup Development Environment

```bash
# Clone repository
git clone https://github.com/jhony91792-oss/devcontext.git
cd devcontext

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/devcontext

# Run specific test
pytest tests/test_devcontext.py -v
```

## Code Quality

```bash
# Format code
black src/

# Run linter
pylint src/devcontext/

# Type checking
mypy src/devcontext/
```

## Project Structure

```
devcontext/
├── src/devcontext/     # Main source code
│   ├── __init__.py     # Package init
│   ├── cli.py          # CLI interface
│   ├── analyzer.py     # Code analysis
│   └── ...
├── tests/              # Test files
├── docs/               # Documentation
└── .github/
    └── workflows/      # CI/CD pipelines
```

## Adding New Modules

1. Create module in `src/devcontext/`
2. Add CLI commands if needed
3. Write tests in `tests/`
4. Update documentation
5. Submit PR

## Commit Messages

Follow conventional commits:
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation
- `test:` Tests
- `refactor:` Code refactoring