"""Part 2: leapfrog (kick-drift-kick) vs explicit Euler over 100 orbits."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from euler_energy import accel, energy, period

# ---- Parameters -------------------------------------------------------------
h = 0.01
n_orbits = 100
r0 = np.array([1.0, 0.0])
cases = {                                  # initial velocities to run
    "circle (v0 = (0, 1))": np.array([0.0, 1.0]),
    "ellipse (v0 = (0, 1.2))": np.array([0.0, 1.2]),
}


def euler_step(r, v, h):
    """r_{n+1} = r_n + h v_n ;  v_{n+1} = v_n + h a(r_n)"""
    return r + h * v, v + h * accel(r)


def leapfrog_step(r, v, h, a):
    """Kick-drift-kick. `a` is a(r_n), passed in from the previous step.
    Returns r_{n+1}, v_{n+1} and a(r_{n+1}) so the caller can reuse it:
    only ONE new acceleration evaluation per step."""
    v_half = v + 0.5 * h * a              # v_{n+1/2} = v_n + (h/2) a(r_n)        (half kick)
    r_new = r + h * v_half                # r_{n+1}   = r_n + h v_{n+1/2}         (drift)
    a_new = accel(r_new)                  # the only new force evaluation this step
    v_new = v_half + 0.5 * h * a_new      # v_{n+1}   = v_{n+1/2} + (h/2) a(r_{n+1}) (half kick)
    return r_new, v_new, a_new


def run(method, r0, v0, h, n_steps):
    """Integrate n_steps; return trajectory (n_steps+1, 2) and energy (n_steps+1,)."""
    r, v = r0.copy(), v0.copy()
    traj = np.empty((n_steps + 1, 2))
    E = np.empty(n_steps + 1)
    traj[0], E[0] = r, energy(r, v)
    if method == "leapfrog":
        a = accel(r)                      # computed once here; afterwards reused from each step
    for n in range(n_steps):
        if method == "euler":
            r, v = euler_step(r, v, h)
        else:
            r, v, a = leapfrog_step(r, v, h, a)
        traj[n + 1], E[n + 1] = r, energy(r, v)
    return traj, E


if __name__ == "__main__":
    fig, axes = plt.subplots(len(cases), 3, figsize=(16, 5 * len(cases)))

    for row, (name, v0) in zip(axes, cases.items()):
        T = period(r0, v0)
        n_steps = int(round(n_orbits * T / h))
        t_orbits = np.arange(n_steps + 1) * h / T
        E0 = energy(r0, v0)

        for ax, method in zip(row[:2], ["euler", "leapfrog"]):
            traj, E = run(method, r0, v0, h, n_steps)
            rel_err = np.abs(E - E0) / abs(E0)

            ax.plot(traj[:, 0], traj[:, 1], lw=0.5)
            ax.plot(0, 0, "o", color="orange", ms=8)
            ax.set_aspect("equal")
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_title(f"{method}: {name}")

            row[2].semilogy(t_orbits, rel_err, lw=0.8, label=method)

        row[2].set_xlabel("time (orbits)")
        row[2].set_ylabel("|E - E0| / |E0|")
        row[2].set_title(f"relative energy error: {name}, h = {h}")
        row[2].legend()

        # Leapfrog with h = 0.01 and h = 0.005: maximum energy error over n_orbits
        print(name)
        for hh in [0.01, 0.005]:
            _, E = run("leapfrog", r0, v0, hh, int(round(n_orbits * T / hh)))
            print(f"  leapfrog h = {hh:<6}  max |E - E0| = {np.max(np.abs(E - E0)):.3e}")

    fig.tight_layout()
    fig.savefig("compare_leapfrog.png", dpi=150)
