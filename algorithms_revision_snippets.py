# --- BINARY SEARCH TREE (BST) ---
# A Binary Search Tree helps us organize numbers (or data) like a smart filing cabinet.
# Every number goes to the left if it's smaller, and to the right if it's bigger.
# This setup makes it easy to find, add, or check numbers quickly — like flipping directly to a letter in a dictionary.

print("\n=== BINARY SEARCH TREE ===")

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left_child = None
        self.right_child = None

class BinarySearchTree:
    def __init__(self):
        self.root_node = None

    def insert_value(self, value):
        if not self.root_node:
            self.root_node = TreeNode(value)
        else:
            self._insert_recursive(self.root_node, value)

    def _insert_recursive(self, current_node, value):
        if value < current_node.value:
            if current_node.left_child:
                self._insert_recursive(current_node.left_child, value)
            else:
                current_node.left_child = TreeNode(value)
        else:
            if current_node.right_child:
                self._insert_recursive(current_node.right_child, value)
            else:
                current_node.right_child = TreeNode(value)

    def find_value(self, value):
        return self._find_recursive(self.root_node, value)

    def _find_recursive(self, current_node, value):
        if current_node is None:
            return False
        if value == current_node.value:
            return True
        elif value < current_node.value:
            return self._find_recursive(current_node.left_child, value)
        else:
            return self._find_recursive(current_node.right_child, value)

    def get_inorder_values(self):
        result = []
        self._inorder_traversal(self.root_node, result)
        return result

    def _inorder_traversal(self, current_node, result):
        if current_node:
            self._inorder_traversal(current_node.left_child, result)
            result.append(current_node.value)
            self._inorder_traversal(current_node.right_child, result)

# Let’s build a simple BST and play with it!
tree = BinarySearchTree()
numbers_to_add = [8, 3, 10, 1, 6, 14, 4, 7]
for number in numbers_to_add:
    tree.insert_value(number)

print("In-order (sorted) values from the tree:", tree.get_inorder_values())  # [1, 3, 4, 6, 7, 8, 10, 14]
print("Is 6 in the tree?", tree.find_value(6))  # True
print("Is 13 in the tree?", tree.find_value(13))  # False