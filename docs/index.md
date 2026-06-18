---
layout: default
title: DevContext — AI-Ready Codebase Context Generator
---

# 🔮 DevContext

<div align="center">

**Give your AI assistant a 200 IQ boost — feed it your entire codebase in 3 seconds.**

[![Stars](https://img.shields.io/github/stars/jhony91792-oss/devcontext?style=social)](https://github.com/jhony91792-oss/devcontext)
[![Tests](https://img.shields.io/github/actions/workflow/status/jhony91792-oss/devcontext/test.yml?style=flat)](https://github.com/jhony91792-oss/devcontext/actions)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)

</div>

## Quick Start

```bash
pip install devcontext
devcontext generate . -o context.json
```

## What It Does

DevContext extracts structured, AI-ready context from any codebase:

- 📊 File tree structure
- 🏗️ Functions and classes
- 📦 Imports and dependencies  
- 🔗 Relationships between files

Paste the output into ChatGPT, Claude, Copilot — any AI assistant instantly knows your project.

## Why DevContext?

Every AI coding assistant fails the same way — **it doesn't know your project**. 

You spend 10-15 minutes every session explaining your codebase. DevContext fixes this.

## Get Started

- [Installation](installation.md)
- [CLI Reference](cli.md)
- [API Documentation](api.md)
- [Examples](examples.md)

## Examples

**Python:**
```bash
devcontext generate ./my-django-api
```

**JavaScript/TypeScript:**
```bash
devcontext generate ./my-nextjs-app
```

**Go:**
```bash
devcontext generate ./my-go-service
```

## License

MIT © jhony91792-oss