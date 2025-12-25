from collections import defaultdict
from copy import deepcopy
from typing import Generic, TypeVar

T = TypeVar("T")


class DynamicUnionFind(Generic[T]):
    """Dynamic Union Find (Disjoint Set Union) data structure implementation."""

    def __init__(self, data: dict[T, T] | None = None):
        self.parent: dict[T, T] = {}
        self.rank: dict[T, int] = defaultdict(int)

        if data is not None:
            self._parse(data=data)

    def _parse(self, data: dict[T, T]) -> None:
        """Parse the given data."""
        for k, v in data.items():
            self.union(x=k, y=v)

    def __len__(self) -> int:
        """Return the number of sets."""
        return len(self.parent)

    def __contains__(self, x: T) -> bool:
        """Check if an element exists in the structure.

        Args:
            x: Element to check.

        Returns:
            True if element has been seen before, False otherwise.
        """
        return x in self.parent

    def __repr__(self) -> str:
        """String representation of the Union-Find structure.

        Returns:
            String showing number of elements and components.
        """
        return f"DynamicUnionFind(elements={len(self)})"

    def find(self, x: T) -> T:
        """Find the root representative of the set containing `x`.

        Args:
            x (T): Element to find the root of.

        Returns:
            T: The found root representative.
        """
        if x not in self.parent:
            self.parent[x] = x

        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])

        return self.parent[x]

    def union(self, x: T, y: T) -> bool:
        """Merge set containing `x` with set containing `y`.

        Args:
            x (T): First element.
            y (T): Second element.

        Returns:
            bool: True if the elements were merged, else False.
        """
        root_x, root_y = self.find(x), self.find(y)

        if root_x == root_y:
            return False

        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y

        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x

        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

        return True

    def connected(self, x: T, y: T) -> bool:
        """Check if two elements are connected.

        Args:
            x (T): Element one.
            y (T): Element two.

        Returns:
            bool: If the elements are connected.
        """
        return self.find(x) == self.find(y)

    def get_components(self) -> dict[T, set[T]]:
        """Get all the connected components.

        Returns:
            dict[T, set[T]]: Dictionary mapping of each root element to a set of all its components.
        """
        components: dict[T, set[T]] = defaultdict(set)

        for element in self.parent.keys():
            root: T = self.find(x=element)
            components[root].add(element)

        return components

    def get_sets(self) -> dict[T, set[T]]:
        """Get all the constructed sets.

        Returns:
            dict[T, set[T]]: Dictionary mapping of each root element to a set of all its components.
        """
        return self.get_components()

    def get_component_sizes(self) -> dict[T, int]:
        """Get all the sizes of the components.

        Returns:
            dict[T, int]: Dictionary mapping of each element to the size of its components.
        """
        return {root: len(members) for root, members in self.get_components().items()}

    def get_set_sizes(self) -> dict[T, int]:
        """Get all the sizes of the set.

        Returns:
            dict[T, int]: Dictionary mapping of each element to the size of its sets.
        """
        return self.get_component_sizes()

    def clear(self) -> None:
        """Clear the DSU."""
        self.parent.clear()

    def copy(self) -> "DynamicUnionFind[T]":
        """Get a deepcopy of the DSU."""
        copy_dsu: DynamicUnionFind[T] = DynamicUnionFind()
        copy_dsu.parent = deepcopy(self.parent)

        return copy_dsu
