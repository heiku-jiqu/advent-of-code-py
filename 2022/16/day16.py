import re
from collections import deque

if __name__ == "__main__":
    with open("input.txt") as f:
        input = f.readlines()

    # parse input
    valves = {}
    flows = {}
    for line in input:
        match = re.match(
            "Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.*)",
            line.strip(),
        )
        src, flow, dest_unparsed = match.groups()
        flow = int(flow)
        dest_list = dest_unparsed.split(", ")

        # append to dict
        valves[src] = dest_list
        flows[src] = flow

    # use bfs on every non-zero node to find shortest path to other nodes
    distances = {}
    for valve in valves:
        # ignore non-AA valves that have 0 flowrates
        if valve != "AA" and flows[valve] == 0:
            continue

        # bfs
        distances[valve] = {valve: 0}
        queue = deque([(valve, 0)])
        visited = {valve}
        while queue:
            current, d = queue.popleft()
            for neighbor in valves[current]:
                if neighbor in visited:
                    continue
                visited.add(neighbor)
                if flows[neighbor]:  # only include if neighbor has flowrate
                    distances[valve][neighbor] = d + 1
                queue.append((neighbor, d + 1))

    cache = {}
    valve_index = {valve: i for i, valve in enumerate(distances.keys())}

    def search(time, valve, valve_state) -> int:
        if (time, valve, valve_state) in cache:
            return cache[(time, valve, valve_state)]

        maxval = 0
        for neighbor in distances[valve]:

            neighbor_bit = 1 << valve_index[neighbor]
            # continue if neighbor already already opened
            if neighbor_bit & valve_state:
                continue

            time_remaining = time - distances[valve][neighbor] - 1
            # continue if travelling to neighbor causes no time left
            if time_remaining <= 0:
                continue
            maxval = max(
                maxval,
                search(time_remaining, neighbor, valve_state | neighbor_bit)
                + flows[neighbor] * time_remaining,
            )

        cache[(time, valve, valve_state)] = maxval
        return maxval

    part2_ans = 0
    xor_mask = (1 << len(valve_index)) - 1
    for state in range(xor_mask + 1):
        part2_ans = max(
            part2_ans, search(26, "AA", state) + search(26, "AA", state ^ xor_mask)
        )

    part1_ans = search(30, "AA", 0)
    print(f"Part 1: {part1_ans}")
    print(f"Part 2: {part2_ans}")
