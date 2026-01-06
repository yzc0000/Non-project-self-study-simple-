import math

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def brute_force(points):
    min_dist = float('inf')
    pair = None
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            d = distance(points[i], points[j])
            if d < min_dist:
                min_dist = d
                pair = (points[i], points[j])
    return min_dist, pair

def strip_closest(strip, delta):    
    min_dist = delta
    pair = None
    n = len(strip)
    for i in range(n):
        for j in range(i + 1, min(i + 7, n)):
            d = distance(strip[i], strip[j])
            if d < min_dist:
                min_dist = d
                pair = (strip[i], strip[j])
    return min_dist, pair

def closest_pair_rec(px, py):
    n = len(px)

    if n <= 3:
        return brute_force(px)
    mid = n // 2
    midpoint = px[mid][0]

    Qx = px[:mid]
    Rx = px[mid:]

    Qy = []
    Ry = []
    for point in py:
        if point[0] <= midpoint:
            Qy.append(point)
        else:
            Ry.append(point)

    dl, pair_left = closest_pair_rec(Qx, Qy)
    dr, pair_right = closest_pair_rec(Rx, Ry)

    if dl < dr:
        delta = dl
        min_pair = pair_left
    else:
        delta = dr
        min_pair = pair_right

    strip = [p for p in py if abs(p[0] - midpoint) < delta]

    ds, pair_strip = strip_closest(strip, delta)

    if ds < delta:
        return ds, pair_strip
    else:
        return delta, min_pair


def closest_pair(points):

    px = sorted(points, key=lambda p: p[0])
    py = sorted(points, key=lambda p: p[1])
    return closest_pair_rec(px, py)



points = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
dist, pair = closest_pair(points)
print(f"En yakın mesafe: {dist}")
print(f"En yakın çift: {pair}")
