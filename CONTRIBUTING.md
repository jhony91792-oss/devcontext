# Contributing to DevContext

Thank you for your interest in contributing! 

## Development Setup

```bash
# Clone and install
git clone https://github.com/jhony91792-oss/devcontext.git
cd devcontext
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src tests
```

## Project Structure

```
devcontext/
├── src/devcontext/
│   ├── __init__.py      # Package init
│   ├── cli.py           # CLI entry point
│   ├── parser.py        # Language parser
│   ├── tree.py          # File tree builder
│   └── output.py        # Output formatters
├── tests/
│   └── test_devcontext.py
└── docs/
    └── examples.md
```

## Code Style

- Follow PEP 8
- Use type hints where possible
- Add docstrings to public functions
- Keep functions small and focused

## Submitting Changes

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Issues

Feel free to submit issues for:
- Bug reports
- Feature requests
- Questions
- Documentation improvements