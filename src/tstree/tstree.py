# Ternary Search Tree implementation
class  TSTreeNode:
    """A node in a tree structure."""
    def __init__(self, char: str):

        """
        Initialize a tree node with a string.
        :param chr: The string to store in the node.
        """

        self._char= char
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
                self._lt =  TSTreeNode(char)
            self._lt._insert(string, index)
        # if the character is greater than the current node, go right
        elif char > self._char:
            if self._gt is None:
                self._gt =  TSTreeNode(char)
            self._gt._insert(string, index)
        # if the character is equal to the current node, go down
        else:
            if index == len(string) - 1:
                self._is_end = True
                return
            if self._eq is None:
                self._eq =  TSTreeNode(string[index + 1])
             # if the character is the end of the string, mark the node as an end node
            self._eq._insert(string, index+1)