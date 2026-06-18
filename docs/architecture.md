# DevContext — Architecture

## Overview

DevContext is a CLI tool that generates AI-ready context from codebases. It's designed to be:
- **Fast**: Processes 10k files in 30 seconds
- **Lightweight**: Zero dependencies
- **Extensible**: Easy to add new language support

## Architecture Diagram

```
User Input (CLI)
     │
     ▼
┌─────────────────┐
│   cli.py        │  Entry point, argument parsing
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   tree.py       │  File system scanning
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  parser.py      │  Language detection, code parsing
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ analyzer.py     │  Complexity, frameworks, endpoints
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  output.py      │  JSON/MD/Compact formatters
└────────┬────────┘
         │
         ▼
   AI-Ready Output
```

## Components

### cli.py
Main entry point. Handles:
- Command-line argument parsing
- Orchestrating the pipeline
- Output formatting

### tree.py
File system operations:
- Recursive directory traversal
- Smart filtering (.gitignore-style rules)
- Skip common non-source directories

### parser.py
Code analysis:
- Language detection by extension
- Regex-based parsing for functions, classes, imports
- Support for 20+ languages

### analyzer.py
Advanced analysis (optional):
- Complexity metrics
- Framework detection
- API endpoint extraction
- Code smell detection

### output.py
Output formatting:
- JSON (default, AI-optimized)
- Markdown (human-readable)
- Compact (minimal for AI prompts)

## Data Flow

1. **Input**: User provides path via CLI
2. **Scan**: `tree.py` recursively lists files
3. **Filter**: Removes noise (node_modules, __pycache__, etc.)
4. **Parse**: `parser.py` extracts code structure
5. **Analyze**: `analyzer.py` computes metrics (if requested)
6. **Format**: `output.py` formats for output
7. **Output**: JSON/MD displayed or saved to file

## Extending DevContext

### Adding Language Support

1. Add extension to `LANG_MAP` in `parser.py`:
```python
'.xyz': 'mylang',
```

2. Add regex patterns for your language:
```python
'mylang': {
    'function': r'...',
    'class': r'...',
    'import': r'...',
},
```

3. Add tests in `tests/test_devcontext.py`

### Adding Output Formats

1. Add formatter function in `output.py`
2. Add CLI flag in `cli.py`
3. Add tests

## Performance Considerations

- **Streaming**: Large directories processed incrementally
- **Caching**: GitHub Actions cache for dependencies
- **Parallel**: Can be extended to use multiprocessing for very large repos

## Security

- All processing is local
- No network requests for code analysis
- No external dependencies (attack surface = 0)
- GitHub Pages served via GitHub's CDN

## Future Architecture

Planned improvements:
- AST-based parsing for precise code analysis
- Language Server Protocol (LSP) integration
- WebAssembly for browser-based execution
- gRPC API for programmatic access