from pytest import fixture

from cp_utils.dsu import DynamicUnionFind


@fixture(scope="function")
def empty_dsu() -> DynamicUnionFind[str]:
    """Empty DSU for tests."""
    return DynamicUnionFind()


@fixture(scope="function")
def dsu() -> DynamicUnionFind[str]:
    """Pre-populate DSU with default elements."""
    relationships: list[tuple[str, str]] = [
        ("a", "b"),
        ("a", "c"),
        ("b", "c"),
        ("d", "e"),
        ("e", "a"),
        ("e", "f"),
        ("f", "g"),
    ]

    res: DynamicUnionFind[str] = DynamicUnionFind()

    for a, b in relationships:
        res.union(a, b)

    return res


def test_len_dunder(dsu: DynamicUnionFind[str]) -> None:
    """Test getting the length of the DSU."""
    assert len(dsu) == 7


def test_len_dunder_empty(empty_dsu: DynamicUnionFind[str]) -> None:
    """Test getting the length of the DSU."""
    assert len(empty_dsu) == 0


def test_dsu_clear(dsu: DynamicUnionFind[str]) -> None:
    """Test clearing the DSU."""
    assert len(dsu) == 7
    dsu.clear()
    assert len(dsu) == 0


def test_find_idempotent(dsu: DynamicUnionFind[str]) -> None:
    """Test the finding of elements."""
    root1: str = dsu.find("a")
    root2: str = dsu.find("a")
    assert root1 == root2


def test_union_new_elements(empty_dsu: DynamicUnionFind[str]) -> None:
    """Test union of two new elements."""
    res: bool = empty_dsu.union("x", "y")
    assert res is True
    assert empty_dsu.find("x") == empty_dsu.find("y")


def test_union_already_exists(dsu: DynamicUnionFind[str]) -> None:
    """Test that an already existing union returns False."""
    res: bool = dsu.union("a", "b")
    assert res is False


def test_union_self(dsu: DynamicUnionFind[str]) -> None:
    """Test union of self."""
    res: bool = dsu.union("a", "a")
    assert res is False


def test_union_chain(empty_dsu: DynamicUnionFind[str]) -> None:
    """Test chaining multiple unions."""
    empty_dsu.union("a", "b")
    empty_dsu.union("b", "c")
    empty_dsu.union("c", "d")

    root: str = empty_dsu.find("a")
    assert empty_dsu.find("b") == root
    assert empty_dsu.find("c") == root
    assert empty_dsu.find("d") == root


def test_connected_elements(empty_dsu: DynamicUnionFind[str]) -> None:
    """Test if two elements are connected or not."""
    empty_dsu.union("a", "b")
    empty_dsu.union("c", "d")

    assert empty_dsu.connected("a", "b") is True
    assert empty_dsu.connected("a", "c") is False


def test_get_components(dsu: DynamicUnionFind[str]) -> None:
    """Test getting all connected components."""
    components: dict[str, set[str]] = dsu.get_components()

    assert len(components) == 1
    assert list(components.values())[0] == {"a", "b", "c", "d", "e", "f", "g"}


def test_get_empty_components(empty_dsu: DynamicUnionFind[str]) -> None:
    """Test getting components of an empty DSU."""
    assert empty_dsu.get_components() == {}


def test_multiple_sets(empty_dsu: DynamicUnionFind[str]) -> None:
    """Test multiple sets."""
    empty_dsu.union("a", "b")
    empty_dsu.union("c", "d")

    components: dict[str, set[str]] = empty_dsu.get_components()
    assert len(components) == 2

    sizes: list[int] = sorted([len(comp) for comp in components.values()])
    assert sizes == [2, 2]


def test_get_sets_alias(dsu: DynamicUnionFind[str]) -> None:
    """Test the `get_sets` alias for `get_components`."""
    assert dsu.get_sets() == dsu.get_components()


def test_get_component_sizes(dsu: DynamicUnionFind[str]) -> None:
    """Test getting component sizes."""
    sizes: dict[str, int] = dsu.get_set_sizes()

    assert len(sizes) == 1
    assert list(sizes.values())[0] == 7


def test_get_sets_sizes_alias(dsu: DynamicUnionFind[str]) -> None:
    """Test the `get_set_sizes` alias for `get_component_sizes`."""
    assert dsu.get_set_sizes() == dsu.get_component_sizes()


def test_path_compression(empty_dsu: DynamicUnionFind[str]) -> None:
    """Test that path compression flattens tree structure."""
    empty_dsu.union("d", "c")
    empty_dsu.union("c", "b")
    empty_dsu.union("b", "a")

    # First find might traverse multiple hops
    root = empty_dsu.find("d")

    # After path compression, d should point directly to root
    assert empty_dsu.parent["d"] == root


def test_union_by_rank(empty_dsu: DynamicUnionFind[str]) -> None:
    """Test that union by rank keeps trees balanced."""
    # Create two trees and verify smaller rank attaches to larger
    empty_dsu.union("a", "b")  # Creates tree of rank 1
    empty_dsu.union("c", "d")  # Creates tree of rank 1

    rank_before_a = empty_dsu.rank[empty_dsu.find("a")]
    rank_before_c = empty_dsu.rank[empty_dsu.find("c")]

    empty_dsu.union("a", "c")  # Should increase rank

    final_root = empty_dsu.find("a")
    assert empty_dsu.rank[final_root] > max(rank_before_a, rank_before_c)


def test_init_with_data() -> None:
    """Test initialization with pre-existing data."""
    data = {"a": "b", "c": "d", "b": "d"}
    dsu = DynamicUnionFind(data)

    # All should be in same component
    assert dsu.find("a") == dsu.find("d")
    assert dsu.find("c") == dsu.find("d")


def test_init_empty() -> None:
    """Test initialization without data."""
    dsu = DynamicUnionFind[int]()
    assert len(dsu.parent) == 0
    assert len(dsu.rank) == 0


def test_singleton_components(empty_dsu: DynamicUnionFind[str]) -> None:
    """Test components with only singleton sets."""
    empty_dsu.find("a")
    empty_dsu.find("b")
    empty_dsu.find("c")

    components = empty_dsu.get_components()
    assert len(components) == 3
    for comp in components.values():
        assert len(comp) == 1


# Type Testing
def test_integer_type() -> None:
    """Test DSU with integer elements."""
    dsu = DynamicUnionFind[int]()
    dsu.union(1, 2)
    dsu.union(2, 3)

    assert dsu.find(1) == dsu.find(3)


def test_tuple_type() -> None:
    """Test DSU with tuple elements."""
    dsu = DynamicUnionFind[tuple[int, int]]()
    dsu.union((0, 0), (0, 1))
    dsu.union((0, 1), (1, 1))

    assert dsu.find((0, 0)) == dsu.find((1, 1))


def test_large_union_find() -> None:
    """Test with larger number of elements."""
    dsu = DynamicUnionFind[int]()
    n = 1000

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
