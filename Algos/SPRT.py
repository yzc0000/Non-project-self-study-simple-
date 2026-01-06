import heapq

jobs_length = [4, 9, 11, 6, 8, 10, 5]
jobs_name = ["Job_A", "Job_B", "Job_C", "Job_D", "Job_E", "Job_F", "Job_G"]
release_times = [0, 3, 10, 14, 22, 33, 44]


def srpt_preemptive(release, proc, names=None):
    n = len(proc)
    if names is None:
        names = [f"Job_{i}" for i in range(n)]
    pending = []
    for i in range(n):
        heapq.heappush(pending, (release[i], i, proc[i], names[i]))

    avail = []
    C = [None] * n
    t = 0

    while avail or pending:
        if not avail and pending and t < pending[0][0]:
            t = pending[0][0]
        while pending and pending[0][0] <= t:
            r, i, p, nm = heapq.heappop(pending)
            heapq.heappush(avail, (p, i, nm))
        if not avail:
            continue
        rem, i, nm = heapq.heappop(avail)
        if pending:
            next_r = pending[0][0]
        else:
            next_r = float("inf")

        if t + rem <= next_r:
            run = rem
        else:
            run = next_r - t
        t += run
        rem -= run
        if rem > 0:
            heapq.heappush(avail, (rem, i, nm))
        else:
            C[i] = t
    return C, t


x = srpt_preemptive(release_times, jobs_length, jobs_name)
print(x)



