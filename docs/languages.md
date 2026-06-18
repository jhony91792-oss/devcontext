# Supported Languages

DevContext supports 20+ programming languages out of the box.

## First-Class Support (Full Parsing)

These languages have complete function, class, and import extraction:

| Language | Extensions | Functions | Classes | Imports | 
|----------|------------|-----------|---------|---------|
| Python | `.py`, `.pyw` | ✅ | ✅ | ✅ |
| JavaScript | `.js`, `.mjs`, `.cjs` | ✅ | ✅ | ✅ |
| TypeScript | `.ts`, `.tsx`, `.jsx` | ✅ | ✅ | ✅ |
| Go | `.go` | ✅ | ✅ | ✅ |
| Rust | `.rs` | ✅ | ✅ | ✅ |
| Java | `.java` | ✅ | ✅ | ✅ |
| C | `.c`, `.h` | ✅ | ✅ | ✅ |
| C++ | `.cpp`, `.hpp`, `.cc` | ✅ | ✅ | ✅ |
| C# | `.cs` | ✅ | ✅ | ✅ |
| Ruby | `.rb` | ✅ | ✅ | ✅ |
| PHP | `.php` | ✅ | ✅ | ✅ |
| Swift | `.swift` | ✅ | ✅ | ✅ |
| Kotlin | `.kt`, `.kts` | ✅ | ✅ | ✅ |
| Scala | `.scala` | ✅ | ✅ | ✅ |

## Second-Class Support (File Detection)

These languages are detected and included in file tree, with basic structural awareness:

| Language | Extensions |
|----------|------------|
| Vue | `.vue` |
| Svelte | `.svelte` |
| HTML | `.html`, `.htm` |
| CSS | `.css`, `.scss`, `.sass`, `.less` |
| SQL | `.sql` |
| Shell | `.sh`, `.bash`, `.zsh`, `.fish` |
| PowerShell | `.ps1`, `.psm1` |
| GraphQL | `.graphql`, `.gql` |
| JSON | `.json` |
| YAML | `.yaml`, `.yml` |
| TOML | `.toml` |
| Markdown | `.md`, `.rst` |

## Framework Detection

DevContext can detect these frameworks within supported languages:

- **Python**: Django, Flask, FastAPI, Pandas, NumPy, TensorFlow, PyTorch, SQLAlchemy, Requests, AioHTTP
- **JavaScript/TypeScript**: React, Vue, Angular, Next.js, Express, React Native
- **Go**: Standard library, Gin, Echo, Fiber

## Language Request

Don't see your language? Open an issue with:
1. Language name
2. File extensions
3. Sample code showing function/class syntax

We'll add support in the next release!

## Contributing

To add support for a new language:
1. Add file extension to `LANG_MAP` in `src/devcontext/parser.py`
2. Add regex patterns for functions, classes, imports
3. Add tests
4. Submit a PR