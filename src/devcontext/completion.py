# Shell completion generator for DevContext

import os
from pathlib import Path
from typing import List


BASH_COMPLETION = '''#!/bin/bash
_devcontext_completion()
{
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    opts="generate tree parse config plugins backup snapshot report"
    subcmds_generate="--output --format --max-depth --analyze --no-stats"
    subcmds_tree="--max-depth --show-lang"
    subcmds_parse="--format"

    case "${prev}" in
        devcontext)
            COMPREPLY=($(compgen -W "${opts}" -- ${cur}))
            return 0
            ;;
        generate)
            COMPREPLY=($(compgen -W "${subcmds_generate}" -- ${cur}))
            return 0
            ;;
        tree)
            COMPREPLY=($(compgen -W "${subcmds_tree}" -- ${cur}))
            return 0
            ;;
        parse)
            COMPREPLY=($(compgen -W "${subcmds_parse}" -- ${cur}))
            return 0
            ;;
        -f|--format)
            COMPREPLY=($(compgen -W "json md html compact" -- ${cur}))
            return 0
            ;;
        -o|--output)
            COMPREPLY=($(compgen -f -- ${cur}))
            return 0
            ;;
    esac
}

complete -F _devcontext_completion devcontext
'''

ZSH_COMPLETION = '''#compdef devcontext

_devcontext() {
    local -a commands
    commands=(
        "generate:Generate context from codebase"
        "tree:Show project tree"
        "parse:Parse single file"
        "config:Configuration management"
        "plugins:Plugin management"
        "backup:Backup management"
        "report:Generate reports"
    )

    _describe 'command' commands
}

devcontext() {
    local -a opts
    opts=(
        "--help[Show help]"
        "--version[Show version]"
    )

    case "$words[1]" in
        generate)
            _devcontext_generate
            ;;
        tree)
            _devcontext_tree
            ;;
    esac
}
'''

FISH_COMPLETION = '''devcontext (Generate AI-ready context from codebases)
    devcontext generate - Generate context from codebase
    devcontext tree - Show project tree
    devcontext parse - Parse single file
    devcontext config - Configuration management
    devcontext plugins - Plugin management
'''


def install_bash_completion(install_path: str = None) -> bool:
    """Install bash completion."""
    if install_path is None:
        install_path = os.path.expanduser("~/.bash_completion.d/devcontext")
    
    Path(install_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(install_path, 'w') as f:
        f.write(BASH_COMPLETION)
    
    return True


def install_zsh_completion(install_path: str = None) -> bool:
    """Install zsh completion."""
    if install_path is None:
        install_path = os.path.expanduser("~/.zsh/completions/_devcontext")
    
    Path(install_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(install_path, 'w') as f:
        f.write(ZSH_COMPLETION)
    
    return True


def install_fish_completion(install_path: str = None) -> bool:
    """Install fish completion."""
    if install_path is None:
        install_path = os.path.expanduser("~/.config/fish/completions/devcontext.fish")
    
    Path(install_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(install_path, 'w') as f:
        f.write(FISH_COMPLETION)
    
    return True


# CLI
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Install shell completions")
    parser.add_argument("-s", "--shell", choices=["bash", "zsh", "fish", "all"], default="all")
    parser.add_argument("-q", "--quiet", action="store_true")
    
    args = parser.parse_args()
    
    shells = ["bash", "zsh", "fish"] if args.shell == "all" else [args.shell]
    
    for shell in shells:
        if shell == "bash":
            success = install_bash_completion()
        elif shell == "zsh":
            success = install_zsh_completion()
        else:
            success = install_fish_completion()
        
        if success and not args.quiet:
            print(f"✅ {shell} completion installed")


if __name__ == "__main__":
    main()