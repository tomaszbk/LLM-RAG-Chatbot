def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    # Iterative merge sort
    size = 1
    while size < len(arr):
        left = 0
        while left < len(arr):
            mid = left + size
            right = min(left + 2 * size, len(arr))
            if mid < right:
                merge(arr, left, mid, right)
            left += 2 * size
        size *= 2

def merge(arr, left, mid, right):
    left_array = arr[left:mid]
    right_array = arr[mid:right]

    i = j = 0
    k = left

    while i < len(left_array) and j < len(right_array):
        if left_array[i] < right_array[j]:
            arr[k] = left_array[i]
            i += 1
        else:
            arr[k] = right_array[j]
            j += 1
        k += 1

    while i < len(left_array):
        arr[k] = left_array[i]
        i += 1
        k += 1

    while j < len(right_array):
        arr[k] = right_array[j]
        j += 1
        k += 1

