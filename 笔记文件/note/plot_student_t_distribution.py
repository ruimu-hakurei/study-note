import math

import matplotlib.pyplot as plt
import numpy as np


def student_t_density(t, n):
    coefficient = math.exp(
        math.lgamma((n + 1) / 2)
        - math.lgamma(n / 2)
        - 0.5 * math.log(n * math.pi)
    )
    return coefficient * (1 + t**2 / n) ** (-(n + 1) / 2)


t = np.linspace(-5, 5, 2500)
degrees = [1, 2, 5, 10, 30]

plt.figure(figsize=(10, 6.2), dpi=180)
for n in degrees:
    plt.plot(t, student_t_density(t, n), linewidth=2, label=rf"$n={n}$")

normal_density = np.exp(-t**2 / 2) / math.sqrt(2 * math.pi)
plt.plot(t, normal_density, color="black", linestyle="--", linewidth=2,
         label=r"$N(0,1)$")

plt.title(r"Student's $t$-distribution density", fontsize=15)
plt.xlabel(r"$t$", fontsize=12)
plt.ylabel(r"$f(t)$", fontsize=12)
plt.xlim(-5, 5)
plt.ylim(0, 0.43)
plt.grid(True, alpha=0.25)
plt.legend(frameon=True)
plt.tight_layout()
plt.savefig("Student-t分布概率密度函数.png", bbox_inches="tight")
