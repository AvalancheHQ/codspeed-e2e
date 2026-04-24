"""
Benchmark tests using pytest-codspeed.
"""

import pytest
from pytest_codspeed import BenchmarkFixture

from benchmark import complex_fractal_benchmark

@pytest.mark.benchmark
def test_python_fractal_computation(benchmark: BenchmarkFixture):
    """Benchmark the complex fractal computation."""
    result = benchmark(complex_fractal_benchmark, 5, 3, 25)

    # Sanity check that we got a result
    assert isinstance(result, float)
    assert 0 <= result < 1_000_000.0
