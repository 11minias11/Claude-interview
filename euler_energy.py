"""Part 1: two-body orbit (GM = 1, sun fixed at origin) with explicit Euler."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---- Parameters -------------------------------------------------------------
h = 0.01                      # time step
n_orbits = 10                 # how many orbits to integrate
r0 = np.array([1.0, 0.0])     # initial position (x, y)
v0 = np.array([0.0, 1.0])     # initial velocity (vx, vy); try (0, 1.2) for an ellipse


def accel(r):
    """a(r) = -r / |r|^3"""
    return -r / np.linalg.norm(r) ** 3


def energy(r, v):
    """E = 1/2 (vx^2 + vy^2) - 1 / sqrt(x^2 + y^2)"""
    return 0.5 * (v[0] ** 2 + v[1] ** 2) - 1.0 / np.sqrt(r[0] ** 2 + r[1] ** 2)


def period(r, v):
    """Orbital period from Kepler's third law (GM = 1): a = -1/(2E), T = 2*pi*a^(3/2).
    Only used to express time in orbits; gives 2*pi for the circular orbit."""
    a = -1.0 / (2.0 * energy(r, v))
    return 2.0 * np.pi * a ** 1.5


if __name__ == "__main__":
    T = period(r0, v0)
    n_steps = int(round(n_orbits * T / h))

    r = r0.copy()
    v = v0.copy()
    traj = np.empty((n_steps + 1, 2))
    E = np.empty(n_steps + 1)
    traj[0] = r
    E[0] = energy(r, v)

    for n in range(n_steps):
        # Euler: both updates use the values at step n
        r, v = r + h * v, v + h * accel(r)   # r_{n+1} = r_n + h v_n ;  v_{n+1} = v_n + h a(r_n)
        traj[n + 1] = r
        E[n + 1] = energy(r, v)

    t_orbits = np.arange(n_steps + 1) * h / T

    print(f"E start = {E[0]:.10f}")
    print(f"E end   = {E[-1]:.10f}")
    print(f"drift   = {E[-1] - E[0]:.10f}")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.plot(traj[:, 0], traj[:, 1], lw=0.8)
    ax1.plot(0, 0, "o", color="orange", ms=10, label="sun")
    ax1.set_aspect("equal")
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax1.set_title(f"Euler orbit, h = {h}, {n_orbits} orbits")
    ax1.legend()

    ax2.plot(t_orbits, E, lw=1, label="Euler")
    ax2.axhline(E[0], ls="--", color="k", label="true E")
    ax2.set_xlabel("time (orbits)")
    ax2.set_ylabel("E")
    ax2.set_title("Energy")
    ax2.legend()

    fig.tight_layout()
    fig.savefig("euler_energy.png", dpi=150)
