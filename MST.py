import random, math, itertools
import matplotlib.pyplot as plt
import statistics

def tour_length(tour, pts):
    return sum(math.dist(pts[tour[i]], pts[tour[(i + 1) % len(tour)]])
               for i in range(len(tour)))

def optimal_tour(pts):
    n = len(pts)
    best, best_len = None, float("inf")
    for perm in itertools.permutations(range(1, n)):
        tour = (0,) + perm
        L = tour_length(tour, pts)
        if L < best_len:
            best, best_len = tour, L
    return list(best), best_len

def mst_prim(pts):
    n = len(pts)
    best = {v: (math.dist(pts[0], pts[v]), 0) for v in range(1, n)}
    children = {v: [] for v in range(n)}
    while best:
        v = min(best, key=lambda u: best[u][0])
        children[best.pop(v)[1]].append(v)
        for u in best:
            d = math.dist(pts[v], pts[u])
            if d < best[u][0]:
                best[u] = (d, v)
    return children

def preorder(children, root=0):
    return [root] + [c for child in children[root] for c in preorder(children, child)]

def two_opt(route, D):
    best = route[:]; n = len(best)
    improved = True
    while improved:
        improved = False
        for i in range(n - 1):
            for j in range(i + 2, n):
                if i == 0 and j == n - 1: continue
                a, b = best[i], best[(i + 1) % n]
                c, d = best[j], best[(j + 1) % n]
                if D[a][c] + D[b][d] < D[a][b] + D[c][d] - 1e-12:
                    best[i + 1:j + 1] = best[i + 1:j + 1][::-1]
                    improved = True
    return best

def simulated_annealing(route, D, T0=50.0, iters=8000):
    current = route[:]; cur = tour_length(current, D)
    best, best_c = current[:], cur
    n = len(current)
    for t in range(iters):
        T = T0 * math.exp(-5 * t / iters)
        if T < 1e-6: break
        i = random.randint(0, n - 2); j = random.randint(i + 1, n - 1)
        nb = current[:i] + current[i:j + 1][::-1] + current[j + 1:]
        c = tour_length(nb, D)
        if c < cur or random.random() < math.exp(-(c - cur) / T):
            current, cur = nb, c
            if c < best_c: best, best_c = nb[:], c
    return best, best_c

def dist_matrix(pts):
    n = len(pts)
    return [[math.dist(pts[i], pts[j]) for j in range(n)] for i in range(n)]

if __name__ == "__main__":
    random.seed(2024)
    N_CITIES, N_INSTANCES = 9, 100
    ratios, records = [], []
    mst_costs, mst2opt_costs, ls_costs, sa_costs, opt_costs = [], [], [], [], []

    for _ in range(N_INSTANCES):
        pts = [(random.uniform(0, 10), random.uniform(0, 10)) for _ in range(N_CITIES)]
        D = dist_matrix(pts)

        _, opt_cost = optimal_tour(pts)
        mst_tour = preorder(mst_prim(pts))
        c_mst = tour_length(mst_tour, pts)
        c_mst2 = tour_length(two_opt(mst_tour, D), pts)

        rand_init = list(range(N_CITIES)); random.shuffle(rand_init)
        c_ls = tour_length(two_opt(rand_init, D), pts)

        rand_init2 = list(range(N_CITIES)); random.shuffle(rand_init2)
        _, c_sa = simulated_annealing(rand_init2, D)

        ratios.append(c_mst / opt_cost)
        mst_costs.append(c_mst); mst2opt_costs.append(c_mst2)
        ls_costs.append(c_ls);  sa_costs.append(c_sa); opt_costs.append(opt_cost)

    print("=== Razón de aproximación MST ===")
    print(f"media={statistics.mean(ratios):.3f}  max={max(ratios):.3f}  "
          f"cota teórica=2.0")
    print(f"Coste medio  MST puro    = {statistics.mean(mst_costs):.2f}")
    print(f"Coste medio  MST + 2-opt = {statistics.mean(mst2opt_costs):.2f}")
    print(f"Coste medio  2-opt rand  = {statistics.mean(ls_costs):.2f}")
    print(f"Coste medio  SA          = {statistics.mean(sa_costs):.2f}")
    print(f"Coste medio  Óptimo      = {statistics.mean(opt_costs):.2f}")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    ax1.hist(ratios, bins=20, color="steelblue", edgecolor="k", alpha=0.8)
    ax1.axvline(2.0, color="red", ls="--", lw=2, label="Cota teórica = 2")
    ax1.axvline(statistics.mean(ratios), color="green", ls="-", lw=2,
                label=f"Media = {statistics.mean(ratios):.2f}")
    ax1.set_xlabel("C_obtenido / C_óptimo"); ax1.set_ylabel("Frecuencia")
    ax1.set_title("Razón de aproximación MST (100 instancias)")
    ax1.legend(); ax1.grid(alpha=0.3)

    ax2.boxplot([mst_costs, mst2opt_costs, ls_costs, sa_costs, opt_costs],
                labels=["MST", "MST+2opt", "2-opt (rand)", "SA", "Óptimo"])
    ax2.set_ylabel("Costo del tour"); ax2.set_title("Comparación de métodos (n=9)")
    ax2.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.savefig("ej5_mst_ratio.png", dpi=120)
    plt.show()