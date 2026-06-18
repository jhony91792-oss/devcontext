# Installation Guide

## Requirements

- Python 3.8 or higher
- pip or pip3

## Install from PyPI (Recommended)

```bash
pip install devcontext
```

## Install from Source

```bash
git clone https://github.com/jhony91792-oss/devcontext.git
cd devcontext
pip install -e .
```

## Verify Installation

```bash
devcontext --version
# Should output: DevContext 0.1.0
```

## pipx (Isolated Installation)

```bash
pipx install devcontext
```

## Docker

```bash
docker pull ghcr.io/jhony91792-oss/devcontext
docker run --rm -v $(pwd):/app ghcr.io/jhony91792-oss/devcontext generate /app
```

## VS Code Extension (Coming Soon)

See [Roadmap](ROADMAP.md) for planned integrations.

## Uninstall

```bash
pip uninstall devcontext
```