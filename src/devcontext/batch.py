# Batch processing module for DevContext

import json
import concurrent.futures
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime


class BatchProcessor:
    """Process multiple directories in batch."""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.results: List[Dict[str, Any]] = []
    
    def process_path(self, path: str) -> Dict[str, Any]:
        """Process a single path."""
        from devcontext import DevContext
        
        try:
            dc = DevContext(path)
            context = dc.generate()
            
            return {
                "path": path,
                "success": True,
                "files": len(context.get("files", {})),
                "context": context
            }
        except Exception as e:
            return {
                "path": path,
                "success": False,
                "error": str(e)
            }
    
    def process_batch(self, paths: List[str]) -> List[Dict[str, Any]]:
        """Process multiple paths in parallel."""
        self.results = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.process_path, p): p for p in paths}
            
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                self.results.append(result)
                print(f"{'✅' if result['success'] else '❌'} {result['path']}")
        
        return self.results
    
    def process_file_list(self, list_file: str) -> List[Dict[str, Any]]:
        """Process paths from a file."""
        paths = []
        
        with open(list_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    paths.append(line)
        
        return self.process_batch(paths)


class BatchReport:
    """Generate reports for batch processing."""
    
    def __init__(self, results: List[Dict[str, Any]]):
        self.results = results
    
    def summary(self) -> str:
        """Generate summary report."""
        total = len(self.results)
        successful = sum(1 for r in self.results if r.get("success"))
        failed = total - successful
        total_files = sum(r.get("files", 0) for r in self.results if r.get("success"))
        
        lines = [
            "=" * 60,
            "BATCH PROCESSING REPORT",
            "=" * 60,
            f"Total paths:  {total}",
            f"Successful:   {successful}",
            f"Failed:       {failed}",
            f"Total files:  {total_files}",
            "=" * 60
        ]
        
        if failed > 0:
            lines.append("")
            lines.append("Failed paths:")
            for r in self.results:
                if not r.get("success"):
                    lines.append(f"  ❌ {r['path']}: {r.get('error')}")
        
        return "\n".join(lines)
    
    def json_report(self) -> str:
        """Generate JSON report."""
        total = len(self.results)
        successful = sum(1 for r in self.results if r.get("success"))
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "total": total,
            "successful": successful,
            "failed": total - successful,
            "results": self.results
        }
        
        return json.dumps(report, indent=2)
    
    def save(self, output_file: str, format: str = "text"):
        """Save report to file."""
        if format == "json":
            content = self.json_report()
        else:
            content = self.summary()
        
        with open(output_file, 'w') as f:
            f.write(content)


# CLI
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Batch process directories")
    parser.add_argument("paths", nargs="*", help="Paths to process")
    parser.add_argument("-f", "--file", help="File with list of paths")
    parser.add_argument("-w", "--workers", type=int, default=4, help="Max workers")
    parser.add_argument("-o", "--output", help="Output file")
    parser.add_argument("-j", "--json", action="store_true", help="JSON output")
    
    args = parser.parse_args()
    
    paths = args.paths
    
    if args.file:
        with open(args.file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    paths.append(line)
    
    if not paths:
        print("No paths specified")
        return
    
    processor = BatchProcessor(max_workers=args.workers)
    results = processor.process_batch(paths)
    
    report = BatchReport(results)
    
    if args.output:
        report.save(args.output, "json" if args.json else "text")
        print(f"Report saved to {args.output}")
    else:
        print()
        print(report.summary())


if __name__ == "__main__":
    main()