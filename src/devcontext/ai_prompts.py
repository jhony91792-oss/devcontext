# AI prompt templates for DevContext

from typing import Dict, Any, List


PROMPTS = {
    "debug": """I'm working on a project and need help debugging. Here's my project context:

{context}

The issue I'm facing:
{issue}

Please analyze the context and help me identify the problem and suggest a fix.""",

    "refactor": """I want to refactor this code. Here's my project context:

{context}

Goals:
{goals}

Please suggest refactoring opportunities and help me implement them.""",

    "review": """Please review this code:

{context}

Focus areas:
{focus}

Provide a detailed code review with suggestions for improvement.""",

    "document": """I need to document this project:

{context}

Please help me create documentation including:
- Overview
- Installation
- Usage examples
- API reference""",

    "test": """I need help writing tests for:

{context}

Please generate comprehensive tests covering:
{coverage}
"""
}


def format_prompt(prompt_type: str, context: str, **kwargs) -> str:
    """Format a prompt template with context."""
    template = PROMPTS.get(prompt_type, PROMPTS["debug"])
    
    prompt = template.replace("{context}", context)
    
    for key, value in kwargs.items():
        prompt = prompt.replace(f"{{{key}}}", str(value))
    
    return prompt


def get_prompt(prompt_type: str) -> str:
    """Get a prompt template."""
    return PROMPTS.get(prompt_type, "")


def list_prompts() -> List[str]:
    """List all available prompt types."""
    return list(PROMPTS.keys())


# CLI
def main():
    import argparse
    parser = argparse.ArgumentParser(description="AI prompt templates")
    sub = parser.add_subparsers(dest="command")
    
    list_cmd = sub.add_parser("list", help="List all prompts")
    
    get_cmd = sub.add_parser("get", help="Get prompt template")
    get_cmd.add_argument("type", choices=list(PROMPTS.keys()))
    
    format_cmd = sub.add_parser("format", help="Format a prompt")
    format_cmd.add_argument("type", choices=list(PROMPTS.keys()))
    format_cmd.add_argument("-c", "--context", required=True, help="Context file")
    format_cmd.add_argument("-i", "--issue", help="Issue description")
    format_cmd.add_argument("-g", "--goals", help="Goals")
    format_cmd.add_argument("-f", "--focus", help="Focus areas")
    format_cmd.add_argument("-o", "--output", help="Output file")
    
    args = parser.parse_args()
    
    if args.command == "list":
        print("Available prompts:")
        for name in PROMPTS:
            print(f"  - {name}")
    
    elif args.command == "get":
        print(PROMPTS[args.type])
    
    elif args.command == "format":
        with open(args.context) as f:
            context = f.read()
        
        prompt = format_prompt(
            args.type,
            context,
            issue=args.issue or "No issue specified",
            goals=args.goals or "Improve code quality",
            focus=args.focus or "General review",
            coverage="Main functionality"
        )
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(prompt)
            print(f"Written to {args.output}")
        else:
            print(prompt)


if __name__ == "__main__":
    main()