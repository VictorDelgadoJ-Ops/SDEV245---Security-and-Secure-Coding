# The problem here was that the original version did not set things up cleanly enough for the user input.
# It needed a proper starting total, a loop that repeated the right number of times, and a place to store each value.
#
# I fixed it by starting the total at a safe value, asking the user how many numbers they want to add,
# converting each one to a float, and then adding it to the running total.
# After the loop finishes, the program prints the final sum.
# That makes the program much more reliable and easier to understand.

# Simple Python program to calculate the sum of a set of numbers supplied by the user
integer_total = 1
integer_num_count = 1
float_num = 1

num_count = int(input("How many numbers do you want to add? "))

for i in range(num_count):
    float_num = float(input(f"Enter number {i + 1}: "))
    integer_total += float_num

print("The sum of the numbers you entered is:", integer_total)
