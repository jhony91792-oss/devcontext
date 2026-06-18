# Testing Guide

How to test DevContext.

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/devcontext --cov-report=html

# Run specific test
pytest tests/test_devcontext.py -v
```

## Writing Tests

```python
import pytest
from devcontext import DevContext

def test_basic_generation():
    dc = DevContext(".")
    context = dc.generate()
    assert context is not None
    assert "version" in context
```

## Test Structure

```
tests/
├── test_devcontext.py    # Main tests
├── test_cli.py           # CLI tests
├── test_analyzer.py      # Analyzer tests
└── ...
```

## CI/CD Testing

Tests run automatically on every push via GitHub Actions.

```yaml
# .github/workflows/test.yml
- name: Test
  run: pytest
```

## Coverage Requirements

- Minimum 80% coverage for new code
- 100% coverage for critical paths