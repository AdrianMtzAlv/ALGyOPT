import random, math, time
import matplotlib.pyplot as plt

def tour_length(route, D):
    return sum(D[route[i]][route[(i + 1) % len(route)]] for i in range(len(route)))

def random_instance(n):
    pts = [(random.uniform(0, 10), random.uniform(0, 10)) for _ in range(n)]
    D = [[math.dist(p, q) for q in pts] for p in pts]
    return D

def simulated_annealing(route, D, schedule, T0, iters=20000):
    current = route[:]
    current_cost = tour_length(current, D)
    best, best_cost = current[:], current_cost
    history = []
    n = len(current)
    for t in range(iters):
        T = schedule(T0, t, iters)
        if T <= 1e-9:
            break

        i = random.randint(0, n - 2)
        j = random.randint(i + 1, n - 1)
        neighbor = current[:i] + current[i:j + 1][::-1] + current[j + 1:]
        d = tour_length(neighbor, D) - current_cost
        if d < 0 or random.random() < math.exp(-d / T):
            current, current_cost = neighbor, tour_length(neighbor, D)
            if current_cost < best_cost:
                best, best_cost = current[:], current_cost
        history.append(best_cost)
    return best, best_cost, history

schedules = {
    "Lineal":    lambda T0, t, N: T0 * max(0.0, 1 - t / N),
    "Exponencial": lambda T0, t, N: T0 * math.exp(-5 * t / N),
    "Geométrico":  lambda T0, t, N: T0 * (0.01) ** (t / N),
}

if __name__ == "__main__":
    random.seed(123)
    N_CITIES = 20
    ITERS    = 20000
    TRIALS   = 5
    D = random_instance(N_CITIES)
    init = list(range(N_CITIES)); random.shuffle(init)
    init_cost = tour_length(init, D)
    print(f"Coste inicial aleatorio: {init_cost:.2f}")

    results = {}
    for name, sch in schedules.items():
        histories, finals, times = [], [], []
        for _ in range(TRIALS):
            route = init[:]; random.shuffle(route)
            t0 = time.perf_counter()
            _, best, hist = simulated_annealing(route, D, sch, T0=100.0, iters=ITERS)
            elapsed = time.perf_counter() - t0
            histories.append(hist); finals.append(best); times.append(elapsed)
        results[name] = dict(
            history=histories[0],
            cost=sum(finals) / TRIALS,
            time=sum(times) / TRIALS,
        )
        print(f"{name:12s} coste_final={results[name]['cost']:.2f}  "
              f"tiempo={results[name]['time']*1000:.0f} ms")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    for name, r in results.items():
        ax1.plot(r["history"], label=name, lw=1.4)
    ax1.set_xlabel("Iteración"); ax1.set_ylabel("Mejor costo")
    ax1.set_title("Curvas de convergencia"); ax1.legend(); ax1.grid(alpha=0.3)

    for name, r in results.items():
        ax2.scatter(r["time"], r["cost"], s=120, label=name)
        ax2.annotate(name, (r["time"], r["cost"]),
                     textcoords="offset points", xytext=(6, 6), fontsize=9)
    ax2.set_xlabel("Tiempo (s)"); ax2.set_ylabel("Calidad (costo final)")
    ax2.set_title("Tiempo vs. Calidad"); ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig("ej4_sa.png", dpi=120)
    plt.show()