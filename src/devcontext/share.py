# Share module for DevContext - generates shareable content

import json
from typing import Dict, Any, List, Optional
from pathlib import Path


def generate_twitter_content(repo_url: str = "https://github.com/jhony91792-oss/devcontext") -> List[str]:
    """Generate Twitter thread content."""
    return [
        f"🧵 1/{len(_TWITTER_THREAD)} DevContext: CLI который экономит 10-15 минут каждый день",
        "Каждый раз когда вы объясняете AI-ассистенту свой код - вы теряете время.",
        f"DevContext генерирует полный контекст проекта за 3 секунды. Бесплатно. Open source.",
        "Поддерживает 20+ языков: Python, JS, TS, Go, Rust, Java, C++, Ruby и другие.",
        "Установка: pip install devcontext",
        f"GitHub: {repo_url}",
        "#DevTools #OpenSource #AI #Python #CLI",
    ]


def generate_hackernews_title() -> str:
    """Generate HN-ready title."""
    return "Show DevContext: CLI that generates AI-ready context from your codebase in 3 seconds"


def generate_hackernews_body() -> str:
    """Generate HN post content."""
    return """**DevContext** is a CLI tool that I built to solve a problem I faced every day.

**The Problem:**
Before every AI coding session, I spent 10-15 minutes explaining my codebase structure, key files, and dependencies. This was repetitive and time-consuming.

**The Solution:**
DevContext generates a complete, AI-ready context from any codebase in 3 seconds.

**Features:**
- 20+ programming languages supported
- Zero configuration required
- Works offline, no API keys needed
- Outputs JSON, Markdown, or compact format
- MIT licensed, 100% open source

**Quick Demo:**
```bash
pip install devcontext
devcontext generate . -f compact
```

Then paste the output to ChatGPT/Claude and get instant relevant help.

**Links:**
- Repo: https://github.com/jhony91792-oss/devcontext
- Docs: https://jhony91792-oss.github.io/devcontext/

Would love your feedback! Ask me anything about the project."""


def generate_devto_article() -> Dict[str, str]:
    """Generate Dev.to article content."""
    return {
        "title": "I Built a CLI That Saves Me 10-15 Minutes Every Day",
        "body": """# I Built a CLI That Saves Me 10-15 Minutes Every Day

Every developer knows this frustration: you want to use AI to help with your code, but first you have to spend 10-15 minutes explaining your entire codebase.

## The Problem

When you start a new AI coding session, you need to provide context:
- Project structure
- Key files and their purposes
- Dependencies
- Important functions and classes

This is repetitive. It's tedious. It's a waste of time.

## The Solution: DevContext

I built a CLI tool that generates complete AI-ready context from any codebase in 3 seconds.

```bash
pip install devcontext
devcontext generate .
```

That's it. No configuration. No API keys. Works offline.

## Supported Languages

Python, JavaScript, TypeScript, Go, Rust, Java, C, C++, Ruby, PHP, Swift, Kotlin, Scala, and more.

## Output Formats

- **JSON**: For programmatic use
- **Markdown**: For human reading  
- **Compact**: Optimized for AI prompts (50% smaller)

## Real-World Use Cases

### Daily Standup
```bash
devcontext generate ./recent-changes -o standup.json
```

### Code Review
```bash
devcontext generate . -f compact | pbcopy
# Paste to ChatGPT with your PR link
```

### Debugging
```bash
devcontext generate . -f compact
# Paste to Claude with error message
```

## Why It's Different

| Feature | DevContext | Others |
|---------|------------|--------|
| Zero config | ✅ | ❌ |
| No API keys | ✅ | ❌ |
| Works offline | ✅ | ❌ |
| Open source | ✅ | ❌ |
| Free | ✅ | ❌ |

## Try It Out

```bash
pip install devcontext
devcontext generate . -f compact
```

Feedback welcome! Star the repo if it helps you too.

**GitHub**: https://github.com/jhony91792-oss/devcontext""",
        "tags": ["python", "cli", "opensource", "devtools", "productivity"],
        "canonical_url": "https://github.com/jhony91792-oss/devcontext"
    }


def generate_social_share(repo_url: str = "https://github.com/jhony91792-oss/devcontext") -> Dict[str, str]:
    """Generate all social content."""
    return {
        "twitter": "\n".join(generate_twitter_content(repo_url)),
        "hackernews_title": generate_hackernews_title(),
        "hackernews_body": generate_hackernews_body(),
        "devto": generate_devto_article(),
        "reddit": generate_reddit_post(),
    }


def generate_reddit_post() -> str:
    """Generate Reddit post content."""
    return """DevContext - CLI that generates AI-ready context from your codebase

I built this to solve my daily frustration: spending 10-15 minutes explaining code structure to AI before getting any actual help.

**What it does:**
- Scans any codebase and extracts structure
- Identifies functions, classes, imports
- Generates context in 3 seconds

**Install:**
```
pip install devcontext
```

**Demo:**
```
devcontext generate . -f compact
```

Supports 20+ languages, outputs JSON/Markdown/compact, MIT licensed.

Repo: https://github.com/jhony91792-oss/devcontext

Questions welcome!"""


# Content stored for easy access
_TWITTER_THREAD = [
    "🧵 DevContext: CLI который экономит 10-15 минут каждый день",
    "Каждый раз когда вы объясняете AI-ассистенту свой код - вы теряете время.",
    f"DevContext генерирует полный контекст проекта за 3 секунды. Бесплатно. Open source.",
    "Поддерживает 20+ языков: Python, JS, TS, Go, Rust, Java, C++, Ruby и другие.",
    "Установка: pip install devcontext",
    "GitHub: https://github.com/jhony91792-oss/devcontext",
    "#DevTools #OpenSource #AI #Python #CLI",
]


def get_all_content() -> Dict[str, Any]:
    """Get all shareable content."""
    return {
        "twitter_thread": _TWITTER_THREAD,
        "hackernews": {
            "title": generate_hackernews_title(),
            "body": generate_hackernews_body(),
        },
        "devto_article": generate_devto_article(),
        "reddit_post": generate_reddit_post(),
    }