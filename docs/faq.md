# FAQ — Frequently Asked Questions

## General

**Q: What is DevContext?**
A: DevContext is a CLI tool that generates AI-ready context from any codebase, helping AI assistants understand your project instantly.

**Q: Why was it created?**
A: Developers spend 10-15 minutes per AI session explaining their project. DevContext reduces this to 3 seconds.

**Q: Is it free?**
A: Yes, completely free and open source under MIT license.

## Installation

**Q: How do I install DevContext?**
A: `pip install devcontext`

**Q: What are the requirements?**
A: Python 3.8+ and no external dependencies.

**Q: It says "command not found"**
A: Make sure your pip bin directory is in PATH. Try `pip install --user devcontext`.

## Usage

**Q: What languages are supported?**
A: Python, JavaScript, TypeScript, Go, Rust, Java, C/C++, Ruby, PHP, Swift, Kotlin, Scala, and 15+ more.

**Q: Can I use it with specific AI tools?**
A: Yes! DevContext works with ChatGPT, Claude, Copilot, and any other AI that accepts text input.

**Q: Does it work offline?**
A: Yes, DevContext works completely offline with no external services.

**Q: My project is large. Will it handle it?**
A: Yes, DevContext is optimized to handle 10,000+ files efficiently.

## Technical

**Q: How does it work?**
A: DevContext recursively scans your project, parses code structure, and formats it as AI-optimized JSON or Markdown.

**Q: Is my code sent anywhere?**
A: No. All processing happens locally. Your code never leaves your machine.

**Q: Can I contribute?**
A: Yes! See CONTRIBUTING.md for details.

## Troubleshooting

**Q: Tests are failing**
A: Make sure you're using Python 3.8+. Run tests with `python3 test_runner.py`.

**Q: Missing language support**
A: Open an issue requesting support for your language.

**Q: How do I report bugs?**
A: Use GitHub Issues with the bug report template.

## Misc

**Q: How do I cite DevContext?**
A: Link to the GitHub repo: https://github.com/jhony91792-oss/devcontext

**Q: Will there be a web interface?**
A: Possibly in the future. Star the repo to follow development.

**Q: Can I sponsor development?**
A: See FUNDING.yml for support options.