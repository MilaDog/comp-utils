# Competitive Programming Utilities

![Package Version](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2FMilaDog%2Fcomp-utils%2Frefs%2Fheads%2Fmain%2Fpyproject.toml&query=%24.project.version&label=version)
![Python Versions](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2FMilaDog%2Fcomp-utils%2Frefs%2Fheads%2Fmain%2Fpyproject.toml&query=%24.project.requires-python&label=requires)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with pyright](https://microsoft.github.io/pyright/img/pyright_badge.svg)](https://microsoft.github.io/pyright/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](https://github.com/MilaDog/comp-utils/blob/main/LICENSE)

This repo serves as a collection of useful utility functions for competitive programming, as well as other generic
DSAs.

## Installation

```commandline
-- install
uv pip install git+https://github.com/MilaDog/comp-utils.git

-- upgrading
uv sync --upgrade-package cp-utils
```

## Documentation

Can find more in-depth documentation in the `./docs` directory.

## What is Available?

### Disjoint Union Set (Union-Find)

#### UnionFindBase

Base implementation of the Union-Find data structure. Requires the own implementation of the `find()` function.

#### UnionFind

Standard implementation of the Union-Find data structure. Requires pre-initialisation.

**Features**

- Generic implementation
- Path compression and union by rank

#### DynamicUnionFind

A union-find implementation that adds elements on access should they not exist. This eliminates the need for
explicit initialisation.

**Features**

- Generic implementation
- Auto-adds elements on `find()`
- Path compression and union by rank

### Grids

#### Grid

Representation of a grid solution, containing various mutation and utility methods.

**Features**

- Generic implementation
- Convert grid into other types, such as floats, integers, complex, or a custom transformation function
- Grid transpose, map, filter, flatten, count

#### ComplexGrid

Representation of a grid as a dictionary of complex points.

**Features**

- Generic implementation

### Files

Simple collection of handling files. main two functions are to `extract_ints` and `extract_floats`.

## Contributing

Feel free to add more utilities following the same documentation format.

## License

MIT - Use freely in contests and projects.
