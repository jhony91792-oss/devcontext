# Performance profiling for DevContext

import time
import json
import cProfile
import pstats
from typing import Dict, Any, Optional, Callable
from io import StringIO


class PerformanceProfiler:
    """Profile DevContext performance."""
    
    def __init__(self):
        self.timings: Dict[str, float] = {}
        self.profiler: Optional[cProfile.Profile] = None
    
    def profile_function(self, func: Callable, *args, **kwargs) -> tuple:
        """Profile a function execution."""
        self.profiler = cProfile.Profile()
        
        start = time.time()
        self.profiler.enable()
        
        result = func(*args, **kwargs)
        
        self.profiler.disable()
        end = time.time()
        
        self.timings[func.__name__] = end - start
        
        return result, end - start
    
    def get_stats(self) -> str:
        """Get profiling stats as string."""
        if not self.profiler:
            return "No profiling data"
        
        stream = StringIO()
        stats = pstats.Stats(self.profiler, stream=stream)
        stats.sort_stats('cumulative')
        stats.print_stats(20)
        
        return stream.getvalue()
    
    def get_timings(self) -> Dict[str, float]:
        """Get all recorded timings."""
        return self.timings.copy()
    
    def benchmark(self, func: Callable, iterations: int = 10, *args, **kwargs) -> Dict[str, Any]:
        """Benchmark a function."""
        times = []
        
        for _ in range(iterations):
            start = time.time()
            func(*args, **kwargs)
            times.append(time.time() - start)
        
        return {
            "function": func.__name__,
            "iterations": iterations,
            "avg_time": sum(times) / len(times),
            "min_time": min(times),
            "max_time": max(times),
            "total_time": sum(times)
        }


def benchmark_context_generation(path: str = ".", iterations: int = 5) -> Dict[str, Any]:
    """Benchmark context generation."""
    from devcontext import DevContext
    
    profiler = PerformanceProfiler()
    times = []
    
    for i in range(iterations):
        start = time.time()
        dc = DevContext(path)
        dc.generate()
        times.append(time.time() - start)
    
    return {
        "iterations": iterations,
        "avg_time": sum(times) / len(times),
        "min_time": min(times),
        "max_time": max(times),
        "times": times
    }


# CLI
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Performance profiling")
    sub = parser.add_subparsers(dest="command")
    
    bench_cmd = sub.add_parser("benchmark", help="Benchmark generation")
    bench_cmd.add_argument("-p", "--path", default=".", help="Path to benchmark")
    bench_cmd.add_argument("-i", "--iterations", type=int, default=5)
    bench_cmd.add_argument("-o", "--output", help="Output file")
    
    profile_cmd = sub.add_parser("profile", help="Profile a command")
    profile_cmd.add_argument("command", help="Command to profile")
    profile_cmd.add_argument("args", nargs="*", help="Command arguments")
    
    args = parser.parse_args()
    
    if args.command == "benchmark":
        result = benchmark_context_generation(args.path, args.iterations)
        
        output = json.dumps(result, indent=2)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"Benchmark written to {args.output}")
        else:
            print(f"Benchmark Results:")
            print(f"  Iterations: {result['iterations']}")
            print(f"  Average:    {result['avg_time']:.3f}s")
            print(f"  Min:        {result['min_time']:.3f}s")
            print(f"  Max:        {result['max_time']:.3f}s")
    
    elif args.command == "profile":
        print(f"Profiling: {args.command} {' '.join(args.args)}")
        profiler = PerformanceProfiler()
        
        profiler.profiler = cProfile.Profile()
        profiler.profiler.enable()
        
        # Run command (simplified)
        print("Use Python profiling to analyze")


if __name__ == "__main__":
    main()