# ARCHITECTURE_PLAN.md

## Project: DevContext CLI

## Overview
DevContext extracts structured context from any codebase to feed AI assistants and agents. Target: 50M+ developers who lose 10-15 min/day explaining projects to AI.

## Architecture

```
devcontext/
├── src/devcontext/
│   ├── __init__.py       # Package init
│   ├── cli.py            # CLI entry point
│   ├── parser.py         # Language-agnostic parser
│   ├── tree.py           # File tree builder
│   ├── analyzer.py       # Code structure analyzer
│   └── output.py         # JSON/MD formatters
├── tests/
│   └── test_devcontext.py
├── docs/
│   └── examples.md
├── pyproject.toml
└── README.md
```

## Core Modules

### 1. cli.py
- Entry point with argparse
- Commands: `generate`, `init`, `config`
- Output formats: JSON, Markdown

### 2. parser.py
- Language detection
- Token extraction
- Import/export parsing

### 3. tree.py
- Recursive file traversal
- Smart filtering (.gitignore-style rules)
- Size calculation

### 4. analyzer.py
- AST analysis for Python
- Regex-based for other languages
- Function/class detection

### 5. output.py
- JSON schema for AI consumption
- Markdown renderer
- Future: XML, YAML

## Data Flow

```
Path → Scanner → Parser → Analyzer → Formatter → Output
         ↓          ↓         ↓
      FileTree    AST/Regex  Structure → JSON/MD
```

## Dependencies
- Zero external dependencies (v1.0)
- Future: tree-sitter for precise AST parsing

## Scalability
- Handles 10k+ files via streaming
- Memory-efficient for large codebases
- CI/CD friendly (fast, no external calls)