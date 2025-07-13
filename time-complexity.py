# --- Time Complexity Examples ---
# Time complexity describes how the runtime of an algorithm scales with input size (n).
# Below are examples of common complexities.

import time

# O(1) - Constant Time
def constant_time_example(items):
    # Always accesses the first element, regardless of list size
    return items[0]

# O(n) - Linear Time
def linear_time_example(items):
    # Iterates once over the entire list
    for item in items:
        print(item)

# O(n^2) - Quadratic Time
def quadratic_time_example(items):
    # Nested loop: for each item, loop again through all items
    for i in items:
        for j in items:
            print(i, j)

# Example list
data = list(range(5))

print("O(1) result:", constant_time_example(data))  # Output: 0

print("\nO(n) result:")
linear_time_example(data)  # Output: 0 1 2 3 4

print("\nO(n^2) result:")

quadratic_time_example(data)
# Output: (0,0), (0,1), ... (4,4)


# --- Measuring Execution Time of Different Complexities ---
# This section shows how to *measure* execution time of each function to observe scaling.

import time

# Helper function to measure execution time
def measure_time(func, arg):
    start = time.time()
    func(arg)
    end = time.time()
    print(f"Execution time for {func.__name__}: {end - start:.6f} seconds\n")

# Define a larger dataset to better observe time differences
large_data = list(range(1000))

# Redefine quadratic function for measurement purposes
def quadratic_time_example_large(items):
    for i in items:
        for j in items:
            _ = i + j  # Perform some operation

# Redefine linear function for measurement purposes
def linear_time_example_large(items):
    for item in items:
        _ = item * 2

# Redefine constant time function
def constant_time_example_large(items):
    _ = items[0]

# Measure execution time for each
measure_time(constant_time_example_large, large_data)
measure_time(linear_time_example_large, large_data)
measure_time(quadratic_time_example_large, large_data)

# Notes:
# - Constant time should remain nearly the same regardless of input size.
# - Linear time will grow with input size.
# - Quadratic time will grow with the square of input size (very noticeable with large n).


# --- Understanding Time Complexity Intuition ---
# When calculating time complexity manually:
# - Count how many times operations are repeated as input size (n) increases.
# - Look at loops: single loop = O(n), nested loops = O(n^2), etc.
# - Recursive calls with half-sized inputs often imply O(log n) or O(n log n).

# --- O(log n) Time Complexity with Binary Search ---
# Binary search works on sorted arrays by cutting the search space in half each step.
# At each step, it discards half the elements, leading to log2(n) comparisons in worst case.

def binary_search(arr, target):
    low = 0
    high = len(arr) - 1
    steps = 0  # Count how many times we cut the array

    while low <= high:
        steps += 1
        mid = (low + high) // 2
        if arr[mid] == target:
            print(f"Found {target} in {steps} steps (O(log n))")
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    print(f"{target} not found after {steps} steps")
    return -1

# Example usage
sorted_list = list(range(1, 1001))  # Sorted list from 1 to 1000
binary_search(sorted_list, 768)    # Should find it quickly using O(log n)

binary_search(sorted_list, 1001)   # Should not find it, still log(n) steps


# --- O(n log n) Time Complexity Example ---
# O(n log n) often arises in algorithms that divide the data (log n splits) and then process each part (n items).
# Example: Merge Sort divides the list recursively (log n) and merges (n) at each level.

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    # Divide the list into halves
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    # Merge sorted halves
    return merge(left, right)

def merge(left, right):
    sorted_list = []
    i = j = 0

    # Merge two sorted arrays
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            sorted_list.append(left[i])
            i += 1
        else:
            sorted_list.append(right[j])
            j += 1

    # Append remaining elements
    sorted_list.extend(left[i:])
    sorted_list.extend(right[j:])
    return sorted_list

# Example usage
unsorted = [9, 3, 7, 1, 6, 2, 5, 8, 4]
sorted_result = merge_sort(unsorted)
print("Sorted using merge sort (O(n log n)):", sorted_result)


