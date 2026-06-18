# Contributing to DevContext

Thank you for your interest in contributing to DevContext!

## Quick Start

```bash
# Fork and clone the repo
git clone https://github.com/YOUR_USERNAME/devcontext.git
cd devcontext

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
python3 test_runner.py
```

## Development Workflow

1. **Fork** the repository on GitHub
2. **Clone** your fork locally
3. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

4. **Make your changes** and commit with clear messages
5. **Add tests** for any new functionality
6. **Ensure tests pass**: `python3 test_runner.py`
7. **Push** to your fork
8. **Open a Pull Request** on GitHub

## Code Style

- Follow PEP 8
- Use meaningful variable names
- Comment complex logic
- Keep functions small and focused
- Type hints encouraged but not required

## Testing

Write tests for all new functionality:

```python
def test_new_feature():
    """Description of expected behavior."""
    # Arrange
    # Act
    # Assert
```

Run tests with:
```bash
python3 test_runner.py
```

## Commit Messages

Use clear, descriptive commit messages:
- `feat: add new language support`
- `fix: correct parser error for Go files`
- `docs: update README with examples`
- `test: add tests for analyzer module`

## Pull Request Process

1. Update documentation if needed
2. Add tests for any new code
3. Ensure all tests pass
4. Update CHANGELOG.md if relevant
5. Request review from maintainers

## Types of Contributions

### Bug Reports
- Search existing issues first
- Include Python version, OS, and error message
- Provide minimal reproduction case

### Feature Requests
- Describe the problem you're solving
- Suggest a solution
- Be open to feedback

### Code
- Follow existing code style
- Add tests
- Update documentation

## Resources

- [GitHub Docs](https://docs.github.com/)
- [Python Packaging Guide](https://packaging.python.org/)
- [GitHub Actions Tutorial](https://docs.github.com/en/actions/learning-github-actions)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.