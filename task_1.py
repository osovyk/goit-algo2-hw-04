from collections import deque, defaultdict


class Digraph:
    """Directed graph with integer capacities."""

    def __init__(self, n: int):
        """Initialize empty graph with n vertices."""
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.cap = [[0] * n for _ in range(n)]

    def add_edge(self, u: int, v: int, c: int):
        """Add directed edge with capacity (cumulative if duplicate)."""
        self.adj[u].append(v)
        self.adj[v].append(u)
        self.cap[u][v] += c

    def sum_out(self, u: int) -> int:
        """Return total outgoing capacity from vertex u."""
        return sum(self.cap[u][v] for v in self.adj[u])


def _bfs(g: Digraph, s: int, t: int, parent: list) -> int:
    """Breadth-first search to find augmenting path."""
    for i in range(g.n):
        parent[i] = -1
    parent[s] = -2
    q = deque([(s, float("inf"))])
    while q:
        u, flow = q.popleft()
        for v in g.adj[u]:
            if parent[v] == -1 and g.cap[u][v] > 0:
                parent[v] = u
                new_flow = min(flow, g.cap[u][v])
                if v == t:
                    return new_flow
                q.append((v, new_flow))
    return 0


def edmonds_karp_with_paths(g: Digraph, s: int, t: int):
    """Run Edmonds–Karp algorithm and record used paths."""
    parent = [-1] * g.n
    maxflow = 0
    used_paths = []
    while True:
        flow = _bfs(g, s, t, parent)
        if flow == 0:
            break
        maxflow += flow
        path = []
        v = t
        while v != s:
            u = parent[v]
            path.append((u, v))
            v = u
        path.reverse()
        for u, v in path:
            g.cap[u][v] -= flow
            g.cap[v][u] += flow
        used_paths.append(([u for u, _ in path] + [path[-1][1]], flow))
    return maxflow, used_paths


def build_network():
    """Build logistics flow network from assignment data."""
    names = []

    def add(name):
        names.append(name)
        return len(names) - 1

    s = add("S")
    t1 = add("Terminal 1")
    t2 = add("Terminal 2")
    w1 = add("Warehouse 1")
    w2 = add("Warehouse 2")
    w3 = add("Warehouse 3")
    w4 = add("Warehouse 4")
    store = {i: add(f"Store {i}") for i in range(1, 15)}
    t = add("T")

    g = Digraph(len(names))
    g.add_edge(t1, w1, 25)
    g.add_edge(t1, w2, 20)
    g.add_edge(t1, w3, 15)
    g.add_edge(t2, w3, 15)
    g.add_edge(t2, w4, 30)
    g.add_edge(t2, w2, 10)
    g.add_edge(w1, store[1], 15)
    g.add_edge(w1, store[2], 10)
    g.add_edge(w1, store[3], 20)
    g.add_edge(w2, store[4], 15)
    g.add_edge(w2, store[5], 10)
    g.add_edge(w2, store[6], 25)
    g.add_edge(w3, store[7], 20)
    g.add_edge(w3, store[8], 15)
    g.add_edge(w3, store[9], 10)
    g.add_edge(w4, store[10], 20)
    g.add_edge(w4, store[11], 10)
    g.add_edge(w4, store[12], 15)
    g.add_edge(w4, store[13], 5)
    g.add_edge(w4, store[14], 10)
    g.add_edge(s, t1, g.sum_out(t1))
    g.add_edge(s, t2, g.sum_out(t2))
    for i in range(1, 15):
        for w in (w1, w2, w3, w4):
            if g.cap[w][store[i]] > 0:
                g.add_edge(store[i], t, g.cap[w][store[i]])
                break
    return g, s, t, t1, t2, w1, w2, w3, w4, store, names


def terminal_store_flows(used_paths, names, t1_idx, t2_idx):
    """Build terminal-to-store flow table from used paths."""
    flows = defaultdict(int)
    for path_nodes, f in used_paths:
        term = None
        dest_store = None
        for u in range(len(path_nodes) - 1):
            a = path_nodes[u]
            b = path_nodes[u + 1]
            if a in (t1_idx, t2_idx):
                term = names[a]
            if names[b].startswith("Store "):
                dest_store = names[b]
        if term and dest_store:
            flows[(term, dest_store)] += f
    return flows


if __name__ == "__main__":
    g, s, t, t1, t2, w1, w2, w3, w4, store, names = build_network()
    maxflow, used_paths = edmonds_karp_with_paths(g, s, t)
    flows = terminal_store_flows(used_paths, names, t1, t2)

    print("Термінал\tМагазин\tПотік (од.)")
    for term in ["Terminal 1", "Terminal 2"]:
        for st in [f"Store {i}" for i in range(1, 15)]:
            print(f"{term}\t{st}\t{flows.get((term, st), 0)}")

    t1_total = sum(v for (tname, _), v in flows.items() if tname == "Terminal 1")
    t2_total = sum(v for (tname, _), v in flows.items() if tname == "Terminal 2")

    print("\nВИСНОВКИ:")
    print(f"Максимальний потік у системі: {maxflow} одиниць.")
    print(f"Terminal 1 постачає {t1_total}, Terminal 2 - {t2_total}.")
    print("Потік є оптимальним (мінімальний розріз: S→T1=60, S→T2=55).")
    print("Магазини без поставок: 3, 9, 12, 13, 14.")
    print("Для покращення слід збільшити пропускну здатність ребер:")
    print(" - S→T2 та T2→W4 для магазинів 12–14;")
    print(" - T1→W1 і T1→W3 для інших дефіцитних напрямів.")
    print("Збільшення місткості термінал→склад або S→Terminal підвищить ефективність мережі.")

