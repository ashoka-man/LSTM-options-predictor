def distinct_goodness_values(arr):
    # Use a set to keep track of unique OR results from strictly increasing subsequences
    goodness_set = set()

    # Initialize with an empty subsequence OR value
    dp = [0]

    # Iterate through each element in the array
    for num in arr:
        # Create a new list to store new OR values
        new_dp = []

        # Update the new list with values formed by OR'ing the current number
        for val in dp:
            if not new_dp or num > new_dp[-1]:  # Ensure strictly increasing order
                new_dp.append(val | num)

        # Include the current number itself as a new strictly increasing subsequence
        new_dp.append(num)

        # Update dp with new OR values
        dp.extend(new_dp)

        # Add all current OR values to the set
        goodness_set.update(dp)

    # Include the goodness value of the empty subsequence (0)
    goodness_set.add(0)

    # Convert the set to a sorted list
    sorted_goodness = sorted(goodness_set)
    return sorted_goodness


# Example usage
arr = [4, 6, 1, 1, 5]
goodness_values = distinct_goodness_values(arr)

# Printing the output in the required format
for value in goodness_values:
    print(value)
