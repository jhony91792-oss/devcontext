# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | ✅ Yes             |
| < 0.1   | ❌ No              |

## Reporting a Vulnerability

If you discover a security vulnerability within DevContext, please send a private security report:

1. Go to [Security Advisories](https://github.com/jhony91792-oss/devcontext/security/advisories)
2. Click "Report a vulnerability"
3. Provide details about the issue
4. We will respond within 48 hours

## Security Best Practices

### Local Processing
DevContext processes all code locally. No data is sent to external servers during context generation.

### No Network Requests
When generating context, DevContext:
- Does NOT send code to any API
- Does NOT use external services
- Does NOT log or transmit proprietary code

### Safe to Use With
- Proprietary code
- Private repositories
- Security-sensitive projects
- Healthcare/finance code

## Permissions Required

DevContext requires:
- Read access to the project directory (for scanning)
- No network permissions (offline tool)

## GitHub Actions Security

If using the GitHub Actions workflow:
- Context is generated within GitHub's sandboxed environment
- Artifacts are encrypted at rest
- Only repository collaborators can access artifacts

## Best Practices

1. **Review before sharing**: Always review generated context before pasting to AI services
2. **Exclude sensitive files**: Add sensitive paths to `.gitignore` or skip config
3. **Use watch mode securely**: Ensure output files are in safe locations
4. **Audit dependencies**: Regularly run `pip audit` on your environment

## Known Limitations

- DevContext cannot scan encrypted or password-protected files
- Binary files are skipped (no content extraction)
- Very large files (>1MB) may cause memory issues

## Changelog

Security fixes will be documented in [CHANGELOG.md](CHANGELOG.md) with a "Security" label.

---

*Last updated: 2026-06-18*