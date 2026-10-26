import matplotlib.pyplot as plt

def greedy_knapsack(values, weights, W, key):
    n = len(values)
    order = sorted(range(n), key=lambda i: key(values[i], weights[i]), reverse=True)
    chosen, used, total = [], 0, 0
    for i in order:
        if used + weights[i] <= W:
            chosen.append(i); used += weights[i]; total += values[i]
    return chosen, used, total


items   = ["A", "B"]
values  = [5, 20]
weights = [5, 10]
W = 10

c_vw, u_vw, val_vw = greedy_knapsack(values, weights, W, key=lambda v, w: v / w)
c_lw, u_lw, val_lw = greedy_knapsack(values, weights, W, key=lambda v, w: -w)  

print("=== Instancia diseñada ===")
for name, chosen, used, total in [
    ("Menor peso primero", c_lw, u_lw, val_lw),
    ("Valor/peso (clásico)", c_vw, u_vw, val_vw),
]:
    objs = [items[i] for i in chosen]
    print(f"{name:22s} -> objetos={objs}  peso={used:>2}/{W}  valor={total}")


items2   = ["A", "B", "C"]
values2  = [60, 100, 120]
weights2 = [10, 20, 30]
W2 = 50
c_vw2, u_vw2, val_vw2 = greedy_knapsack(values2, weights2, W2, key=lambda v, w: v / w)
c_lw2, u_lw2, val_lw2 = greedy_knapsack(values2, weights2, W2, key=lambda v, w: -w)


fig, axes = plt.subplots(1, 2, figsize=(12, 5))

for ax, (title, (cv, uv, vv), (cl, ul, vl)) in zip(
    axes,
    [
        ("Instancia diseñada (W=10)",
         (c_vw, u_vw, val_vw), (c_lw, u_lw, val_lw)),
        ("Instancia clásica (W=50)",
         (c_vw2, u_vw2, val_vw2), (c_lw2, u_lw2, val_lw2)),
    ],
):
    labels = ["Valor/peso", "Menor peso"]
    heights = [vv, vl]
    bars = ax.bar(labels, heights, color=["#2a9d8f", "#e76f51"])
    for b, h in zip(bars, heights):
        ax.text(b.get_x() + b.get_width()/2, h + 1, str(h),
                ha="center", fontweight="bold")
    ax.set_ylabel("Valor total obtenido")
    ax.set_title(title)
    ax.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("ej2_knapsack.png", dpi=120)
plt.show()