# Welcome to DevContext

**DevContext** generates AI-ready context from your codebase in 3 seconds.

## Why DevContext?

Every AI coding session starts the same way: you spend 10-15 minutes explaining your codebase. DevContext automates this.

## Quick Start

```bash
pip install devcontext
devcontext generate . -f compact | pbcopy
# Paste to ChatGPT/Claude
```

## Features

- **Fast**: Generates context in 3 seconds
- **Complete**: Extracts functions, classes, imports, structure
- **Language Support**: 20+ programming languages
- **Multiple Formats**: JSON, Markdown, HTML, Compact
- **Works Offline**: No API keys, no internet required
- **Open Source**: MIT license, 100% transparent

## Use Cases

### Daily Development
```bash
devcontext generate . -f compact
```
Paste to AI, get instant relevant help.

### Code Review
```bash
devcontext generate . -o review-context.json
```

### Onboarding
```bash
devcontext generate . -f md > PROJECT_OVERVIEW.md
```

## Documentation

- [Installation](installation.md)
- [CLI Usage](cli.md)
- [API Reference](api.md)
- [Examples](examples.md)
- [FAQ](faq.md)

## Support

- GitHub Issues: https://github.com/jhony91792-oss/devcontext
- Documentation: https://jhony91792-oss.github.io/devcontext/

## License

MIT - free for personal and commercial use.