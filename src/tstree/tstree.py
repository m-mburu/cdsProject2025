# Ternary Search Tree implementation
class TSTreeNode:
    """A node in a tree structure."""
    def __init__(self, char: str):

        """
        Initialize a tree node with a string.
        :param chr: The string to store in the node.
        """

        self._char = char
        self._lt, self._eq, self._gt, self._is_end = None, None, None, False
    # insert a character into the tree

    def _insert(self, string: str, index: int = 0) -> None:

        """
        Insert a string into the tree.
        :param string: The string to insert.
        :param index: The index of the character to compare.
        """
        if index >= len(string):
            self._is_end = True
            return
        # if the character is less than the current node, go left
        char = string[index]
        if char < self._char:
            if self._lt is None:
                self._lt = TSTreeNode(char)
            self._lt._insert(string, index)
        # if the character is greater than the current node, go right
        elif char > self._char:
            if self._gt is None:
                self._gt = TSTreeNode(char)
            self._gt._insert(string, index)
        # if the character is equal to the current node, go down
        else:
            if index == len(string) - 1:
                self._is_end = True
                return
            if self._eq is None:
                self._eq = TSTreeNode(string[index + 1])
            # if the character is the end of the string, mark the node as an
            # end node
            self._eq._insert(string, index+1)

    def _search(self, string: str, index: int = 0) -> bool:
        """
        Search for a string in the tree.
        :param string: The string to search for.
        :param index: The index of the character to compare.
        :return: True if the string is found, False otherwise.
        """
        if index >= len(string):
            return False

        chr = string[index]
        if chr < self._char:
            return self._lt is not None and self._lt._search(string, index)
        elif chr > self._char:
            return self._gt is not None and self._gt._search(string, index)
        else:
            if index == len(string) - 1:
                return self._is_end
            if self._eq is None:
                return False
            return self._eq._search(string, index + 1)
        

    def _all_strings(self, prefix: str = "", strings: list = None) -> None:
        """
        all_strings recursively collects all complete words that exist in the tree.
        It builds words by traversing the tree nodes while maintaining a prefix.
        If it reaches a node marked as the end of a word, it adds the current prefix
        to the results list. The method explores all three branches of each node
        (left, equal, and right) to ensure that all possible words are found and returned.

        :param prefix: Current prefix being built
        :param strings: List to store results
        :return: List of all words in the tree
        """
        if strings is None:
            strings = []
        # Add current character to prefix
            current_prefix = prefix + self._char
            
            # If this is the end of a word, add it to results
            if self._is_end:
                strings.append(current_prefix)
            
            # Continue search in left child (same prefix)
            if self._lt is not None:
                self._lt._all_strings(prefix, strings)
            
            # Continue search in equal child (with updated prefix)
            if self._eq is not None:
                self._eq._all_strings(current_prefix, strings)
            
            # Continue search in right child (same prefix)
            if self._gt is not None:
                self._gt._all_strings(prefix, strings)
            return strings
            
    def  __len__(self) -> int:
        """
        Get the total number of nodes in the subtree rooted at this node.
        
        return: Total node count (including this node and all children).
        """
        length = 1
        if self._lt is not None:
            length += len(self._lt)
        if self._eq is not None:
            length += len(self._eq)
        if self._gt is not None:
            length += len(self._gt)
        return length
