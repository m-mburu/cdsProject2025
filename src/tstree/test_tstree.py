from tstree import TSTree


def test_tstree():
    print("🔍 Starting tests for TSTree...")

    tree = TSTree()

    # Test empty tree
    assert len(tree) == 0
    assert tree.search("hello") == False
    assert tree.all_strings() == []
    print("Empty tree checks passed")

    # Insert strings
    words = ["cat", "car", "cart", "dog", "door", "dot"]
    for word in words:
        tree.insert(word)

    # Test length (total number of nodes, not just strings)
    total_nodes = len(tree)
    print(f"ℹTotal nodes in tree: {total_nodes}")
    assert total_nodes > len(words)

    # Test search
    for word in words:
        assert tree.search(word) == True

    assert tree.search("cab") == False
    assert tree.search("do") == False
    assert tree.search("cars") == False
    print("Search tests passed")

    # Test all_strings
    strings = tree.all_strings()
    assert sorted(strings) == sorted(words)
    print("all_strings() test passed")

    # Test __repr__
    tree_repr = repr(tree)
    print("Tree structure:\n")
    print(tree_repr)
    assert isinstance(tree_repr, str)
    print(" __repr__ test passed")

    print("All TSTree tests passed successfully.")


# Only run tests if this file is executed directly
if __name__ == "__main__":
    test_tstree()
