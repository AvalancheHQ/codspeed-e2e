#!/usr/bin/env python3
"""
Main executable program for Python fractal computation.
This is a direct executable (not a benchmark framework test).
"""

from benchmark import complex_fractal_benchmark

if __name__ == "__main__":
    result = complex_fractal_benchmark(7, 4, 35)

    print(f"Fractal computation result: {result}")

    # Sanity check
    assert isinstance(result, float)
    assert 0 <= result < 1_000_000.0
