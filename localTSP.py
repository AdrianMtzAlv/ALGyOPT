import random, math, statistics
import matplotlib.pyplot as plt

def tour_length(route, D):
    return sum(D[route[i]][route[(i + 1) % len(route)]] for i in range(len(route)))

def two_opt(route, D):
    """2-opt por delta; devuelve (mejor_ruta, num_mejoras)."""
    best = route[:]
    n = len(best)
    improvements = 0
    improved = True
    while improved:
        improved = False
        for i in range(n - 1):
            for j in range(i + 2, n):
                if i == 0 and j == n - 1:
                    continue
                a, b = best[i], best[(i + 1) % n]
                c, d = best[j], best[(j + 1) % n]
                if D[a][c] + D[b][d] < D[a][b] + D[c][d] - 1e-12:
                    best[i + 1:j + 1] = best[i + 1:j + 1][::-1]
                    improvements += 1
                    improved = True
    return best, improvements

def nearest_neighbor(start, D):
    n = len(D)
    unvisited = set(range(n)); unvisited.remove(start)
    route = [start]
    while unvisited:
        last = route[-1]
        nxt = min(unvisited, key=lambda j: D[last][j])
        route.append(nxt); unvisited.remove(nxt)
    return route

def random_instance(n):
    pts = [(random.uniform(0, 10), random.uniform(0, 10)) for _ in range(n)]
    D = [[math.dist(p, q) for q in pts] for p in pts]
    return D

if __name__ == "__main__":
    random.seed(42)
    N_CITIES = 20
    TRIALS   = 30

    rand_improvements, nn_improvements = [], []
    rand_final,       nn_final        = [], []

    for _ in range(TRIALS):
        D = random_instance(N_CITIES)

     
        r0 = list(range(N_CITIES)); random.shuffle(r0)
        r_opt, imp = two_opt(r0, D)
        rand_improvements.append(imp)
        rand_final.append(tour_length(r_opt, D))

   
        start = random.randrange(N_CITIES)
        nn0 = nearest_neighbor(start, D)
        r_opt2, imp2 = two_opt(nn0, D)
        nn_improvements.append(imp2)
        nn_final.append(tour_length(r_opt2, D))

    print("=== Estadísticas ===")
    print(f"Random init  – mejoras: media={statistics.mean(rand_improvements):.1f}, "
          f"coste medio={statistics.mean(rand_final):.2f}")
    print(f"NearestNeigh – mejoras: media={statistics.mean(nn_improvements):.1f}, "
          f"coste medio={statistics.mean(nn_final):.2f}")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    ax1.boxplot([rand_improvements, nn_improvements],
                labels=["Random init", "Nearest-Neighbor init"])
    ax1.set_ylabel("Nº de mejoras 2-opt"); ax1.set_title("Mejoras hasta óptimo local")
    ax1.grid(axis="y", alpha=0.3)

    ax2.boxplot([rand_final, nn_final],
                labels=["Random init", "Nearest-Neighbor init"])
    ax2.set_ylabel("Longitud final del tour"); ax2.set_title("Calidad del óptimo local")
    ax2.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.savefig("ej3_two_opt.png", dpi=120)
    plt.show()