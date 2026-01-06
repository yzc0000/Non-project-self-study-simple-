def merge_sort(lst):
    if len(lst) <= 1:
        return lst, 0

    left_half, right_half = split(lst)
    left, inv_left = merge_sort(left_half)
    right, inv_right = merge_sort(right_half)

    l, inv_split = merge(left, right)

    total_inv = inv_left + inv_right + inv_split
    return l, total_inv


def split(lst):
    midpoint = len(lst) // 2
    left = lst[:midpoint]
    right = lst[midpoint:]
    return left, right


def merge(left, right):
    count = 0
    l = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            l.append(left[i])
            i += 1
        else:
            l.append(right[j])
            j += 1
            count += len(left) - i

    l += left[i:]
    l += right[j:]

    return l, count

def verify_sorted(list):
    n = len(list)
    if n == 0 or n == 1:
        return True

    return list[0] <= list[1] and verify_sorted(list[1:])

blacklist = [54, 62, 93, 17, 77, 31, 44, 55, 20]

blacklist, inversion_count = merge_sort(blacklist)
print("Sorted list:", blacklist)
print("Inversion count:", inversion_count)


#DATAYI OKUTMA

def read_data_from_file(filename):
    with open(filename, "r") as file:
        data = file.read().strip().split()
        data = list(map(int, data))
    return data


if __name__ == "__main__":
    data = read_data_from_file("data")
    sorted_list, inversion_count = merge_sort(data)
    print("Sorted list'in ilk 10 elemanı:", sorted_list[:10])
    print("Inversion sayısı:", inversion_count)
