# DevContext — Social Media Content

## Twitter/X Thread

**Tweet 1 (launch):**
```
🚀 Built DevContext in one session.

CLI that gives ANY AI assistant instant context about your codebase.

Stop wasting 10 min explaining your project to every new AI chat.

$ pip install devcontext
$ devcontext generate . | pbcopy
→ Paste into ChatGPT/Claude/Copilot

Get 200 IQ boost for your AI assistant ⚡

github.com/jhony91792-oss/devcontext
⭐ if you found it useful!
```

**Tweet 2:**
```
Hot take:

Every AI coding assistant fails the same way.

It doesn't know YOUR project.

You spend 10-15 min every session explaining your codebase.

DevContext fixes this.

3 sec to generate full project context → paste to AI → instant understanding.
```

**Tweet 3:**
```
DevContext supports 20+ languages:
Python, JS, TS, Go, Rust, Java, C++, Ruby, PHP, Swift, Kotlin...

Works offline. Zero config. No API keys.

Try it:
github.com/jhony91792-oss/devcontext
```

## Dev.to Article

```markdown
# I Built an Open-Source CLI That Gives Your AI Assistant a Photographic Memory

## The Problem

Every developer knows this feeling: you open a new AI chat, want to debug something, and then spend the next 10 minutes explaining your project structure, key files, important functions...

**Every. Single. Time.**

This is 10-15 minutes lost per session. If you use AI assistants 5 times a day, that's an hour wasted daily. 5 hours per week. 260 hours per year.

## The Solution

I built DevContext — a CLI that generates AI-ready context from any codebase in seconds.

```bash
pip install devcontext
devcontext generate . -o context.json
```

Paste the output into ChatGPT, Claude, Copilot — any AI assistant — and it instantly knows your entire project.

## How It Works

1. **Scan** — Recursively walks your project, filtering noise (.git, node_modules, __pycache__)
2. **Parse** — Extracts functions, classes, imports, exports from each file
3. **Structure** — Builds a relationship map of your codebase
4. **Output** — Formats as JSON (optimized for AI) or Markdown (for humans)

## Supported Languages

Python, JavaScript, TypeScript, Go, Rust, Java, C/C++, Ruby, PHP, Swift, Kotlin, Scala, and 15+ more.

## Real-World Use Cases

1. **Debugging** — Paste context, get instant relevant help
2. **Code Review** — Generate comprehensive overviews
3. **Onboarding** — New devs understand projects instantly
4. **Documentation** — Auto-generate project structure docs

## Why Open Source?

I believe every developer deserves this. No API keys, no account needed, no cost.

## Try It Out

```bash
pip install devcontext
devcontext generate . | pbcopy
```

Star the repo if you find it useful: https://github.com/jhony91792-oss/devcontext

---
*What other features would you like to see? Comment below!*
```

## Reddit Post (r/programming)

```markdown
Title: [POC] DevContext — CLI that generates AI-ready context from any codebase in 3 seconds

Hey r/programming,

Built this tool to solve a real problem: AI assistants don't know your project.

DevContext scans your codebase, extracts structure (functions, classes, imports), and formats it as JSON optimized for LLM consumption.

GitHub: github.com/jhony91792-oss/devcontext

pip install devcontext && devcontext generate .

Curious if this solves a real pain point for others. Feedback welcome!
```

## Product Hunt Submission

```markdown
Tagline: Give your AI assistant instant context about any codebase

Description: DevContext extracts structured, AI-ready context from any codebase in seconds. Stop wasting 10 minutes explaining your project to every new AI chat session.

Features:
- Zero-config CLI
- 20+ programming languages
- Works offline
- JSON optimized for LLM
- GitHub Actions integration

Category: Developer Tools
```

---

## Share Instructions

1. **Twitter**: Copy tweet thread, post with link
2. **Dev.to**: Copy article, post with embedded code blocks
3. **Reddit**: Post to r/programming or r/python
4. **HackerNews**: Submit at news.ycombinator.com (need account)
5. **LinkedIn**: Post with brief description + link