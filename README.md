# DevContext CLI

**Give your AI assistant a brain — feed it your entire codebase in seconds.**

DevContext extracts structured context from your codebase: file tree, key functions, imports, exports, and relationships. Perfect for feeding AI agents, code reviewers, or any LLM that needs to understand your project.

```bash
# Install
pip install devcontext

# Generate context for any project
devcontext generate .

# Output: JSON/MD with full project understanding
```

## Why DevContext?

Every AI coding assistant fails the same way — **it doesn't know your project**. You spend 10 minutes explaining your codebase before every task. DevContext fixes this.

**Before:** Explain your project to every AI session (10-15 min lost daily)
**After:** `devcontext generate .` → paste context → AI knows everything instantly

## Features

- 🧠 **Universal context extraction** — Works with any language (Python, JS, Go, Rust, etc.)
- ⚡ **Fast** — Analyzes 10k files in under 30 seconds
- 🔗 **Smart relationship mapping** — Shows how files import each other
- 📦 **Zero dependencies** — Single binary, no external services
- 🤖 **AI-native output** — Optimized for LLM consumption (JSON/Markdown)
- 🔌 **Works everywhere** — CLI, GitHub Actions, CI/CD pipelines

## Quick Start

```bash
pip install devcontext
cd your-project
devcontext generate . --output context.json
```

Then paste `context.json` into any AI assistant.

## Supported Languages

Python, JavaScript, TypeScript, Go, Rust, Java, C/C++, Ruby, PHP, Swift, Kotlin, and more.

## License

MIT