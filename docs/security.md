# Security Guide

DevContext security considerations.

## Overview

DevContext is a read-only tool that analyzes code. It does not modify files or send data to external servers (unless using optional notification features).

## Security Features

### 1. Local Processing
All context generation happens locally. No data is sent to external servers.

### 2. Path Validation
DevContext validates file paths to prevent path traversal attacks:
- Blocks `..` in paths
- Warns about absolute paths

### 3. File Access Controls
- Respects `.gitignore` patterns
- Skips sensitive directories (.git, etc.)

## Best Practices

### 1. Use Ignore Patterns
```json
{
    "skip_dirs": [".git", "node_modules", "__pycache__"],
    "skip_files": ["*.env", "*.pem", "*.key"]
}
```

### 2. Review Generated Context
Before sharing context publicly, review for:
- API keys
- Passwords
- Personal information
- proprietary code

### 3. GitHub Actions
When using DevContext in CI:
- Store credentials in GitHub Secrets
- Don't log sensitive data

## Potential Risks

### Sensitive Data in Context
If your project contains:
- API keys
- Passwords
- Private keys
- Environment files

These may appear in generated context.

**Mitigation**: Use skip patterns to exclude sensitive files.

### Webhooks
If using notification webhooks:
- Keep webhook URLs private
- Use signed payloads when available

## Reporting Security Issues

If you find a security vulnerability, please email:
- private@github.com (via GitHub Security Advisories)

## Updates

DevContext is actively maintained. Always use the latest version: