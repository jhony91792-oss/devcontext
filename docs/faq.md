# FAQ

Frequently asked questions about DevContext.

## General

### What is DevContext?
DevContext is a CLI tool that generates AI-ready context from codebases. Instead of manually explaining your project to an AI assistant, you run one command and get a complete context dump in 3 seconds.

### Why use DevContext?
- Save 10-15 minutes per AI coding session
- Get consistent, complete context
- Never miss important details
- Works offline, no API keys needed

### Is it free?
Yes, DevContext is 100% free and open source under MIT license.

## Installation

### How do I install DevContext?
```bash
pip install devcontext
```

### What are the requirements?
- Python 3.8 or higher
- pip or pip3

### Can I install from source?
```bash
git clone https://github.com/jhony91792-oss/devcontext.git
cd devcontext
pip install -e .
```

## Usage

### How do I use it?
```bash
# Generate context
devcontext generate .

# Copy to clipboard for AI
devcontext generate . -f compact | pbcopy
```

### What formats are supported?
- JSON (default)
- Markdown
- HTML
- Compact (minified JSON)

### How do I exclude directories?
Create a `.devcontextrc` file:
```json
{
    "skip_dirs": ["node_modules", ".git"]
}
```

## Troubleshooting

### No files found
- Check the path is correct
- Try with `-a` flag for analysis
- Verify files have supported extensions

### Slow on large projects
- Use `--max-depth` to limit scan depth
- Add large directories to skip list

### Memory issues
- Scan subdirectories separately
- Use compact format

## GitHub

### How do I star the project?
Visit https://github.com/jhony91792-oss/devcontext and click the star button.

### How do I report issues?
Open an issue at https://github.com/jhony91792-oss/devcontext/issues

### Can I contribute?
Yes! Open a pull request. See CONTRIBUTING.md for details.