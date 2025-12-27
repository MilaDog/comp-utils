from pytest import fixture
from pytest import raises as pytest_raises

from cp_utils.grids import Grid


@fixture(scope="function")
def empty_grid() -> Grid[str]:
    """Get an empty grid."""
    return Grid([])


@fixture(scope="function")
def grid() -> Grid[str]:
    """Get a pre-populated grid."""
    RAW_GRID: str = "1,2,3\n1,2,3"

    return Grid.parse(RAW_GRID, delim=",")


def test_len_empty_grid(empty_grid: Grid[str]) -> None:
    """Test getting the number of elements in an empty Grid."""
    assert len(empty_grid) == 0


def test_len_grid(grid: Grid[str]) -> None:
    """Test getting the number of elements in an empty Grid."""
    assert len(grid) == 2


def test_grid_count_elements(grid: Grid[str]) -> None:
    """Test getting the number of a certain element in the grid."""
    assert grid.count("1") == 2


def test_empty_grid_get_item(empty_grid: Grid[str]) -> None:
    """Test getting an element from an empty Grid."""
    with pytest_raises(IndexError):
        _ = empty_grid[(1, 1)]


def test_grid_get_item(grid: Grid[str]) -> None:
    """Test getting an element from a Grid."""
    assert grid[(1, 1)] == "2"
    assert grid.get(1, 1) == "2"
    assert grid.get(3, 4, None) is None


def test_empty_grid_set_item(empty_grid: Grid[str]) -> None:
    """Test setting an element in an empty Grid."""
    with pytest_raises(IndexError):
        empty_grid[(1, 1)] = "s"


def test_grid_set_item(grid: Grid[str]) -> None:
    """Test setting an element in a Grid."""
    grid[(1, 1)] = "a"
    assert grid[(1, 1)] == "a"

    grid.set(1, 1, "b")
    assert grid.get(1, 1) == "b"

    with pytest_raises(IndexError):
        grid.set(100, 1, "j")


def test_grid_as_x(grid: Grid[str]) -> None:
    """Test converting the grid into different types."""
    assert grid.as_raw() == [["1", "2", "3"], ["1", "2", "3"]]
    assert grid.as_ints().as_raw() == [[1, 2, 3], [1, 2, 3]]
    assert grid.as_floats().as_raw() == [[1.0, 2.0, 3.0], [1.0, 2.0, 3.0]]
    assert grid.as_ints().as_complex().as_raw() == {0j: 1, 1j: 2, 2j: 3, (1 + 0j): 1, (1 + 1j): 2, (1 + 2j): 3}

    from dataclasses import dataclass

    @dataclass
    class Point:
        """Local point."""

        x: int

    assert grid.as_ints().as_x(lambda x: Point(x)).as_raw() == [
        [Point(x=1), Point(x=2), Point(x=3)],
        [Point(x=1), Point(x=2), Point(x=3)],
    ]


def test_grid_row_col_getting(grid: Grid[str]) -> None:
    """Test getting row(s) / column(s)."""
    assert grid.row(0) == ["1", "2", "3"]
    assert grid.col(0) == ["1", "1"]

    assert grid.rows() == [["1", "2", "3"], ["1", "2", "3"]]
    assert grid.rows() == grid.as_raw()

    assert grid.cols() == [["1", "1"], ["2", "2"], ["3", "3"]]
    assert grid.cols() == grid.transpose().as_raw()


def test_grid_dimensions(grid: Grid[str]) -> None:
    """Test getting the dimensions of the grid."""
    assert grid.dimensions() == (2, 3)


def test_grid_finding(grid: Grid[str]) -> None:
    """Test finding elements in the grid."""
    assert grid.find("1") == (0, 0)
    assert grid.find("4") is None

    assert list(grid.find_all("1")) == [(0, 0), (1, 0)]
    assert list(grid.find_all("4")) == []


def test_grid_get_neighbours_no_diagonals(grid: Grid[str]) -> None:
    """Test getting the neighbours of a position in the grid, without including diagonals."""
    assert set(grid.get_neighbours(1, 1)) == {(0, 1), (1, 0), (1, 2)}


def test_grid_get_neighbours_with_diagonals(grid: Grid[str]) -> None:
    """Test getting the neighbours of a position in the grid, with diagonals."""
    assert set(grid.get_neighbours(1, 1, include_diagonals=True)) == {
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 0),
        (1, 2),
    }


def test_grid_flatten(grid: Grid[str]) -> None:
    """Test flattening the grid."""
    assert grid.flatten() == ["1", "2", "3", "1", "2", "3"]


def test_grid_filter(grid: Grid[str]) -> None:
    """Test filtering the grid."""
    assert grid.filter(lambda x: isinstance(x, str)).as_raw() == [["1", "2", "3"], ["1", "2", "3"]]
    assert grid.filter(lambda x: x == "1", default=None).as_raw() == [["1", None, None], ["1", None, None]]


def test_grid_map(grid: Grid[str]) -> None:
    """Test mapping the grid."""
    assert grid.map(int).as_raw() == [[1, 2, 3], [1, 2, 3]]
