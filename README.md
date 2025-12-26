# Competitive Programming Utilities

![Package Version](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2FMilaDog%2Fcomp-utils%2Frefs%2Fheads%2Fmain%2Fpyproject.toml&query=%24.project.version&label=version)
![Python Versions](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2FMilaDog%2Fcomp-utils%2Frefs%2Fheads%2Fmain%2Fpyproject.toml&query=%24.project.requires-python&label=requires)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with pyright](https://microsoft.github.io/pyright/img/pyright_badge.svg)](https://microsoft.github.io/pyright/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](https://github.com/MilaDog/comp-utils/blob/main/LICENSE)

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

### Grids

#### Grid

Representation of a grid solution, containing various mutation and utility methods.

**Features**

- Generic implementation
- Convert grid into other types, such as floats, integers, complex, or a custom transformation function
- Grid transpose, map, filter, flatten, count

**Example Usage**

```python
from cp_utils.grids import Grid

RAW_GRID = "1,2,3\n3,2,1\n2,1,3"

# Parse from string
grid: Grid[str] = Grid.parse(RAW_GRID, delim=",")

# Parse from file
grid2: Grid[int] = Grid.parse_file("grid.txt")

# Grid conversions
print(grid.as_raw())  # [['1', '2', '3'], ['3', '2', '1'], ['2', '1', '3']]
print(grid.as_floats().as_raw())  # [[1.0, 2.0, 3.0], [3.0, 2.0, 1.0], [2.0, 1.0, 3.0]]
print(grid.as_complex())  #
print(grid.as_x(func=lambda x: str(x)).as_raw())  # [['1', '2', '3'], ['3', '2', '1'], ['2', '1', '3']]

# rows, cols
print(grid.rows())  # [['1', '2', '3'], ['3', '2', '1'], ['2', '1', '3']]
print(grid.cols())  # same as transpose - [['1', '3', '2'], ['2', '2', '1'], ['3', '1', '3']]
print(grid.dimensions())  # (3, 3)

# Transpose
print(grid.transpose().as_raw())  # [['1', '3', '2'], ['2', '2', '1'], ['3', '1', '3']]

# Searching
print(grid.find("1"))  # first occurrence at (0, 0)
print(grid.find("a"))  # None
print(grid.find_all("1"))  # All occurrences: [(0, 0), (1, 2), (2, 1)]

# Neighbours
print(grid.get_neighbours(1, 1,
                          include_diagonals=True))  # [(0, 1), (2, 1), (1, 0), (1, 2), (0, 0), (0, 2), (2, 0), (2, 2)]

# Filtering
print(grid.filter(predicate=lambda x: x == 3).as_raw())  # [[None, None, None], [None, None, None], [None, None, None]]

# Mapping
print(grid.map(func=lambda x: str((int(x) + 2) % 3)).as_raw())  # [['0', '1', '2'], ['2', '1', '0'], ['1', '0', '2']]

```

#### ComplexGrid

Representation of a grid as a dictionary of complex points.

**Features**

- Generic implementation

**Example Usage**

```python
from cp_utils.grids import ComplexGrid, Grid

RAW_GRID = "1,2,3\n3,2,1\n2,1,3"

# Parse from string
complex_grid: ComplexGrid[int] = ComplexGrid.parse(RAW_GRID, delim=",").map(int)

# Parse from string
grid: Grid[str] = Grid.parse(RAW_GRID, delim=",")

# Parse from file
grid2: Grid[int] = Grid.parse_file("grid.txt")

print(complex_grid)
# ComplexGrid[data={0j: 1, (1+0j): 2, (2+0j): 3, 1j: 3, (1+1j): 2, (2+1j): 1, 2j: 2, (1+2j): 1, (2+2j): 3}]

complex_grid[complex(0, 1)] = 10
print(complex_grid[complex(0, 1)])  # 10

# invalid access
print(complex_grid[complex(10, 10)])  # None

try:
    complex_grid[complex(10, 10)] = 2
except KeyError as e:
    print(e)  # Position `(10+10j)` does not exist.

print(len(complex_grid))  # 9 elements

print(complex_grid.as_raw())  # {0j: 1, (1+0j): 2, (2+0j): 3, 1j: 3, (1+1j): 2, (2+1j): 1, 2j: 2, (1+2j): 1, (2+2j): 3}

print(complex_grid.get_neighbours(complex(1, 1),
                                  include_diagonals=True))  # [1j, (2+1j), (1+0j), (1+2j), 0j, 2j, (2+0j), (2+2j)]

print(complex_grid.map(func=lambda x: str(x)).as_raw())
# {0j: '1', (1+0j): '2', (2+0j): '3', 1j: '10', (1+1j): '2', (2+1j): '1', 2j: '2', (1+2j): '1', (2+2j): '3'}

print(complex_grid.find(1))  # 0j
print(complex_grid.find_all(1))  # [0j, (2+1j), (1+2j)]
print(complex_grid.find(4))  # None
print(complex_grid.find_all(4))  # []
```

### Files

Simple collection of handling files. main two functions are to `extract_ints` and `extract_floats`.

## Contributing

Feel free to add more utilities following the same documentation format.

## License

MIT - Use freely in contests and projects.
