package main

func mergeSort(arr []int) []int {
	n := len(arr)
	if n <= 1 {
		return arr
	}

	temp := make([]int, n)
	copy(temp, arr)

	for currSize := 1; currSize < n; currSize *= 2 {
		for leftStart := 0; leftStart < n-1; leftStart += 2 * currSize {
			mid := min(leftStart+currSize-1, n-1)
			rightEnd := min(leftStart+2*currSize-1, n-1)

			merge(temp, leftStart, mid, rightEnd)
		}
	}

	return temp
}

func merge(arr []int, leftStart, mid, rightEnd int) {
	leftSize := mid - leftStart + 1
	rightSize := rightEnd - mid

	left := make([]int, leftSize)
	right := make([]int, rightSize)

	for i := 0; i < leftSize; i++ {
		left[i] = arr[leftStart+i]
	}

	for j := 0; j < rightSize; j++ {
		right[j] = arr[mid+1+j]
	}

	i, j, k := 0, 0, leftStart

	for i < leftSize && j < rightSize {
		if left[i] <= right[j] {
			arr[k] = left[i]
			i++
		} else {
			arr[k] = right[j]
			j++
		}
		k++
	}

	for i < leftSize {
		arr[k] = left[i]
		i++
		k++
	}

	for j < rightSize {
		arr[k] = right[j]
		j++
		k++
	}
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}
