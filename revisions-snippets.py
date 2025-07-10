

# ==============================================
# Python Key Concepts: Code Snippets & Explanations
# ==============================================
#
# This script demonstrates:
#   1. Memory management and garbage collection
#   2. Pass-by-object-reference
#   3. Shallow copy vs deep copy
#   4. List comprehension
#   5. Decorators
#
# Each section is clearly separated and commented.

# --- 1. Memory Management and Garbage Collection ---
# Python automatically manages memory using reference counting and a cyclic garbage collector.
# The __del__ method is called when an object is about to be destroyed.
# Forcing garbage collection can be useful to immediately reclaim memory for objects with circular references.
import gc

class Demo:
    def __del__(self):
        print("Demo object deleted")

# Create and delete an object to trigger garbage collection
obj = Demo()
del obj  # This should trigger __del__ if no more references exist
gc.collect()  # Forces garbage collection (useful for objects involved in reference cycles)
print("Garbage collection complete\n")


## Dunder methods

# --- Dunder (Magic) Methods ---
# These are special methods in Python that start and end with double underscores (e.g., __init__, __str__).
# They let you customize how objects of your class behave with built-in functions and operators.

class Book:
    def __init__(self, title, pages):
        # __init__ is called when an object is created
        self.title = title
        self.pages = pages

    def __str__(self):
        # __str__ is used when you print the object
        return f"Book: {self.title}, Pages: {self.pages}"

    def __len__(self):
        # __len__ defines behavior for len(obj)
        return self.pages

    def __eq__(self, other):
        # __eq__ defines behavior for obj1 == obj2
        return self.title == other.title and self.pages == other.pages

book1 = Book("Python Basics", 300)
book2 = Book("Python Basics", 300)
book3 = Book("Advanced Python", 400)

print(str(book1))        # Calls __str__
print(len(book1))        # Calls __len__
print(book1 == book2)    # Calls __eq__
print(book1 == book3)    # Calls __eq__



## Self with an object

# --- Understanding 'self' in Python Classes ---
# 'self' represents the instance of the class and is used to access attributes and methods
# associated with that specific object instance.

class Car:
    def __init__(self, brand, model):
        # 'self' is used to assign the parameters to instance variables
        self.brand = brand
        self.model = model

    def display_info(self):
        # 'self' lets us access instance attributes
        return f"Car Brand: {self.brand}, Model: {self.model}"

    def update_model(self, new_model):
        # 'self' is also used to modify instance attributes
        self.model = new_model

    def update_brand(self, new_brand):
        # 'self' is also used to modify instance attributes
        self.brand = new_brand

# Creating an instance of the Car class
my_car = Car("Toyota", "Corolla")

# Display initial car info
print(my_car.display_info())  # Output: Car Brand: Toyota, Model: Corolla

# Update the car model using a method that uses 'self'
my_car.update_model("Camry")

# Display updated car info
print(my_car.display_info())  # Output: Car Brand: Toyota, Model: Camry


# --- 2. Pass-by-Object-Reference ---
# Python function arguments are passed by object reference (sometimes called "pass by assignment").
# Mutable objects (like lists) can be changed inside the function.
# Immutable objects (like ints) cannot be changed in-place; reassignment creates a new object.
def modify_list(lst):
    # Appends 100 to the passed-in list (modifies original list)
    lst.append(100)

my_list = [1, 2, 3]
modify_list(my_list)
print("Modified list (mutable):", my_list)  # [1, 2, 3, 100]

def modify_int(x):
    # This only changes the local reference, not the original variable
    x += 10
    print("Inside function (immutable):", x)

num = 5
modify_int(num)
print("Outside function (immutable):", num, "\n")  # Still 5


# --- 3. Shallow Copy vs Deep Copy ---
# Shallow copy: copies the outer object, but not nested objects.
# Deep copy: recursively copies all nested objects.
import copy

original = [1, 2, [3, 4]]
shallow = copy.copy(original)     # Outer list is copied, inner list is shared
deep = copy.deepcopy(original)    # Everything is copied recursively

shallow[2].append(5)  # Modifies the inner list, affects both original and shallow
print("Original after shallow copy change:", original)  # [1, 2, [3, 4, 5]]
print("Shallow copy:", shallow)                        # [1, 2, [3, 4, 5]]

deep[2].append(6)     # Only affects deep copy
print("Original after deep copy change:", original)     # [1, 2, [3, 4, 5]]
print("Deep copy:", deep, "\n")                         # [1, 2, [3, 4, 6]]


## one more example

# --- Additional Example: Nested Structures in Shallow vs Deep Copy ---
nested_original = [[1, 2], [3, 4], [5, 6]]
nested_shallow = copy.copy(nested_original)
nested_deep = copy.deepcopy(nested_original)

# Modify an inner list in the shallow copy
nested_shallow[0].append(99)
print("Nested Original after shallow modification:", nested_original)
print("Nested Shallow Copy:", nested_shallow)

# Modify an inner list in the deep copy
nested_deep[1].append(88)
print("Nested Original after deep modification:", nested_original)
print("Nested Deep Copy:", nested_deep, "\n")


# --- 4. List Comprehension ---
# List comprehensions provide a concise way to create lists.
# They can include conditions and expressions.
squares = [x**2 for x in range(5)]  # Squares of 0 to 4
print("List comprehension - squares:", squares)

evens = [x for x in range(10) if x % 2 == 0]  # Even numbers from 0 to 9
print("List comprehension with condition - evens:", evens, "\n")


# --- 5. Decorators ---
# Decorators are functions that modify the behavior of other functions.
# Useful for logging, access control, timing, etc.
def my_decorator(func):
    def wrapper():
        print("Before the function call")
        func()
        print("After the function call")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()  # When called, prints messages before and after the function