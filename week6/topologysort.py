import sys

sys.setrecursionlimit(100000)

adj = {}
visited = {}
ret = []


def dfs(here):
    if visited[here]:
        return

    visited[here] = True
    if here in adj:
        for there in adj[here]:
            if not visited[there]:
                dfs(there)

    ret.append(str(here))


def main():
    infile = open("../test.in", "r")
    outfile = open("../test.out", "w")

    all_vertices = set()
    indegree_vertices = set()

    lines = [line.strip() for line in infile.readlines() if line.strip()]
    for line in lines:
        start, end = line.split(" -> ")
        start = int(start)
        end = list(map(int, end.split(",")))

        all_vertices.add(start)
        for e in end:
            all_vertices.add(e)
            indegree_vertices.add(e)

        if start in adj:
            adj[start] = adj[start].extend(end)
        else:
            adj[start] = end

    for there in all_vertices:
        visited[there] = False

    for there in all_vertices - indegree_vertices:
        dfs(there)

    outfile.write(", ".join(reversed(ret)))

    infile.close()
    outfile.close()


if __name__ == "__main__":
    main()
