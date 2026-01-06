comparison_count = 0

def quicksort(values, low, high):
    if low < high:
        p = partition(values, low, high)
        quicksort(values, low, p - 1)
        quicksort(values, p + 1, high)

def partition(values, low, high):
    global comparison_count
    pivot = values[low]
    i = low
    for j in range(low + 1, high + 1):
        comparison_count += 1
        if values[j] < pivot:
            i += 1
            values[i], values[j] = values[j], values[i]
    values[low], values[i] = values[i], values[low]
    return i


with open("quicksortdata", "r") as file:
    data = file.read()

arr = list(map(int, data.strip().split()))
quicksort(arr, 0, len(arr) - 1)
print("Sorted array:", arr)
print("Number of comparisons:", comparison_count)
