# We start off by adding the number to the list
numbers = [18, 20, 26, 30, 33, 36]

# We determine the length of the list using length = len(numbers).
# This will help us handle the wrapping behavior when accessing the next number.
length = len(numbers)

# We use a for loop to iterate over the indices of the numbers list.
# The loop variable i represents the current index.
for i in range(length):

    # Inside the loop, we assign the current number to the current_number
    # variable using numbers[i].
    current_number = numbers[i]

    # To find the next number, we use (i + 1) % length. Adding 1 to the current index
    # (i + 1) allows us to access the next index, and using the modulo operator
    # (% length) ensures that the index wraps around to 0 when reaching the end of the list.
    next_number = numbers[(i + 1) % length]

    # We calculate the sum of the current number and the next number by adding current_number
    # and next_number together. This sum is stored in the sum_next variable.
    sum_next = current_number + next_number

    # Finally, we print the value of sum_next for each iteration of the loop.
    print(sum_next)

