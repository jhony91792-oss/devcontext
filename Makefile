.PHONY: install test lint clean build publish docs

# Install DevContext in development mode
install:
	pip install -e ".[dev]"

# Run tests
test:
	python3 test_runner.py

# Run linting
lint:
	python3 -m py_compile src/devcontext/*.py

# Clean build artifacts
clean:
	rm -rf build/ dist/ *.egg-info/
	rm -f .devcontext.json
	rm -rf __pycache__/ */__pycache__/ */*/__pycache__/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/

# Build package for PyPI
build: clean
	pip install build
	python -m build

# Publish to PyPI
publish: build
	pip install twine
	twine upload dist/* --token $(PYPI_TOKEN)

# Generate documentation site
docs:
	@echo "Docs available at: https://jhony91792-oss.github.io/devcontext/"

# Run DevContext on itself (self-check)
self-check:
	devcontext generate . -o .devcontext-check.json
	@echo "Self-check complete. Review .devcontext-check.json"

# Format code
format:
	black src/ tests/ --line-length 100

# Type check
typecheck:
	mypy src/ --ignore-missing-imports

# Dev context for AI
ai-context:
	devcontext generate . -o .ai-context.json
	@echo "AI context generated at .ai-context.json"