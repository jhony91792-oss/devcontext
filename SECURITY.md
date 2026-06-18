# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | ✅ Currently stable |

## Reporting a Vulnerability

If you discover a security vulnerability within DevContext, please create an issue or contact us directly.

We take security seriously. Please include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

We will:
1. Acknowledge receipt within 48 hours
2. Provide an estimated timeline for fix
3. Credit you in the release notes (if desired)

## Security Best Practices

When using DevContext:

1. **Generated context may contain sensitive information** — Do not share generated context publicly without reviewing it first
2. **Review before sharing with AI assistants** — Ensure no secrets or keys are included in the output
3. **Add output files to .gitignore** — Generated context files typically shouldn't be committed

```gitignore
# DevContext output
*.devcontext.json
context.json
```

## General Advice

- Never commit sensitive data to Git
- Use environment variables for secrets
- Review AI assistant outputs before sharing confidential information