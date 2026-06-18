# Shell completion for DevContext

import os
import sys
from pathlib import Path


def generate_bash_completion() -> str:
    """Generate bash completion script."""
    return '''#!/bin/bash
# DevContext bash completion

_devcontext() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    
    opts="generate tree parse --help --version"
    gen_opts="-o --output -f --format --max-depth -a --analyze --no-stats"
    
    case "${COMP_CWORD}" in
        1)
            COMPREPLY=($(compgen -W "${opts}" -- ${cur}))
            ;;
        2)
            case "${prev}" in
                generate)
                    COMPREPLY=($(compgen -d -- ${cur}))
                    ;;
                tree)
                    COMPREPLY=($(compgen -d -- ${cur}))
                    ;;
                parse)
                    COMPREPLY=($(compgen -f -- ${cur}))
                    ;;
            esac
            ;;
        3)
            case "${prev}" in
                -o|--output)
                    COMPREPLY=($(compgen -f -- ${cur}))
                    ;;
                -f|--format)
                    COMPREPLY=($(compgen -W "json md html compact" -- ${cur}))
                    ;;
                --max-depth)
                    COMPREPLY=($(compgen -W "1 2 3 5 10 20" -- ${cur}))
                    ;;
            esac
            ;;
    esac
    
    return 0
}

complete -F _devcontext devcontext
'''


def generate_zsh_completion() -> str:
    """Generate zsh completion script."""
    return '''#compdef devcontext

_devcontext() {
    local -a commands opts
    
    commands=(
        "generate:Generate context from codebase"
        "tree:Show file tree"
        "parse:Parse single file"
    )
    
    opts=(
        "--help[Show help]"
        "--version[Show version]"
    )
    
    if [[ CURRENT -eq 2 ]]; then
        _describe 'command' commands
    else
        _describe 'option' opts
    fi
}

_devcontext "$@"
'''


def generate_fish_completion() -> str:
    """Generate fish completion script."""
    return '''# DevContext fish completion

complete -c devcontext -n '__fish_use_subcommand' -a 'generate' -d 'Generate context'
complete -c devcontext -n '__fish_use_subcommand' -a 'tree' -d 'Show file tree'
complete -c devcontext -n '__fish_use_subcommand' -a 'parse' -d 'Parse file'

complete -c devcontext -s h -l help -d 'Show help'
complete -c devcontext -s v -l version -d 'Show version'
complete -c devcontext -s o -l output -d 'Output file' -r
complete -c devcontext -s f -l format -d 'Format' -w 'json md html compact'
complete -c devcontext -l max-depth -d 'Max depth' -a '1 2 3 5 10 20'
'''


def install_completion(shell: str = None) -> bool:
    """Install completion for the current shell."""
    if shell is None:
        shell = os.path.basename(os.environ.get("SHELL", "bash"))
    
    home = Path.home()
    
    completions_dir = None
    completion_content = None
    
    if shell in ("bash", "sh"):
        completions_dir = home / ".bash_completion.d"
        completion_content = generate_bash_completion()
        completions_dir.mkdir(exist_ok=True)
        (completions_dir / "devcontext").write_text(completion_content)
        
    elif shell in ("zsh",):
        completions_dir = home / ".zsh" / "completions"
        completion_content = generate_zsh_completion()
        completions_dir.mkdir(parents=True, exist_ok=True)
        (completions_dir / "_devcontext").write_text(completion_content)
        
    elif shell in ("fish",):
        completions_dir = home / ".config" / "fish" / "completions"
        completion_content = generate_fish_completion()
        completions_dir.mkdir(parents=True, exist_ok=True)
        (completions_dir / "devcontext.fish").write_text(completion_content)
    
    else:
        return False
    
    return True


def main():
    import argparse
    parser = argparse.ArgumentParser(description="DevContext shell completions")
    parser.add_argument("--bash", action="store_true", help="Generate bash completion")
    parser.add_argument("--zsh", action="store_true", help="Generate zsh completion")
    parser.add_argument("--fish", action="store_true", help="Generate fish completion")
    parser.add_argument("--install", action="store_true", help="Install for current shell")
    parser.add_argument("--print", action="store_true", help="Print completion script")
    
    args = parser.parse_args()
    
    if args.bash:
        print(generate_bash_completion())
    elif args.zsh:
        print(generate_zsh_completion())
    elif args.fish:
        print(generate_fish_completion())
    elif args.install:
        if install_completion():
            print("Completion installed!")
        else:
            print("Failed to install completion")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()