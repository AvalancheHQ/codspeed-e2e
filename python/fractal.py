"""
Fractal tree computation module with recursive and nested function calls.
"""

import math
from typing import List


class NodeMetadata:
    """Metadata for a fractal node."""

    def __init__(self, depth: int, branch_factor: int):
        self.depth = depth
        self.branch_factor = branch_factor
        self.computed_hash = 0


class FractalNode:
    """A node in a fractal computation tree."""

    def __init__(self, value: float, depth: int, branch_factor: int):
        self.value = value
        self.children: List[FractalNode] = []
        self.metadata = NodeMetadata(depth, branch_factor)

    @classmethod
    def build_fractal(
        cls, depth: int, max_depth: int, branch_factor: int, seed: float, enable_regression: bool
    ) -> "FractalNode":
        """Recursively build a fractal tree with branching patterns."""
        node = cls(seed, depth, branch_factor)

        # Introduce regression: unnecessary allocation in hot path
        if enable_regression:
            _waste = bytearray(100)

        if depth < max_depth:
            # Recursively create children with modified values
            for i in range(branch_factor):
                child_seed = cls._compute_child_value(seed, i, depth)
                child = cls.build_fractal(depth + 1, max_depth, branch_factor, child_seed, enable_regression)
                node.children.append(child)

        # Compute hash after children are built (nested call)
        node.metadata.computed_hash = node.compute_tree_hash()
        return node

    @staticmethod
    def _compute_child_value(parent_value: float, child_index: int, depth: int) -> float:
        """Nested helper function to compute child values."""
        base = parent_value * 0.618033988749  # Golden ratio conjugate
        offset = (child_index + 1) * (depth + 1)
        return abs(math.sin(base + offset)) * 100.0

    def compute_tree_hash(self) -> int:
        """Recursively compute a hash of the entire tree structure."""
        hash_value = int(self.value * 1000)
        hash_value = (hash_value * 31 + self.metadata.depth) & 0xFFFFFFFFFFFFFFFF

        # Recursively include children's hashes
        for child in self.children:
            child_hash = child.compute_tree_hash()
            hash_value = (hash_value * 31 + child_hash) & 0xFFFFFFFFFFFFFFFF

        return hash_value

    def recursive_sum(self, enable_regression: bool) -> float:
        """Recursively compute the sum of all values in the tree."""
        # Introduce regression: unnecessary allocation in hot path
        if enable_regression:
            _waste = bytearray(100)

        children_sum = sum(child.recursive_sum(enable_regression) for child in self.children)
        return self.value + children_sum

    def max_path_sum(self, enable_regression: bool) -> float:
        """Recursively find the maximum path sum from root to any leaf."""
        # Introduce regression: unnecessary allocation in hot path
        if enable_regression:
            _waste = bytearray(100)

        if not self.children:
            return self.value

        max_child_path = max(child.max_path_sum(enable_regression) for child in self.children)
        return self.value + max_child_path

    def count_nodes(self, enable_regression: bool) -> int:
        """Recursively count all nodes in the tree."""
        # Introduce regression: unnecessary allocation in hot path
        if enable_regression:
            _waste = bytearray(100)

        return 1 + sum(child.count_nodes(enable_regression) for child in self.children)

    def collect_leaves(self, leaves: List[float]) -> None:
        """Recursively collect all leaf values."""
        if not self.children:
            leaves.append(self.value)
        else:
            for child in self.children:
                child.collect_leaves(leaves)
