from pytest import fixture
from pytest import raises as pytest_raises

from cp_utils.grids import ComplexGrid


@fixture(scope="function")
def empty_complex_grid() -> ComplexGrid[str]:
    """Get an empty ComplexGrid."""
    return ComplexGrid({})


@fixture(scope="function")
def complex_grid() -> ComplexGrid[str]:
    """Pre-populate ComplexGrid with default elements."""
    RAW_GRID: str = "1,2,3\n1,2,3"

    return ComplexGrid.parse(RAW_GRID, delim=",")


def test_len_empty_complex_grid(empty_complex_grid: ComplexGrid[str]) -> None:
    """Test getting the number of elements in an empty ComplexGrid."""
    assert len(empty_complex_grid) == 0


def test_len_complex_grid(complex_grid: ComplexGrid[str]) -> None:
    """Test getting the number of elements in an empty ComplexGrid."""
    assert len(complex_grid) == 6


def test_empty_complex_grid_get_item(empty_complex_grid: ComplexGrid[str]) -> None:
    """Test getting an element from an empty ComplexGrid."""
    assert empty_complex_grid[complex(1, 1)] is None


def test_complex_grid_get_item(complex_grid: ComplexGrid[str]) -> None:
    """Test getting an element from a ComplexGrid."""
    assert complex_grid[complex(1, 1)] == "2"


def test_empty_complex_grid_set_item(empty_complex_grid: ComplexGrid[str]) -> None:
    """Test setting an element in an empty ComplexGrid."""
    with pytest_raises(KeyError):
        empty_complex_grid[complex(1, 1)] = "s"


def test_complex_grid_set_item(complex_grid: ComplexGrid[str]) -> None:
    """Test setting an element in a ComplexGrid."""
    complex_grid[complex(1, 1)] = "a"
    assert complex_grid[complex(1, 1)] == "a"


def test_complex_grid_get_neighbours_no_diagonals(complex_grid: ComplexGrid[str]) -> None:
    """Test getting the neighbours of a position in the ComplexGrid, without including diagonals."""
    assert set(complex_grid.get_neighbours(complex(1, 1))) == {complex(0, 1), complex(1, 0), complex(1, 2)}


def test_complex_grid_get_neighbours_with_diagonals(complex_grid: ComplexGrid[str]) -> None:
    """Test getting the neighbours of a position in the ComplexGrid, with diagonals."""
    assert set(complex_grid.get_neighbours(complex(1, 1), include_diagonals=True)) == {
        complex(0, 0),
        complex(0, 1),
        complex(0, 2),
        complex(1, 0),
        complex(1, 2),
    }


def test_complex_grid_map(complex_grid: ComplexGrid[str]) -> None:
    """Test the mapping of the elements in the ComplexGrid."""
    new_complex_grid: ComplexGrid[int] = complex_grid.map(int)

    assert new_complex_grid.as_raw() == {0j: 1, 1j: 2, 2j: 3, (1 + 0j): 1, (1 + 1j): 2, (1 + 2j): 3}


def test_complex_grid_count(complex_grid: ComplexGrid[str]) -> None:
    """Test counting the number of elements in the ComplexGrid."""
    assert complex_grid.count("1") == 2


def test_complex_grid_find(complex_grid: ComplexGrid[str]) -> None:
    """Test finding the first element in the ComplexGrid."""
    assert complex_grid.find("1") == complex(0, 0)
    assert complex_grid.find("3") == complex(0, 2)
    assert complex_grid.find("4") is None


def test_complex_grid_find_all(complex_grid: ComplexGrid[str]) -> None:
    """Test finding all occurrences of an element in the ComplexGrid."""
    assert set(complex_grid.find_all("2")) == {complex(0, 1), complex(1, 1)}
    assert list(complex_grid.find_all("4")) == []
