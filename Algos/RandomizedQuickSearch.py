 #not inplace too lazy
import random

def rselect(A, i):

    if len(A) == 1:
        return A[0]

    pivot_index = random.randint(0, len(A) - 1)
    pivot = A[pivot_index]
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
        return rselect(lows, i)
    elif i < k + len(pivots):
        return pivot
    else:
        return rselect(highs, i - k - len(pivots))
A = [7, 10, 4, 3, 20, 15,44,2,99,4]
print(rselect(A, 8))


