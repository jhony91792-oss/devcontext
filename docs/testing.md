# Testing Guide

How to test DevContext.

## Running Tests

```bash
# Run all tests
python3 test_runner.py

# Run specific test
python3 test_runner.py TestLanguageDetection
```

## Test Categories

### Unit Tests
- Language detection
- File parsing
- Output formatting

### Integration Tests
- Full context generation
- CLI commands
- File system operations

## Writing Tests

```python
def test_my_feature():
    """Test description."""
    # Arrange
    # Act
    # Assert
```

## CI/CD

All tests run automatically via GitHub Actions:
- Push to main
- Pull requests
- Daily schedule

See `.github/workflows/test.yml`