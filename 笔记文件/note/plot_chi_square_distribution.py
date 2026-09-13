import math

import matplotlib.pyplot as plt
import numpy as np


def chi_square_density(x, k):
    log_density = (
        (k / 2 - 1) * np.log(x)
        - x / 2
        - (k / 2) * math.log(2)
        - math.lgamma(k / 2)
    )
    return np.exp(log_density)


x = np.linspace(0.002, 30, 3000)
degrees = [1, 2, 3, 5, 10, 20]

plt.figure(figsize=(10, 6.2), dpi=180)
for k in degrees:
    plt.plot(x, chi_square_density(x, k), linewidth=2, label=rf"$k={k}$")

plt.title(r"Chi-square distribution density", fontsize=15)
plt.xlabel(r"$x$", fontsize=12)
plt.ylabel(r"$f(x)$", fontsize=12)
plt.xlim(0, 30)
plt.ylim(0, 0.55)
plt.grid(True, alpha=0.25)
plt.legend(title="Degrees of freedom", frameon=True)
plt.tight_layout()
plt.savefig("卡方分布概率密度函数.png", bbox_inches="tight")
