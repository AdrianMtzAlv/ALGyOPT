import multiprocessing as mp
import random, time
import matplotlib.pyplot as plt

def estimate_pi(seed, samples=1_000_000):
    rng = random.Random(seed)
    inside = sum(rng.random()**2 + rng.random()**2 <= 1.0 for _ in range(samples))
    return 4 * inside / samples

if __name__ == "__main__":
    seeds = list(range(8))

    with mp.Pool(1) as p:
        p.map(estimate_pi, [0])

    t0 = time.perf_counter()
    seq = [estimate_pi(s) for s in seeds]
    t_seq = time.perf_counter() - t0
    print(f"Sequential wall-clock: {t_seq:.3f}s")

    process_counts = [1, 2, 4, 8]
    times, speedups = [], []
    for n_proc in process_counts:
        t0 = time.perf_counter()
        with mp.Pool(processes=n_proc) as pool:
            pool.map(estimate_pi, seeds)
        t_par = time.perf_counter() - t0
        sp = t_seq / t_par
        times.append(t_par); speedups.append(sp)
        print(f"procs={n_proc}: {t_par:.3f}s  speedup={sp:.2f}x")

    fig, (ax1) = plt.subplots(1, figsize=(12, 5))
    ax1.plot(process_counts, speedups, "o-", lw=2, label="Medido")
    ax1.plot(process_counts, process_counts, "k--", label="Ideal (y = x)")
    ax1.set_xlabel("Número de procesos"); ax1.set_ylabel("Speedup")
    ax1.set_title("Aceleración vs. Nº de procesos")
    ax1.set_xticks(process_counts); ax1.grid(alpha=0.3); ax1.legend()

 
    plt.tight_layout()
    plt.savefig("ej1_speedup.png", dpi=120)
    plt.show()

    print(f"\npi estimado: {sum(seq)/len(seq):.5f}")