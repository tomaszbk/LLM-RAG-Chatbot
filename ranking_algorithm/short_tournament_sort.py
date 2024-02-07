def tournament_sort(arr, cmp):
    # Base case: if the array is empty or contains a single element, it is already sorted
    if len(arr) <= 1:
        return arr

    # Calculate the midpoint of the array using regular division
    mid = len(arr) // 2

    # Recursive case: divide the array into two halves and sort each half
    left_half = tournament_sort(arr[:mid], cmp)
    right_half = tournament_sort(arr[mid:], cmp)

    # Merge the two sorted halves into a single sorted array
    return merge(left_half, right_half, cmp)

def merge(left, right, cmp):
    # Initialize an empty list to hold the sorted elements
    sorted_list = []

    # While both lists have elements
    while left and right:
        # If the first element of the left list is smaller, remove it and append it to the sorted list
        if not cmp(left[0], right[0]):
            sorted_list.append(left.pop(0))
        # Otherwise, remove the first element of the right list and append it to the sorted list
        else:
            sorted_list.append(right.pop(0))

    # If there are any elements left in either list, append them to the sorted list
    sorted_list.extend(left if left else right)

    return sorted_list