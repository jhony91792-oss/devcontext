# Architecture

DevContext architecture overview.

## Overview

DevContext follows a modular architecture with clear separation of concerns.

```
devcontext/
├── src/devcontext/       # Main package
│   ├── __init__.py       # Package entry
│   ├── cli.py            # CLI interface
│   ├── analyzer.py       # Code analysis
│   ├── parser.py         # File parsing
│   └── ...               # Feature modules
├── tests/                # Test suite
└── docs/                 # Documentation
```

## Core Components

### 1. CLI Layer (`cli.py`)
Entry point for command-line interface.
- Parses arguments
- Routes commands
- Formats output

### 2. Core Engine (`DevContext` class)
Main context generation logic.
- Scans directories
- Collects file info
- Aggregates metadata

### 3. Analyzer (`analyzer.py`)
Language-specific code analysis.
- Parses source files
- Extracts functions/classes
- Detects imports

### 4. Parser (`parser.py`)
File type detection and parsing.
- Identifies language by extension
- Routes to appropriate parser

### 5. Output Formatters
Multiple output format support.
- JSON (default)
- Markdown
- HTML
- Compact

## Module Categories

### Data Processing
- `analyzer.py` - Code analysis
- `parser.py` - File parsing
- `tree.py` - Directory tree

### Output
- `output.py` - Output formatting
- `export.py` - Multi-format export
- `report.py` - Report generation

### Integration
- `api_client.py` - Python API
- `hooks.py` - Git hooks
- `notifiers.py` - Notifications
- `webhooks.py` - Webhook support

### Utilities
- `cache.py` - Caching
- `config.py` - Configuration
- `stats.py` - Statistics
- `search.py` - Search

## Data Flow

```
User Input → CLI → DevContext → Analyzer → Parser → Context
                                                      ↓
                                               Formatter → Output
```

## Extension Points

### Custom Analyzers
Add language support by implementing `Analyzer` interface.

### Plugins
Use plugin system for custom hooks.

### Templates
Create custom output templates.