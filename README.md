# Competitive Programming Utilities

This repo serves as a collection of useful utility functions for competitive programming, as well as other generic
DSAs.

## Data Structures

### Disjoint Union Set (Union-Find)

#### UnionFindBase

Base implementation of the Union-Find data structure. Requires the own implementation of the `find()` function.

#### UnionFind

Standard implementation of the Union-Find data structure. Requires pre-initialisation.

**Features**
- Generic implementation
- Path compression and union by rank

**Example Usage**
```python
from cp_utils.dsu import UnionFind

# Initialize
elements: list[int] = list(range(1, 6))

uf: UnionFind[int] = UnionFind(data=elements)

# Union operations
uf.union(1, 2)
uf.union(2, 3)
uf.union(4, 5)

# Find operations
print(uf.find(1))  # Returns root of 1's component
print(uf.find(4))  # Returns root of 4's component
print(uf.find(6))  # KeyError - Element `6` not initialised

print(1 in uf)  # True

# Check if connected
print(uf.connected(1, 3))  # True (1-2-3 are connected)
print(uf.connected(1, 4))  # False (different components)

# Getting components
print(uf.get_components())  # {1: {1, 2, 3}, 4: {4, 5}}
print(uf.get_sets())  # Alias for above

# Getting component sizes
print(uf.get_component_sizes())  # {1: 3, 4: 2}
print(uf.get_set_sizes())  # Alias for above

# Number of elements
print(len(uf))  # 5

# Clearing set
uf.clear()

# Deepcopy of set
uf2 = uf.copy()
```

#### DynamicUnionFind

A union-find implementation that adds elements on access should they not exist. This eliminates the need for
explicit initialisation.

**Features**

- Generic implementation
- Auto-adds elements on `find()`
- Path compression and union by rank

**Example Usage**
```python
from cp_utils.dsu import DynamicUnionFind

# Initialize
uf: DynamicUnionFind[int] = DynamicUnionFind()

# Union operations - elements are added automatically
uf.union(1, 2)
uf.union(2, 3)
uf.union(4, 5)

# Find operations
print(uf.find(1))  # Returns root of 1's component
print(uf.find(4))  # Returns root of 4's component

print(1 in uf)  # True

# Check if connected
print(uf.connected(1, 3))  # True (1-2-3 are connected)
print(uf.connected(1, 4))  # False (different components)

# Getting components
print(uf.get_components())  # {1: {1, 2, 3}, 4: {4, 5}}
print(uf.get_sets())  # Alias for above

# Getting component sizes
print(uf.get_component_sizes())  # {1: 3, 4: 2}
print(uf.get_set_sizes())  # Alias for above

# Number of elements
print(len(uf))  # 5

# Clearing set
uf.clear()

# Deepcopy of set
uf2 = uf.copy()
```


## Contributing

Feel free to add more utilities following the same documentation format.

## License

MIT - Use freely in contests and projects.
