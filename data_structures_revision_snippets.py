

# This script revises major Python data structures with examples.
# For each data structure, we include:
# - Theoretical explanation
# - Basic operations
# - Their time complexity
# - Performance measurement using time module


# --- Python Data Structures Revision with Code and Time Complexity ---
import time

# --- LISTS ---
# Lists are ordered and mutable.
# You can access, insert, or delete elements.
# Index-based access is fast (O(1)), but inserts/removals can be O(n) if shifting is required.
print("\n=== LISTS ===")
# Lists: Ordered, mutable
my_list = [1, 2, 3, 4]
my_list.append(5)          # O(1) amortized
my_list.insert(2, 10)      # O(n)
print("List after insert:", my_list)  # [1, 2, 10, 3, 4, 5]

# Measuring list traversal time (O(n))
start = time.time()
for item in my_list:
    pass
print("List traversal time:", time.time() - start)


# --- TUPLES ---
# Tuples are ordered and immutable.
# Once created, you cannot modify their contents.
# They're often used for fixed collections of items and are slightly faster than lists.
print("\n=== TUPLES ===")
# Tuples: Ordered, immutable
my_tuple = (1, 2, 3)
print("Tuple element:", my_tuple[1])  # O(1)


# --- SETS ---
# Sets store unordered, unique values.
# Useful for fast membership testing, deduplication, and set operations.
# Insertion, deletion, and lookup are average-case O(1).
print("\n=== SETS ===")
# Sets: Unordered, unique elements
my_set = {1, 2, 3}
my_set.add(4)              # O(1)
my_set.discard(2)          # O(1)
print("Set after add/discard:", my_set)

# Membership check is fast
print("Is 3 in set?", 3 in my_set)    # O(1)


# --- DICTIONARIES ---
# Dictionaries store key-value pairs.
# They're implemented using hash tables.
# Average-case complexity for access, insertion, and deletion is O(1).
print("\n=== DICTIONARIES ===")
# Dicts: Key-value pairs, unordered (but insertion-ordered as of Python 3.7+)
my_dict = {'a': 1, 'b': 2}
my_dict['c'] = 3           # O(1)
print("Dictionary:", my_dict)
print("Access value by key:", my_dict['a'])  # O(1)


# --- LINKED LISTS ---
# A linked list is a linear data structure where each element (node) contains data and a reference to the next node.
# Nodes are not stored in contiguous memory like arrays.
# This makes insertions and deletions efficient at the start or end (with reference), but accessing elements by index is slow.
#
# TIME COMPLEXITY OF COMMON OPERATIONS:
# - Access by index: O(n) → You must traverse the list from the head to the desired index
# - Search (find value): O(n) → You must iterate node-by-node to locate the value
# - Insert at beginning: O(1) → You can update the head pointer directly
# - Insert at end (without tail pointer): O(n) → Traverse to the last node and link a new node
# - Delete at beginning: O(1) → Update the head to the next node
# - Delete at end (without previous reference): O(n) → Traverse to the second last node to unlink the last one
# - Insert or delete at middle: O(n) → You must first reach the index by traversal
print("\n=== LINKED LIST ===")
# Implementing a basic singly linked list
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):  # O(n)
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def print_list(self):
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")

ll = LinkedList()
ll.append(10)
ll.append(20)
ll.append(30)
print("Linked List:")
ll.print_list()


# --- TIME COMPLEXITY DEMOS ---
# Demonstrates how operations scale with input size using time measurement.
# - O(1): Constant time (e.g., direct access)
# - O(n): Linear time (e.g., traversal)
# - O(n^2): Quadratic time (e.g., nested loops)
# These help compare real-world performance implications of different algorithmic complexities.
print("\n=== TIME COMPLEXITY DEMOS ===")

# Constant time: O(1)
def constant_access(data):
    return data[0]

# Linear time: O(n)
def linear_search(data, target):
    for item in data:
        if item == target:
            return True
    return False

# Quadratic time: O(n^2)
def quadratic_demo(data):
    count = 0
    for i in data:
        for j in data:
            count += i * j
    return count

sample_data = list(range(1000))

# Time measurement examples
start = time.time()
constant_access(sample_data)
print("O(1) access time:", time.time() - start)

start = time.time()
linear_search(sample_data, 999)
print("O(n) search time:", time.time() - start)

start = time.time()
quadratic_demo(sample_data[:100])  # Keep size small to avoid long delay

print("O(n^2) demo time:", time.time() - start)


# --- HOW HASH IS CALCULATED IN PYTHON ---
# Python provides a built-in `hash()` function which returns an integer hash value for hashable objects.
# Hashes are used internally by dictionaries and sets to determine where to store values.

# Only immutable objects (like int, str, tuple) can be hashed
# The hash value is used to index into a hash table

print("\n=== HASH FUNCTION ===")
print("Hash of integer 42:", hash(42))
print("Hash of string 'hello':", hash("hello"))
print("Hash of tuple (1, 2):", hash((1, 2)))

# Note: Different runs of Python may produce different hash values for strings due to hash randomization (enabled by default)
# This helps avoid certain types of denial-of-service attacks involving hash collisions

# Custom objects can also be made hashable by implementing __hash__ and __eq__ methods
class Employee:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __hash__(self):
        # Combine id and name into a single hash
        return hash((self.id, self.name))

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name

emp1 = Employee(101, "Alice")
emp2 = Employee(101, "Alice")

print("Hash of emp1:", hash(emp1))
print("Hash of emp2:", hash(emp2))
print("emp1 == emp2:", emp1 == emp2)  # True
print("emp1 is emp2:", emp1 is emp2)  # False (different objects in memory)


# --- DOUBLY LINKED LIST ---
# A doubly linked list is a linear data structure where each node contains:
# - data
# - a pointer to the next node
# - a pointer to the previous node
# This allows bidirectional traversal and efficient insertions/deletions from both ends.
#
# TIME COMPLEXITY:
# - Access/search by value: O(n)
# - Insert/delete at head or tail: O(1)
# - Insert/delete at middle: O(n)

print("\n=== DOUBLY LINKED LIST ===")

class DNode:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):  # O(n)
        new_node = DNode(data)
        if not self.head:
            self.head = new_node
            return
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = new_node
        new_node.prev = curr

    def prepend(self, data):  # O(1)
        new_node = DNode(data)
        new_node.next = self.head
        if self.head:
            self.head.prev = new_node
        self.head = new_node

    def print_forward(self):
        curr = self.head
        while curr:
            print(curr.data, end=" <-> ")
            last = curr
            curr = curr.next
        print("None")

    def print_backward(self):
        curr = self.head
        if not curr:
            print("None")
            return
        while curr.next:
            curr = curr.next
        while curr:
            print(curr.data, end=" <-> ")
            curr = curr.prev
        print("None")

dll = DoublyLinkedList()
dll.append(1)
dll.append(2)
dll.prepend(0)
print("Doubly Linked List forward:")
dll.print_forward()
print("Doubly Linked List backward:")
dll.print_backward()


# --- BINARY TREE ---
# A binary tree is a hierarchical data structure with nodes having up to 2 children.
# The top node is the "root". Each node points to a left and right child.
#
# TIME COMPLEXITY:
# - Insert/Search/Delete in balanced tree: O(log n)
# - In worst-case (skewed tree), operations degrade to O(n)

print("\n=== BINARY TREE ===")

class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

# In-order traversal: Left -> Root -> Right
def inorder_traversal(root):
    if root:
        inorder_traversal(root.left)
        print(root.val, end=" ")
        inorder_traversal(root.right)

# Build a sample tree manually
#         10
#        /  \
#       5    15
#      / \     \
#     2   7     20
root = TreeNode(10)
root.left = TreeNode(5)
root.right = TreeNode(15)
root.left.left = TreeNode(2)
root.left.right = TreeNode(7)
root.right.right = TreeNode(20)

print("In-order traversal of binary tree:")
inorder_traversal(root)
print()



 
# --- STACK ---
# A stack is a linear data structure that follows Last In First Out (LIFO) principle.
# You can push (add) elements to the top and pop (remove) the most recent element.
# It can be implemented using lists or collections.deque in Python.
#
# TIME COMPLEXITY:
# - Push (append): O(1)
# - Pop: O(1)
# - Peek (access top element): O(1)

print("\n=== STACK ===")
stack = []

# Push elements
stack.append(10)
stack.append(20)
stack.append(30)
print("Stack after pushes:", stack)

# Pop element
top = stack.pop()
print("Popped element:", top)
print("Stack after pop:", stack)

# Peek
print("Top element (peek):", stack[-1])


# --- QUEUE ---
# A queue is a linear data structure that follows First In First Out (FIFO) principle.
# You enqueue (add) elements at the back and dequeue (remove) from the front.
# Efficient implementation is done using collections.deque.

from collections import deque

print("\n=== QUEUE ===")
queue = deque()

# Enqueue
queue.append(1)
queue.append(2)
queue.append(3)
print("Queue after enqueue:", list(queue))

# Dequeue
first = queue.popleft()
print("Dequeued element:", first)
print("Queue after dequeue:", list(queue))

# Peek
print("Front element (peek):", queue[0])