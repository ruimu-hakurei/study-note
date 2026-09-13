import math

import matplotlib.pyplot as plt
import numpy as np


def f_density(x, n1, n2):
    log_coefficient = (
        math.lgamma((n1 + n2) / 2)
        - math.lgamma(n1 / 2)
        - math.lgamma(n2 / 2)
        + (n1 / 2) * math.log(n1 / n2)
    )
    return np.exp(
        log_coefficient
        + (n1 / 2 - 1) * np.log(x)
        - ((n1 + n2) / 2) * np.log1p((n1 / n2) * x)
    )


x = np.linspace(0.002, 5, 2000)
parameters = [(1, 5), (5, 5), (5, 10), (10, 20), (30, 30)]

plt.figure(figsize=(10, 6.2), dpi=180)
for n1, n2 in parameters:
    plt.plot(x, f_density(x, n1, n2), linewidth=2, label=rf"$n_1={n1},\ n_2={n2}$")

plt.title(r"F-distribution density $f(x)$", fontsize=15)
plt.xlabel(r"$x$", fontsize=12)
plt.ylabel(r"$f(x)$", fontsize=12)
plt.xlim(0, 5)
plt.ylim(0, 1.55)
plt.grid(True, alpha=0.25)
plt.legend(frameon=True)
plt.tight_layout()
plt.savefig("F分布概率密度函数.png", bbox_inches="tight")
