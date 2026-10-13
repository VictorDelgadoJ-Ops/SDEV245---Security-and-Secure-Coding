# The problem here was mostly a logic issue, not a security issue.
# The original code was trying to add up values in the list, but it needed a cleaner setup
# so the total started at zero and was updated correctly during the loop.
#
# I fixed it by making a simple sum_array function and setting total to 0 before the loop starts.
# Then I added each number in the list to that total and returned the final result.
# This makes the code easier to follow and gives the correct output.

items = [10, 20, 30, 40, 50]


def sum_array(arr):
    total = 0
    for i in range(len(arr)):
        total += arr[i]
    return total


result = sum_array(items)
print("Sum of elements in the array:", result)
