#!/usr/bin/env python3
# Deterministic regeneration of all nine measured benchmark edge lists.
# Python 3; standard library only. Does not import historical algorithm code.
import itertools
import random
from pathlib import Path

P = Path(__file__).resolve().parent / "graphs"
P.mkdir(exist_ok=True)

def save(name, n, m, edges):
    edges = sorted(edges)
    assert len(edges) == len(set(edges))
    with (P / (name + ".edges")).open("w") as f:
        f.write(f"{n} {m} {len(edges)}\n")
        f.writelines(f"{u} {w}\n" for u, w in edges)

def lift(n, m, edges, s, kind, seed):
    rng = random.Random(seed)
    out = []
    for j, (u, w) in enumerate(edges):
        perm = list(range(s))
        if kind == "random":
            rng.shuffle(perm)
        elif j == 0:
            perm = [(i + 1) % s for i in range(s)]
        out.extend((u * s + i, w * s + perm[i]) for i in range(s))
    return n * s, m * s, out

for base, q, dv, dc in [("A", 7, 3, 6), ("B", 5, 3, 4), ("C", 11, 4, 8)]:
    n, m = dc * q, dv * q
    edges = [(x*q+y, a*q+(y-a*x)%q)
             for x in range(dc) for y in range(q) for a in range(dv)]
    for s in ([16, 128] if base == "A" else [128]):
        for kind in (["cyclic", "random"] if s == 128 and base in ("A", "C") else ["cyclic"]):
            nn, mm, ee = lift(n, m, edges, s, kind, 20261008+s+q*100)
            save(f"{base}{s}{kind[0]}", nn, mm, ee)

# Symplectic generalized quadrangle W(5), point splitting to degree three.
q = 5
norm = lambda x: tuple((a * pow(next(t for t in x if t), -1, q)) % q for a in x)
points = sorted(set(norm(x) for x in itertools.product(range(q), repeat=4) if any(x)))
idx = {x:i for i,x in enumerate(points)}
lines = set()
for i,x in enumerate(points):
    for y in points[i+1:]:
        if (x[0]*y[2]+x[1]*y[3]-x[2]*y[0]-x[3]*y[1]) % q:
            continue
        line = tuple(sorted({idx[norm(tuple((a*x[j]+b*y[j])%q for j in range(4)))]
                             for a,b in itertools.product(range(q),repeat=2) if a or b}))
        assert len(line)==6
        lines.add(line)
lines = sorted(lines)
inc = [[] for _ in points]
for j,line in enumerate(lines):
    for i in line:
        inc[i].append(j)
edges = []
for i,ls in enumerate(inc):
    assert len(ls)==6
    for k,j in enumerate(ls):
        edges.append((2*i+k//3,j))
n,m = 2*len(points),len(lines)
nn,mm,ee = lift(n,m,edges,16,"cyclic",20261008+16+500)
save("D16c",nn,mm,ee)

# The two modified QC matrices from the research benchmark definition.
E = [[0]*6,[0,3,14,18,24,26],[0,19,62,107,170,224]]
for name,L,g,z,s,r,j in [("Q410",4,10,79,128,2,0),("Q412",4,12,142,64,0,3)]:
    Z=z*s
    ex=[a[:L] for a in E]
    ex[r][j]+=z
    save(name,L*Z,3*Z,[(col*Z+i,row*Z+(i+ex[row][col])%Z)
                        for col in range(L) for i in range(Z) for row in range(3)])
# Additional cycle-rich lift benchmarks, generated using exactly the
# same incidence bases, seed convention and cyclic lift definition.
for base, q, dv, dc, sizes in [
    ("A", 7, 3, 6, [256]),
    ("C", 11, 4, 8, [256, 512]),
]:
    bn, bm = dc*q, dv*q
    be = [(x*q+y, a*q+(y-a*x)%q)
          for x in range(dc) for y in range(q) for a in range(dv)]
    for size in sizes:
        nn, mm, lifted = lift(bn, bm, be, size, "cyclic",
                              20261008+size+q*100)
        save(f"{base}{size}c", nn, mm, lifted)

# The same split symplectic W(5) incidence base as D16c above
nn, mm, lifted = lift(n, m, edges, 32, "cyclic", 20261008+32+500)
save("D32c", nn, mm, lifted)

print("Regenerated original nine and four cycle-rich benchmark graphs.")

