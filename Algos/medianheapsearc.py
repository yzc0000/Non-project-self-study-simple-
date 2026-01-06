import heapq

def median_maintenance(numbers):
    max_heap = []
    min_heap = []
    med_sum = 0

    for x in numbers:

        if not max_heap or x <= -max_heap[0]:
            heapq.heappush(max_heap, -x)
        else:
            heapq.heappush(min_heap, x)
        if len(max_heap) > len(min_heap) + 1:
            heapq.heappush(min_heap, -heapq.heappop(max_heap))
        elif len(min_heap) > len(max_heap):
            heapq.heappush(max_heap, -heapq.heappop(min_heap))

        med = -max_heap[0]
        med_sum += med

    return med_sum % 10000
