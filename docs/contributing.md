# Contributing to DevContext

Thank you for your interest in contributing to DevContext!

## How to Contribute

### Reporting Issues

Found a bug? Have a feature request? Open an issue at:
https://github.com/jhony91792-oss/devcontext/issues

Please include:
- DevContext version
- Python version
- Steps to reproduce
- Expected vs actual behavior

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Run tests: `pytest`
5. Commit your changes: `git commit -m "feat: add my feature"`
6. Push to your branch: `git push origin feature/my-feature`
7. Open a Pull Request

### Code Style

- Follow PEP 8
- Use type hints where possible
- Write docstrings for public functions
- Add tests for new features

### Development Setup

```bash
# Clone
git clone https://github.com/jhony91792-oss/devcontext.git
cd devcontext

# Create venv
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install
pip install -e .

# Run tests
pytest
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/devcontext

# Run specific test
pytest tests/test_devcontext.py -v
```

## Project Structure

```
devcontext/
├── src/devcontext/     # Source code
│   ├── __init__.py     # Package init
│   ├── cli.py          # CLI interface
│   └── ...
├── tests/              # Test files
├── docs/               # Documentation
└── .github/
    └── workflows/      # CI/CD
```

## Commit Messages

Follow conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Tests
- `refactor:` Refactoring

## License

By contributing, you agree that your contributions will be licensed under the MIT License.