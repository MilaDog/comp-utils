from copy import deepcopy
from typing import Any, Callable, Generic, Iterator, Self, TypeVar, overload

T = TypeVar("T")
U = TypeVar("U")


class Grid(Generic[T]):
    """Wrapper for grid data with various transformation methods."""

    def __init__(self, data: list[list[T]]):
        self._data: list[list[T]] = data

    def __repr__(self) -> str:
        """String representation of grid."""
        return f"Grid[height={len(self._data)}, width={len(self._data[0]) if self._data else 0}]"

    def __str__(self) -> str:
        """Pretty print the grid."""
        return "\n".join("".join(str(row)) for row in self._data)

    def __getitem__(self, key: tuple[int, int]) -> T:
        """Access grid element.

        Args:
            key (tuple[int, int]): Grid position to access.

        Returns:
            T: Found element
        """
        return self._data[key[0]][key[1]]

    def __setitem__(self, key: tuple[int, int], value: T) -> None:
        """Set grid element.

        Args:
            key (tuple[int, int]): Grid position to access.
            value (T): Value to set.
        """
        self._data[key[0]][key[1]] = value

    def __len__(self) -> int:
        """Number of rows in grid.

        Returns:
            int: Number of rows.
        """
        return len(self._data)

    def __iter__(self) -> Iterator[list[T]]:
        """Iterate over rows of the grid.

        Yields:
            list[T]: Each row of the grid.
        """
        return iter(self._data)

    @classmethod
    def parse(cls, grid: str, delim: str = " ", converter: Callable[[str], T] | None = None) -> Self:
        """Parse and return the grid.

        Args:
            grid (str): Content to parse.
            delim (str): Delimiter to split on.
            converter (Callable[[str], T]): Convert the content into a desired type.

        Returns:
            list[list[T]]: Parsed grid.
        """
        content: list[str] = grid.strip().splitlines()
        data: list[list[str]] = [line.split(delim) for line in content]

        if converter is not None:
            return cls(data=[[converter(cell) for cell in row] for row in data])  # type: ignore[arg-type]

        return cls(data=data)  # type: ignore[arg-type]

    @classmethod
    def parse_file(cls, file: str, delim: str = " ", converter: Callable[[str], T] | None = None) -> Self:
        """Parse file and return the grid.

        Args:
            file (str): File to parse.
            delim (str): Delimiter to split on.
            converter (Callable[[str], T]): Convert the content into a desired type.

        Returns:
            list[list[str]]: Parsed grid.
        """
        content: list[str] = open(file, "r").read().strip().splitlines()
        data: list[list[str]] = [line.split(delim) for line in content]

        if converter is not None:
            return cls(data=[[converter(cell) for cell in row] for row in data])  # type: ignore[arg-type]

        return cls(data=data)  # type: ignore[arg-type]

    def as_raw(self) -> list[list[T]]:
        """Get the raw grid.

        Returns:
            list[list[T]]: Original grid.
        """
        return self._data

    @overload
    def as_ints(self: "Grid[str]") -> "Grid[int]": ...

    @overload
    def as_ints(self: "Grid[float]") -> "Grid[int]": ...

    def as_ints(self) -> "Grid[int]":
        """Convert grid elements into integers.

        Returns:
            Grid[int]: Grid instance with integer elements.
        """
        return Grid[int]([[int(cell) for cell in row] for row in self._data])  # type: ignore[arg-type]

    @overload
    def as_floats(self: "Grid[str]") -> "Grid[float]": ...

    @overload
    def as_floats(self: "Grid[int]") -> "Grid[float]": ...

    def as_floats(self) -> "Grid[float]":
        """Convert grid elements into floats.

        Returns:
            Grid[float]: Grid instance with float elements.
        """
        return Grid[float]([[float(cell) for cell in row] for row in self._data])  # type: ignore[arg-type]

    def as_complex(self, func: Callable[[T], U] = lambda x: x) -> "ComplexGrid[U]":
        """Convert grid to complex coordinate dictionary.

        Args:
            func (Callable[[T], U]): Function to transform each cell value. Default: identity.

        Returns:
            ComplexGrid[U]: Returning transformed grid.
        """
        return ComplexGrid(
            data={complex(x, y): func(cell) for x, row in enumerate(self._data) for y, cell in enumerate(row)}
        )

    def as_x(self, func: Callable[[T], U] = lambda x: x) -> "Grid[U]":
        """Convert grid to a custom grid using a specified transformation function.

        Args:
            func (Callable[[T], U]): Function to transform each cell value. Default: identity.

        Returns:
            Grid[U]: Grid instance with transformed values.
        """
        return Grid([[func(cell) for cell in row] for row in self._data])

    def row(self, index: int) -> list[T]:
        """Get a specific row.

        Args:
            index (int): Row index.

        Returns:
            list[T]: The row at the given index.
        """
        return self._data[index]

    def col(self, index: int) -> list[T]:
        """Get a specific column.

        Args:
            index (int): Column index.

        Returns:
            list[T]: The column at the given index.
        """
        return [row[index] for row in self._data]

    def rows(self) -> list[list[T]]:
        """Get all rows (same as as_raw, but more explicit).

        Returns:
            list[list[T]]: All rows in the grid.
        """
        return self._data

    def cols(self) -> list[list[T]]:
        """Get all columns (transposed).

        Returns:
            list[list[T]]: All columns in the grid.
        """
        if not self._data:
            return []
        return [list(col) for col in zip(*self._data)]

    def transpose(self) -> "Grid[T]":
        """Get a transposed grid.

        Returns:
            Grid[T]: Resulting transposed grid.

        Examples:
            >>> grid = Grid([["a", "b", "c"], ["d", "e", "f"]])
            >>> grid.cols()
            [["a", "d"], ["b", "e"], ["c", "f"]]
        """
        return Grid(self.cols())

    def _is_valid(self, row: int, col: int) -> bool:
        """If the position is within the grid bounds.

        Args:
            row (int): Row index.
            col (int): Column index.

        Returns:
            bool: Value position or not.
        """
        height, width = self.dimensions()
        return 0 <= row < height and 0 <= col < width

    def dimensions(self) -> tuple[int, int]:
        """Get the dimensions of the grid.

        Returns:
            tuple[int, int]: Dimensions of the grid.
        """
        if not self._data:
            return 0, 0

        return len(self._data), len(self._data[0]) if self._data else 0

    def get(self, row: int, col: int, default: Any = None) -> Any:
        """Get the element in the grid at position (`row`, `col`). Safely checks bounds.

        Args:
            row (int): Row position.
            col (int): Column position.
            default (Any): Default value to return if nothing was found.

        Returns:
            Any: Found result.
        """
        if self._is_valid(row, col):
            return self._data[row][col]
        return default

    def set(self, row: int, col: int, value: T) -> None:
        """Set the element in the grid at position (`row`, `col`).

        Args:
            row (int): Row position.
            col (int): Column position.
            value (T): Value to set at index.
        """
        self._data[row][col] = value

    def find(self, value: T) -> tuple[int, int] | None:
        """Traverse the grid to find the first instance of `value`, returning the position of the element.

        Args:
            value (T): Value to search for.

        Returns:
            tuple[int, int] | None: Position of the found element, else None.
        """
        for x, row in enumerate(self._data):
            for y, cell in enumerate(row):
                if cell == value:
                    return x, y
        return None

    def find_all(self, value: T) -> list[tuple[int, int]]:
        """Traverse the grid to find the all instances of `value`, returning an iterable of all positions.

        Args:
            value (T): Value to search for.

        Returns:
            list[tuple[int, int]]: Iterable of all found positions of the target value.
        """
        res: list[tuple[int, int]] = []

        for x, row in enumerate(self._data):
            for y, cell in enumerate(row):
                if cell == value:
                    res.append((x, y))

        return res

    def get_neighbours(self, row: int, col: int, include_diagonals: bool = False) -> list[tuple[int, int]]:
        """Get the positions all of neighbouring cells.

        Args:
            row (int): Row index.
            col (int): Column index.
            include_diagonals (bool): Include diagonal neighbours.

        Returns:
            list[tuple[int, int]]: All neighbouring cell positions.
        """
        res: list[tuple[int, int]] = []

        directions: list[tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if include_diagonals:
            directions += [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dx, dy in directions:
            new_x, new_y = row + dx, col + dy

            if self._is_valid(new_x, new_y):
                res.append((new_x, new_y))

        return res

    def flatten(self, func: Callable[[T], T] = lambda x: x) -> list[T]:
        """Flatten the grid into a single list.

        Args:
            func (Callable[[T], T]): Transformation function for each cell. Default: identity.

        Returns:
            list[T]: Flattened grid.
        """
        return [func(cell) for row in self._data for cell in row]

    def filter(self, predicate: Callable[[T], bool], default: T | None = None) -> "Grid[T | None]":
        """Filter grid cells by predicate, replacing non-matching with empty string.

        Args:
            predicate (Callable[[T], bool]): Function that takes a cell value and returns bool.
            default (T | None): Default value.

        Returns:
            Grid[T | None]: New grid with filtered values.
        """
        filtered: list[list[T | None]] = [[cell if predicate(cell) else default for cell in row] for row in self._data]
        return Grid[T | None](filtered)

    def map(self, func: Callable[[T], U]) -> "Grid[U]":
        """Apply function to each cell.

        Args:
            func (Callable[[T], U]): Function to apply to each cell.

        Returns:
            Grid[U]: New grid with transformed values.
        """
        mapped: list[list[U]] = [[func(cell) for cell in row] for row in self._data]
        return Grid[U](mapped)

    def copy(self) -> "Grid[T]":
        """Create a deep copy of the grid.

        Returns:
            Grid[T]: New grid with copied data.
        """
        return Grid([row[:] for row in self._data])

    def count(self, value: T) -> int:
        """Count occurrences of a value in the grid.

        Args:
            value (T): Value to count.

        Returns:
            int: Number of times value appears.
        """
        return sum(1 for row in self._data for cell in row if cell == value)


class ComplexGrid(Generic[T]):
    """Representation of a grid as a dictionary of complex points."""

    def __init__(self, data: dict[complex, T]):
        self._data: dict[complex, T] = data

    def __repr__(self) -> str:
        """String representation of grid."""
        return f"ComplexGrid[data={self._data}]"

    def __getitem__(self, key: complex) -> T | None:
        """Access grid element.

        Args:
            key (complex): Grid position to access.

        Returns:
            T | None: Found element
        """
        return self._data.get(key, None)

    def __setitem__(self, key: complex, value: T) -> None:
        """Set grid element.

        Args:
            key (tuple[int, int]): Grid position to access.
            value (T): Value to set.
        """
        if not self._data.get(key, None):
            raise KeyError(f"Position `{key}` does not exist.")

        self._data[key] = value

    def __len__(self) -> int:
        """Number of elements in grid.

        Returns:
            int: Number of elements.
        """
        return len(self._data)

    def __iter__(self) -> Iterator[complex]:
        """Iterate over the elements in the grid.

        Yields:
            complex: Element in the grid.
        """
        return iter(self._data)

    @classmethod
    def parse(cls, grid: str, delim: str = " ", converter: Callable[[str], T] | None = None) -> Self:
        """Parse and return the grid.

        Args:
            grid (str): Content to parse.
            delim (str): Delimiter to split on.
            converter (Callable[[str], T]): Convert the content into a desired type.

        Returns:
            list[list[str]]: Parsed grid.
        """
        res: dict[complex, str] = {}

        for x, row in enumerate(grid.strip().splitlines()):
            for y, cell in enumerate(row.strip().split(delim)):
                res[complex(x, y)] = cell

        if converter is not None:
            return cls(data={k: converter(v) for k, v in res})  # type: ignore[arg-type]

        return cls(data=res)  # type: ignore[arg-type]

    @classmethod
    def parse_file(cls, file: str, delim: str = " ", converter: Callable[[str], T] | None = None) -> Self:
        """Parse file and return the grid.

        Args:
            file (str): File to parse.
            delim (str): Delimiter to split on.
            converter (Callable[[str], T]): Convert the content into a desired type.

        Returns:
            list[list[str]]: Parsed grid.
        """
        res: dict[complex, str] = {}

        with open(file, "r") as f:
            for x, row in enumerate(f.read().strip().splitlines()):
                for y, cell in enumerate(row.strip().split(delim)):
                    res[complex(x, y)] = cell

        if converter is not None:
            return cls(data={k: converter(v) for k, v in res})  # type: ignore[arg-type]

        return cls(data=res)  # type: ignore[arg-type]

    def as_raw(self) -> dict[complex, T]:
        """Get the data of the grid.

        Returns:
            dict[complex, T]: Data of the grid.
        """
        return self._data

    def copy(self) -> "ComplexGrid[T]":
        """Create a deep copy of the complex grid.

        Returns:
            ComplexGrid[T]: New grid with copied data.
        """
        grid: ComplexGrid[T] = object.__new__(ComplexGrid)
        grid._data = deepcopy(self._data)

        return grid

    def get_neighbours(self, index: complex, include_diagonals: bool = False) -> list[complex]:
        """Get the positions all of neighbouring cells.

        Args:
            index (complex): Index to search around.
            include_diagonals (bool): Include diagonal neighbours.

        Returns:
            list[complex]: All neighbouring cell positions.
        """
        res: list[complex] = []

        directions: list[tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if include_diagonals:
            directions += [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dx, dy in directions:
            new_index: complex = index + complex(dx, dy)

            if new_index in self._data:
                res.append(new_index)

        return res

    def find(self, value: T) -> complex | None:
        """Traverse the grid to find the first instance of `value`, returning the position of the element.

        Args:
            value (T): Value to search for.

        Returns:
            complex | None: Position of the found element, else None.
        """
        for k, v in self._data.items():
            if v == value:
                return k
        return None

    def find_all(self, value: T) -> list[complex]:
        """Traverse the grid to find the all instances of `value`, returning an iterable of all positions.

        Args:
            value (T): Value to search for.

        Returns:
            list[complex]: Iterable of all found positions of the target value.
        """
        return [k for k, v in self._data.items() if v == value]

    def map(self, func: Callable[[T], U]) -> "ComplexGrid[U]":
        """Apply function to each cell.

        Args:
            func (Callable[[T], U]): Function to apply to each cell.

        Returns:
            ComplexGrid[U]: New complex grid with transformed values.
        """
        mapped: dict[complex, U] = {k: func(v) for k, v in self._data.items()}
        return ComplexGrid(mapped)

    def count(self, value: T) -> int:
        """Count occurrences of a value in the grid.

        Args:
            value (T): Value to count.

        Returns:
            int: Number of times value appears.
        """
        return sum(cell == value for cell in self._data.values())
