"""
Main benchmark module combining fractal computation with Fibonacci and analysis.
"""

import math
import os
from typing import Dict, List

from fractal import FractalNode

# Read regression flag once at module load time
_REGRESSION_ENABLED = os.getenv("CODSPEED_REGRESSION", "").lower() in ("1", "true")


class TreeAnalysis:
    """Results of fractal tree analysis."""

    def __init__(
        self,
        total_sum: float,
        node_count: int,
        max_path: float,
        leaf_variance: float,
        complexity_score: float,
    ):
        self.total_sum = total_sum
        self.node_count = node_count
        self.max_path = max_path
        self.leaf_variance = leaf_variance
        self.complexity_score = complexity_score


def fibonacci_memo(n: int, memo: Dict[int, int], enable_regression: bool) -> int:
    """Compute Fibonacci with memoization (recursive with nested HashMap operations)."""
    if n <= 1:
        return n

    if n in memo:
        return memo[n]

    # Introduce regression: unnecessary allocation in hot path
    if enable_regression:
        _waste = bytearray(100)

    # Recursive calls with nested memoization
    result = fibonacci_memo(n - 1, memo, enable_regression) + fibonacci_memo(n - 2, memo, enable_regression)
    memo[n] = result
    return result


def compute_variance(values: List[float]) -> float:
    """Nested helper to compute variance."""
    if not values:
        return 0.0

    mean = sum(values) / len(values)
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    return variance


def recursive_path_score(value: float, depth: int) -> float:
    """Recursive helper for path scoring."""
    if depth == 0 or value < 1.0:
        return value

    reduced = value * 0.8
    return 1.0 + recursive_path_score(reduced, depth - 1) * 0.5


def compute_complexity_score(node_count: int, variance: float, max_path: float) -> float:
    """Nested helper to compute complexity score (with recursive internal call)."""
    base_score = math.log(node_count) * math.sqrt(variance)
    path_factor = recursive_path_score(max_path, 5)
    return base_score * path_factor


def analyze_fractal_tree(tree: FractalNode, analysis_depth: int, enable_regression: bool) -> TreeAnalysis:
    """Nested function that analyzes the fractal tree with multiple passes."""
    # First pass: basic metrics (nested recursive calls)
    total_sum = tree.recursive_sum(enable_regression)
    node_count = tree.count_nodes(enable_regression)
    max_path = tree.max_path_sum(enable_regression)

    # Second pass: collect and process leaves (nested operations)
    leaves: List[float] = []
    tree.collect_leaves(leaves)
    leaf_variance = compute_variance(leaves)

    # Third pass: recursive analysis if depth allows
    if analysis_depth > 0:
        nested_analysis = analyze_fractal_tree(tree, analysis_depth - 1, enable_regression)
        return TreeAnalysis(
            total_sum=total_sum + nested_analysis.total_sum * 0.1,
            node_count=node_count,
            max_path=max(max_path, nested_analysis.max_path),
            leaf_variance=(leaf_variance + nested_analysis.leaf_variance) / 2.0,
            complexity_score=compute_complexity_score(node_count, leaf_variance, max_path),
        )
    else:
        return TreeAnalysis(
            total_sum=total_sum,
            node_count=node_count,
            max_path=max_path,
            leaf_variance=leaf_variance,
            complexity_score=compute_complexity_score(node_count, leaf_variance, max_path),
        )


def complex_fractal_benchmark(tree_depth: int, branch_factor: int, fib_n: int) -> float:
    """
    Main benchmark function: Complex fractal tree computation.

    This function combines multiple recursive operations, nested function calls,
    and memoized Fibonacci computation to create a rich computational workload.
    """
    # Use the pre-loaded regression flag (read once at module load time)
    enable_regression = _REGRESSION_ENABLED

    # Build the fractal tree (recursive construction)
    tree = FractalNode.build_fractal(0, tree_depth, branch_factor, 42.0, enable_regression)

    # Perform nested analysis (multiple recursive passes)
    analysis = analyze_fractal_tree(tree, 2, enable_regression)

    # Compute Fibonacci for additional complexity (recursive with memoization)
    memo: Dict[int, int] = {}
    fib_result = float(fibonacci_memo(fib_n, memo, enable_regression))

    # Combine all metrics into final score
    tree_hash = float(tree.compute_tree_hash())
    tree_metric = (
        analysis.total_sum
        + (analysis.node_count * 10.0)
        + analysis.max_path
        + analysis.leaf_variance
    )

    # Return combined score
    return (tree_metric + fib_result + tree_hash) % 1_000_000.0
