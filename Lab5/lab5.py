import math


def input_vector(name):
    return list(map(int, input("Enter " + name + " vector: ").split()))


def input_matrix(m):
    matrix = []
    print("Enter c matrix: ")
    for el in range(m):
        matrix.append(
            list(map(int, input("c row №" + str(el) + ": ").split())))
    return matrix


def shortest_paths(n, v0, adj, capacity, cost):
    vector_d = [math.inf for _ in range(n)]
    vector_d[v0] = 0
    inq = [False for _ in range(n)]
    q = [v0]
    p = [-1 for _ in range(n)]

    while len(q):
        u = q[0]
        del q[0]
        inq[u] = False
        for v in adj[u]:
            if capacity[u][v] > 0 and vector_d[v] > vector_d[u] + cost[u][v]:
                vector_d[v] = vector_d[u] + cost[u][v]
                p[v] = u
                if not inq[v]:
                    inq[v] = True
                    q.append(v)

    return vector_d, p


def min_cost_flow(N, edges, K, s, t, n, m):
    adj = [[] for _ in range(N)]
    cost = [[0 for _ in range(N)] for _ in range(N)]
    capacity = [[0 for _ in range(N)] for _ in range(N)]

    for e in edges:
        adj[e[0]].append(e[1])
        adj[e[1]].append(e[0])
        cost[e[0]][e[1]] = e[3]
        cost[e[1]][e[0]] = -e[3]
        capacity[e[0]][e[1]] = e[2]

    flow = 0
    cost_s = 0

    while flow < K:
        vector_d, p = shortest_paths(N, s, adj, capacity, cost)
        if vector_d[t] == math.inf:
            break

        f = K - flow
        cur = t
        while cur != s:
            f = min(f, capacity[p[cur]][cur])
            cur = p[cur]

        flow += f
        cost_s += f * vector_d[t]
        cur = t

        while cur != s:
            capacity[p[cur]][cur] -= f
            capacity[cur][p[cur]] += f
            cur = p[cur]

    ans = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            ans[i][j] = capacity[j + m + 1][i + 1]

    if flow < K:
        return None
    else:
        return ans


def matrix_transport_task():
    m, n = map(int, input("Enter m and n: ").split(' '))
    matrix_c = input_matrix(m)
    vector_a = input_vector("a")
    vector_b = input_vector("b")

    s = 0
    t = m + n + 1
    sum_a = 0
    sum_b = 0
    edges = []

    for i in range(m):
        for j in range(n):
            edges.append([i + 1, m + j + 1, math.inf, matrix_c[i][j]])

    for i in range(m):
        sum_a += vector_a[i]
        edges.append([0, i + 1, vector_a[i], 0])

    for i in range(n):
        sum_b += vector_b[i]
        edges.append([m + i + 1, n + m + 1, vector_b[i], 0])

    route = min_cost_flow(n + m + 2, edges, min(sum_a, sum_b), s, t, n, m)
    print("Answer matrix: ")
    return '\n'.join([' '.join(list(map(str, map(int, i)))) for i in route])


if __name__ == '__main__':
    print(matrix_transport_task())

#2 2
#4 3
#3 4
#8 2
#5 5


#3 3
#8 4 1
#8 4 3
#9 7 5
#100 300 300
#300 200 200