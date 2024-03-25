import pandas as pd
from models import Player


def tournament_sort(arr):
    # Base case: if the array is empty or contains a single element, it is already sorted
    if len(arr) <= 1:
        return arr

    # Recursive case: divide the array into two halves and sort each half
    left_half = tournament_sort(arr[: len(arr) // 2])
    right_half = tournament_sort(arr[len(arr) // 2 :])

    # Merge the two sorted halves into a single sorted array
    return merge(left_half, right_half)


def merge(left: list[Player], right: list[Player]):
    # Initialize an empty list to hold the sorted elements
    sorted_list = []

    # While both lists have elements
    while left and right:
        answer = 0
        # If the first element of the left list is smaller, remove it and append it to the sorted list
        player1 = left[0]
        player2 = right[0]
        print(f"--which one is better? {player1.name}[1] or {player2.name}[2]--")
        while answer not in [1, 2]:
            try:
                answer = int(input("1 or 2: "))
            except ValueError:
                pass
        match answer:
            case 1:
                print(f"You've chosen {player1.name}")
                sorted_list.append(left.pop(0))
            case 2:
                print(f"You've chosen {player2.name}")
                sorted_list.append(right.pop(0))

    # If there are any elements left in either list, append them to the sorted list
    sorted_list.extend(left if left else right)

    return sorted_list


players = list(pd.read_csv("players.csv", header=None, names=["name"])["name"])
players_list = []
for player in players:
    players_list.append(Player(player))

print(tournament_sort(players_list))
