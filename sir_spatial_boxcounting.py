# ============================================================
# SIR Espacial com Autômato Celular + Box-Counting
# ============================================================
# Autor: Marcelo Antonio de Menezes Júnior
# Artigo: Análise da Transição Crítica da Propagação do Sarampo
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from scipy.stats import linregress
from scipy.signal import convolve2d

# ============================================================
# ESTADOS
# ============================================================

SUSCEPTIBLE = 0
INFECTED = 1
RECOVERED = 2

# ============================================================
# PARÂMETROS
# ============================================================

L = 200
GAMMA = 0.2
MAX_STEPS = 500
N_RUNS = 30

# ============================================================
# INICIALIZAÇÃO
# ============================================================

def initialize_grid():
    grid = np.zeros((L, L), dtype=np.int8)
    c = L // 2
    grid[c, c] = INFECTED
    return grid

# ============================================================
# KERNEL DE MOORE
# ============================================================

KERNEL = np.array([
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1]
])

# ============================================================
# ATUALIZAÇÃO
# ============================================================

def update(grid, beta):
    infected = (grid == INFECTED)

    # Conta vizinhos infectados
    infected_neighbors = convolve2d(
        infected.astype(int),
        KERNEL,
        mode='same',
        boundary='fill'
    )

    # Probabilidades
    rand_inf = np.random.rand(L, L)
    rand_rec = np.random.rand(L, L)

    new_grid = grid.copy()

    # Infecção
    new_grid[
        (grid == SUSCEPTIBLE) &
        (infected_neighbors > 0) &
        (rand_inf < beta)
    ] = INFECTED

    # Recuperação
    new_grid[
        (grid == INFECTED) &
        (rand_rec < GAMMA)
    ] = RECOVERED

    return new_grid

# ============================================================
# SIMULAÇÃO
# ============================================================

def run_simulation(beta):
    grid = initialize_grid()

    S, I, R = [], [], []
    peak_grid = None
    max_I = 0

    for _ in range(MAX_STEPS):
        s = np.sum(grid == SUSCEPTIBLE)
        i = np.sum(grid == INFECTED)
        r = np.sum(grid == RECOVERED)

        S.append(s)
        I.append(i)
        R.append(r)

        if i > max_I:
            max_I = i
            peak_grid = grid.copy()

        if i == 0:
            break

        grid = update(grid, beta)

    return np.array(S), np.array(I), np.array(R), peak_grid

# ============================================================
# BOX-COUNTING
# ============================================================

def box_counting(binary_grid):
    epsilons = []
    sizes = []

    n = 1
    while n <= L // 2:
        epsilons.append(n)
        n *= 2

    for eps in epsilons:
        count = 0
        for i in range(0, L, eps):
            for j in range(0, L, eps):
                if np.any(binary_grid[i:i+eps, j:j+eps]):
                    count += 1
        sizes.append(count)

    log_eps = np.log(1 / np.array(epsilons))
    log_N = np.log(np.array(sizes))

    slope, _, _, _, _ = linregress(log_eps, log_N)
    return slope

# ============================================================
# VARIAÇÃO DE BETA
# ============================================================

def run_beta_experiment(beta_values):
    mean_D = []
    std_D = []

    for beta in beta_values:
        D_vals = []

        for _ in range(N_RUNS):
            S, I, R, peak_grid = run_simulation(beta)

            if peak_grid is None or np.max(I) < 5:
                continue

            binary_peak = (peak_grid == INFECTED).astype(int)
            D_vals.append(box_counting(binary_peak))

        mean_D.append(np.mean(D_vals))
        std_D.append(np.std(D_vals))

        print(f"β = {beta:.2f} | D = {mean_D[-1]:.3f}")

    return np.array(mean_D), np.array(std_D)

# ============================================================
# VISUALIZAÇÃO
# ============================================================

def plot_grid(grid, title=""):
    cmap = colors.ListedColormap(["white", "red", "green"])
    bounds = [0, 1, 2, 3]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    plt.figure(figsize=(6, 6))
    plt.imshow(grid, cmap=cmap, norm=norm)
    plt.title(title)
    plt.axis("off")

    legend_elements = [
        plt.matplotlib.patches.Patch(facecolor='white', edgecolor='black', label='Suscetível'),
        plt.matplotlib.patches.Patch(facecolor='red', edgecolor='black', label='Infectado'),
        plt.matplotlib.patches.Patch(facecolor='green', edgecolor='black', label='Recuperado')
    ]

    plt.legend(handles=legend_elements, loc='upper right')
    plt.show()

def plot_time_series(S, I, R):
    plt.figure(figsize=(10, 5))
    plt.plot(S, label="Suscetíveis")
    plt.plot(I, label="Infectados")
    plt.plot(R, label="Recuperados")
    plt.xlabel("Tempo")
    plt.ylabel("População")
    plt.legend()
    plt.grid()
    plt.show()

def plot_fractal_dimension(beta_values, mean_D, std_D):
    plt.figure(figsize=(10, 5))
    plt.errorbar(beta_values, mean_D, yerr=std_D, fmt='o-', capsize=3)
    plt.xlabel(r'$\beta$')
    plt.ylabel('Dimensão Fractal D')
    plt.title('Dimensão Fractal vs Taxa de Transmissão')
    plt.grid()
    plt.show()

if __name__ == "__main__":
    beta = 0.25
    S, I, R, peak = run_simulation(beta)

    plot_time_series(S, I, R)
    plot_grid(peak, "Pico da Infecção")

    beta_values = np.arange(0.05, 0.51, 0.01)
    mean_D, std_D = run_beta_experiment(beta_values)
    plot_fractal_dimension(beta_values, mean_D, std_D)