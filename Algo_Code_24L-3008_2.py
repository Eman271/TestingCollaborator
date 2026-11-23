

import random
big = 10 ** 9
random.seed(3008)

def nm(x):
    return 'nil' if x is None else str(x)

def fm(x):
    return 'inf' if x >= big else str(x)

def undir(n, es):
    adj = [[] for i in range(n)]
    for u, v in es:
        adj[u].append(v)
        adj[v].append(u)
    return [sorted(a) for a in adj]

def direct(n, es):
    adj = [[] for i in range(n)]
    for u, v in es:
        adj[u].append(v)
    return [sorted(a) for a in adj]

def transpose(adj):
    t = [[] for i in adj]
    for u in range(len(adj)):
        for v in adj[u]:
            t[v].append(u)
    return [sorted(a) for a in t]

def reach(adj, s):
    seen = {s}
    st = [s]
    while st:
        u = st.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                st.append(v)
    return seen

def sccref(adj):
    r = [reach(adj, u) for u in range(len(adj))]
    return {frozenset((v for v in r[u] if u in r[v])) for u in range(len(adj))}

def gconn(n, m):
    order = list(range(n))
    random.shuffle(order)
    es = set()
    for i in range(1, n):
        u = order[i]
        v = order[random.randrange(i)]
        es.add((min(u, v), max(u, v)))
    while len(es) < m:
        u, v = random.sample(range(n), 2)
        es.add((min(u, v), max(u, v)))
    return sorted(es)

def gweight(es):
    ws = random.sample(range(1, 100), len(es))
    return [(w, u, v) for (u, v), w in zip(es, ws)]

def gdir():
    while True:
        n = random.randint(12, 15)
        m = random.randint(21, 28)
        es = set()
        while len(es) < m:
            u, v = random.sample(range(n), 2)
            es.add((u, v))
        adj = direct(n, sorted(es))
        cs = sccref(adj)
        if len(cs) >= 3 and max((len(c) for c in cs)) >= 2:
            return (n, sorted(es), adj)

def gdag(n, m):
    order = list(range(n))
    random.shuffle(order)
    es = set()
    while len(es) < m:
        i, j = sorted(random.sample(range(n), 2))
        es.add((order[i], order[j]))
    return sorted(es)

def showadj(title, adj):
    print(title)
    for u in range(len(adj)):
        print(' ', u, '->', adj[u])

def showw(title, wadj):
    print(title)
    for u in range(len(wadj)):
        print(' ', u, '->', [str(v) + '(' + str(w) + ')' for v, w in wadj[u]])

def dfs(adj, roots, show):
    n = len(adj)
    col = ['white'] * n
    d = [0] * n
    f = [0] * n
    pi = [None] * n
    cls = []
    order = []
    tops = []
    t = 0

    def visit(u, k):
        nonlocal t
        t += 1
        d[u] = t
        col[u] = 'gray'
        if show:
            print('time', t, 'discover', u, 'parent', nm(pi[u]), 'depth', k)
        for v in adj[u]:
            if col[v] == 'white':
                c = 'tree'
                pi[v] = u
            elif col[v] == 'gray':
                c = 'back'
            elif d[u] < d[v]:
                c = 'forward'
            else:
                c = 'cross'
            cls.append((u, v, c))
            if show:
                print(' edge', u, '->', v, c)
            if c == 'tree':
                visit(v, k + 1)
        col[u] = 'black'
        t += 1
        f[u] = t
        order.append(u)
        if show:
            print('time', t, 'finish', u, 'parent', nm(pi[u]), 'depth', k)
    for r in roots:
        if col[r] == 'white':
            tops.append(r)
            visit(r, 0)
    return (d, f, pi, cls, order, tops)

def bfs(adj):
    n = len(adj)
    col = ['white'] * n
    d = [None] * n
    pi = [None] * n
    col[0] = 'gray'
    d[0] = 0
    q = [0]
    while q:
        u = q.pop(0)
        for v in adj[u]:
            if col[v] == 'white':
                col[v] = 'gray'
                d[v] = d[u] + 1
                pi[v] = u
                q.append(v)
        col[u] = 'black'
        print('dequeued', u, 'queue:', q)
        for v in range(n):
            print(' ', v, col[v], 'd =', nm(d[v]), 'pi =', nm(pi[v]))
    return (d, pi)

def find(p, x):
    if p[x] != x:
        p[x] = find(p, p[x])
    return p[x]

def prim(n, wadj):
    wt = {}
    for u in range(n):
        for v, w in wadj[u]:
            wt[u, v] = w
    key = [big] * n
    pi = [None] * n
    key[0] = 0
    q = list(range(n))
    while q:
        u = min(q, key=lambda x: (key[x], x))
        q.remove(u)
        print('extract', u, 'key', fm(key[u]))
        for v, w in wadj[u]:
            if v in q and w < key[v]:
                key[v] = w
                pi[v] = u
        for v in range(n):
            print(' ', v, 'key =', fm(key[v]), 'pi =', nm(pi[v]))
        print(' queue:', ' '.join((str(v) + '(' + fm(key[v]) + ')' for v in sorted(q, key=lambda x: (key[x], x)))))
    tree = [(pi[v], v) for v in range(n) if pi[v] is not None]
    return (tree, sum((wt[e] for e in tree)))

def kruskal(n, wes):
    p = list(range(n))
    rk = [0] * n
    tree = []
    total = 0
    es = sorted(wes)
    print('sorted edges:', [(u, v, w) for w, u, v in es])
    for w, u, v in es:
        ru = find(p, u)
        rv = find(p, v)
        a = ru
        b = rv
        if ru != rv:
            if rk[ru] < rk[rv]:
                ru, rv = (rv, ru)
            p[rv] = ru
            if rk[ru] == rk[rv]:
                rk[ru] += 1
            tree.append((u, v))
            total += w
            dec = 'accept'
        else:
            dec = 'reject'
        print('edge', (u, v), 'w =', w, 'roots', a, b, dec)
        print(' parent:', p)
        print(' rank: ', rk)
    return (tree, total)

def main():
    n = random.randint(12, 15)
    m = random.randint(21, 28)
    es = gconn(n, m)
    adj = undir(n, es)
    wes = gweight(es)
    wadj = [[] for i in range(n)]
    for w, u, v in wes:
        wadj[u].append((v, w))
        wadj[v].append((u, w))
    wadj = [sorted(a) for a in wadj]
    print('\nconnected undirected graph: vertices', n, 'edges', len(es))
    showadj('adjacency lists', adj)
    showw('weighted adjacency lists', wadj)
    dn, des, dadj = gdir()
    print('\ndirected graph: vertices', dn, 'edges', len(des))
    showadj('adjacency lists', dadj)
    gn = random.randint(12, 15)
    ges = gdag(gn, random.randint(21, 28))
    gadj = direct(gn, ges)
    print('\ndag: vertices', gn, 'edges', len(ges))
    showadj('adjacency lists', gadj)
    print('\n=== bfs ===')
    d, pi = bfs(adj)
    print('bfs tree edges:', [(pi[v], v) for v in range(n) if pi[v] is not None])
    print('distances:', {v: d[v] for v in range(n)})
    print('\n=== dfs ===')
    d, f, pi, cls, order, tops = dfs(dadj, range(dn), True)
    print('vertex d f')
    for v in range(dn):
        print(v, d[v], f[v])
    for c in ('tree', 'back', 'forward', 'cross'):
        print(c, 'edges:', sum((1 for e in cls if e[2] == c)))
    print('\n=== strongly connected components ===')
    print('first dfs finishing times:')
    d1, f1, p1, c1, o1, t1 = dfs(dadj, range(dn), True)
    print('vertex f:', {v: f1[v] for v in range(dn)})
    tadj = transpose(dadj)
    showadj('transpose adjacency lists', tadj)
    rootorder = sorted(range(dn), key=lambda v: -f1[v])
    print('second dfs root order (decreasing finish):', rootorder)
    print('second dfs:')
    d2, f2, p2, c2, o2, t2 = dfs(tadj, rootorder, True)
    print('roots actually used:', t2)
    comp = {}
    for v in range(dn):
        r = v
        while p2[r] is not None:
            r = p2[r]
        comp.setdefault(r, set()).add(v)
    for r in t2:
        print('component:', sorted(comp[r]))
    cid = {}
    for r in comp:
        for v in comp[r]:
            cid[v] = r
    reachs = [reach(dadj, u) for u in range(dn)]
    good = all(((cid[u] == cid[v]) == (v in reachs[u] and u in reachs[v]) for u in range(dn) for v in range(dn)))
    print('scc check:', 'passed' if good else 'failed')
    print('\n=== topological sort ===')
    d, f, pi, cls, order, tops = dfs(gadj, range(gn), True)
    lst = []
    for v in order:
        lst.insert(0, v)
        print('finished', v, 'list:', lst)
    print('topological order:', lst)
    pos = {v: i for i, v in enumerate(lst)}
    print('order check:', 'passed' if all((pos[u] < pos[v] for u, v in ges)) else 'failed')
    print('\n=== prim ===')
    ptree, ptotal = prim(n, wadj)
    print('tree edges:', ptree)
    print('total weight:', ptotal)
    print('\n=== kruskal ===')
    ktree, ktotal = kruskal(n, wes)
    print('tree edges:', ktree)
    print('total weight:', ktotal)
    print('prim and kruskal totals equal:', ptotal == ktotal)
main()
