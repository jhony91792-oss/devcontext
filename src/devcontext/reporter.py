# Reporter module for DevContext

import json
from typing import Dict, Any, List, Optional
from datetime import datetime


class Reporter:
    """Generate reports from context."""
    
    def __init__(self, context: Dict[str, Any]):
        self.context = context
    
    def generate_summary(self) -> str:
        """Generate summary report."""
        meta = self.context.get("metadata", {})
        files = self.context.get("files", {})
        
        lines = [
            "=" * 60,
            "DEVCONTEXT SUMMARY REPORT",
            "=" * 60,
            "",
            f"Generated: {datetime.now().isoformat()}",
            f"Total Files: {len(files)}",
            f"Languages: {', '.join(meta.get('languages', []))}",
            "",
        ]
        
        return "\n".join(lines)
    
    def generate_files_report(self) -> str:
        """Generate detailed files report."""
        files = self.context.get("files", {})
        
        lines = ["=" * 60, "FILES REPORT", "=" * 60, ""]
        
        # Group by language
        by_lang = {}
        for path, info in files.items():
            if isinstance(info, dict):
                lang = info.get("language", "unknown")
                if lang not in by_lang:
                    by_lang[lang] = []
                by_lang[lang].append((path, info))
        
        for lang in sorted(by_lang.keys()):
            lines.append(f"\n## {lang} ({len(by_lang[lang])} files)")
            for path, info in by_lang[lang][:10]:
                funcs = len(info.get("functions", []))
                classes = len(info.get("classes", []))
                lines.append(f"  {path} ({funcs}f, {classes}c)")
            if len(by_lang[lang]) > 10:
                lines.append(f"  ... and {len(by_lang[lang]) - 10} more")
        
        return "\n".join(lines)
    
    def generate_json_report(self) -> str:
        """Generate JSON report."""
        meta = self.context.get("metadata", {})
        files = self.context.get("files", {})
        
        # Count totals
        total_funcs = sum(
            len(info.get("functions", [])) 
            for info in files.values() 
            if isinstance(info, dict)
        )
        
        total_classes = sum(
            len(info.get("classes", [])) 
            for info in files.values() 
            if isinstance(info, dict)
        )
        
        report = {
            "generated": datetime.now().isoformat(),
            "summary": {
                "total_files": len(files),
                "total_functions": total_funcs,
                "total_classes": total_classes,
                "languages": meta.get("languages", [])
            }
        }
        
        return json.dumps(report, indent=2)
    
    def generate_full_report(self) -> str:
        """Generate complete report."""
        parts = [
            self.generate_summary(),
            "",
            self.generate_files_report(),
            "",
            self.generate_json_report(),
        ]
        
        return "\n".join(parts)


# CLI
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate reports")
    parser.add_argument("input", help="Context JSON file")
    parser.add_argument("-t", "--type", choices=["summary", "files", "json", "full"],
                        default="full")
    parser.add_argument("-o", "--output", help="Output file")
    
    args = parser.parse_args()
    
    with open(args.input) as f:
        context = json.load(f)
    
    reporter = Reporter(context)
    
    if args.type == "summary":
        output = reporter.generate_summary()
    elif args.type == "files":
        output = reporter.generate_files_report()
    elif args.type == "json":
        output = reporter.generate_json_report()
    else:
        output = reporter.generate_full_report()
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Report written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()