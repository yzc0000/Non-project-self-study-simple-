def dselect(A, i):
    if len(A) == 1:
        return A[0]

    groups = [A[j:j + 5] for j in range(0, len(A), 5)]
    sorted_groups = [sorted(group) for group in groups]
    medians = [group[len(group) // 2] for group in sorted_groups]
    pivot = dselect(medians, len(medians) // 2)

    lows, highs, pivots = [], [], []
    for x in A:
        if x < pivot:
            lows.append(x)
        elif x > pivot:
            highs.append(x)
        else:
            pivots.append(x)

    k = len(lows)
    if i < k:
        return dselect(lows, i)
    elif i < k + len(pivots):
        return pivot
    else:
        return dselect(highs, i - k - len(pivots))

A = [7, 10, 4, 3, 20, 15, 44, 2, 99, 4]
print(dselect(A, 8))
