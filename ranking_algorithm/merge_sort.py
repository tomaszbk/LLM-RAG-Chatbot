import os


total_questions=0


def merge_sort(arr):
    
    if len(arr) > 1:
        mid = len(arr) // 2  # Find the middle of the array
        left_half = arr[:mid]  # Divide the array into two halves
        right_half = arr[mid:]

        merge_sort(left_half)  # Recursively sort the left half
        merge_sort(right_half)  # Recursively sort the right half

        i, j, k = 0, 0, 0

        # Merge the two halves
        while i < len(left_half) and j < len(right_half):
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"1: {left_half[i]}")
            print(f"2: {right_half[j]}")
            choice = input("1 or 2? ")
            global total_questions
            total_questions+=1
            if choice == '1':
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1
            print("")

        # Check for any remaining elements in both halves
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1
    print(f"Total questions: {total_questions}")

# Example usage:
my_list = ["jujutsu", 'fma', 'haikyu', 'spy family', 'naruto']
print("Original List:", my_list)

merge_sort(my_list)
print("Sorted List:", my_list)
