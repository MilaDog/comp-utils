from pytest import fixture
from pytest import raises as pytest_raises

from cp_utils.dsu import UnionFind


@fixture(scope="function")
def dsu() -> UnionFind[str]:
    """Pre-populate DSU with default elements."""
    elements: list[str] = ["a", "b", "c", "d", "e", "f", "g"]

    res: UnionFind[str] = UnionFind(data=elements)

    return res


def test_len_dunder(dsu: UnionFind[str]) -> None:
    """Test getting the length of the DSU."""
    assert len(dsu) == 7


def test_dsu_clear(dsu: UnionFind[str]) -> None:
    """Test clearing the DSU."""
    assert len(dsu) == 7
    dsu.clear()
    assert len(dsu) == 0


def test_find_idempotent(dsu: UnionFind[str]) -> None:
    """Test the finding of elements."""
    root1: str = dsu.find("a")
    root2: str = dsu.find("a")
    assert root1 == root2


def test_union_new_elements(dsu: UnionFind[str]) -> None:
    """Test union of two new elements."""
    with pytest_raises(KeyError):
        _ = dsu.union("x", "y")


def test_union_already_exists(dsu: UnionFind[str]) -> None:
    """Test that an already existing union returns False."""
    res: bool = dsu.union("a", "b")
    assert res is True

    res: bool = dsu.union("a", "b")
    assert res is False


def test_union_self(dsu: UnionFind[str]) -> None:
    """Test union of self."""
    res: bool = dsu.union("a", "a")
    assert res is False


def test_union_chain(dsu: UnionFind[str]) -> None:
    """Test chaining multiple unions."""
    dsu.union("a", "b")
    dsu.union("b", "c")
    dsu.union("c", "d")

    root: str = dsu.find("a")
    assert dsu.find("b") == root
    assert dsu.find("c") == root
    assert dsu.find("d") == root


def test_connected_elements(dsu: UnionFind[str]) -> None:
    """Test if two elements are connected or not."""
    dsu.union("a", "b")
    dsu.union("c", "d")

    assert dsu.connected("a", "b") is True
    assert dsu.connected("a", "c") is False


def test_get_components(dsu: UnionFind[str]) -> None:
    """Test getting all connected components."""
    components: dict[str, set[str]] = dsu.get_components()

    assert len(components) == 7
    assert list(components.values()) == [{"a"}, {"b"}, {"c"}, {"d"}, {"e"}, {"f"}, {"g"}]


def test_multiple_sets(dsu: UnionFind[str]) -> None:
    """Test multiple sets."""
    dsu.union("a", "b")
    dsu.union("c", "d")

    components: dict[str, set[str]] = dsu.get_components()
    assert len(components) == 5

    sizes: list[int] = sorted([len(comp) for comp in components.values()])
    assert sizes == [1, 1, 1, 2, 2]


def test_get_sets_alias(dsu: UnionFind[str]) -> None:
    """Test the `get_sets` alias for `get_components`."""
    assert dsu.get_sets() == dsu.get_components()


def test_get_component_sizes(dsu: UnionFind[str]) -> None:
    """Test getting component sizes."""
    sizes: dict[str, int] = dsu.get_set_sizes()

    assert len(sizes) == 7
    assert list(sizes.values())[0] == 1


def test_get_sets_sizes_alias(dsu: UnionFind[str]) -> None:
    """Test the `get_set_sizes` alias for `get_component_sizes`."""
    assert dsu.get_set_sizes() == dsu.get_component_sizes()


def test_path_compression(dsu: UnionFind[str]) -> None:
    """Test that path compression flattens tree structure."""
    dsu.union("d", "c")
    dsu.union("c", "b")
    dsu.union("b", "a")

    # First find might traverse multiple hops
    root = dsu.find("d")

    # After path compression, d should point directly to root
    assert dsu.parent["d"] == root


def test_union_by_rank(dsu: UnionFind[str]) -> None:
    """Test that union by rank keeps trees balanced."""
    # Create two trees and verify smaller rank attaches to larger
    dsu.union("a", "b")  # Creates tree of rank 1
    dsu.union("c", "d")  # Creates tree of rank 1

    rank_before_a = dsu.rank[dsu.find("a")]
    rank_before_c = dsu.rank[dsu.find("c")]

    dsu.union("a", "c")  # Should increase rank

    final_root = dsu.find("a")
    assert dsu.rank[final_root] > max(rank_before_a, rank_before_c)


def test_singleton_components(dsu: UnionFind[str]) -> None:
    """Test components with only singleton sets."""
    dsu.find("a")
    dsu.find("b")
    dsu.find("c")

    components = dsu.get_components()
    assert len(components) == 7
    for comp in components.values():
        assert len(comp) == 1


# Type Testing
def test_integer_type() -> None:
    """Test DSU with integer elements."""
    dsu = UnionFind[int]([1, 2, 3])
    dsu.union(1, 2)
    dsu.union(2, 3)

    assert dsu.find(1) == dsu.find(3)


def test_tuple_type() -> None:
    """Test DSU with tuple elements."""
    dsu = UnionFind[tuple[int, int]]([(0, 0), (0, 1), (1, 1)])
    dsu.union((0, 0), (0, 1))
    dsu.union((0, 1), (1, 1))

    assert dsu.find((0, 0)) == dsu.find((1, 1))


def test_large_union_find() -> None:
    """Test with larger number of elements."""
    n = 1000
    dsu = UnionFind[int](range(n))

    # Create chain
    for i in range(n - 1):
        dsu.union(i, i + 1)

    # All should be in same component
    root = dsu.find(0)
    for i in range(n):
        assert dsu.find(i) == root

    components = dsu.get_components()
    assert len(components) == 1
    assert len(list(components.values())[0]) == n
