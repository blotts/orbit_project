import numpy as np
import matplotlib.pyplot as plt
from dynamics import acceleration, step
from constants import MU, R_EARTH

def main():
    alt = 400.0e3

    r0 = np.array([R_EARTH + alt, 0, 0])
    v_circ = np.sqrt(MU / np.linalg.norm(r0))
    v0 = np.array([0, v_circ, 0])
    state0 = np.concatenate([r0, v0])

    T = 2*np.pi*np.sqrt(np.linalg.norm(r0)**3 / MU)
    t = np.linspace(0, T, 1000)
    dt = t[1] - t[0]

    xs = np.zeros(len(t))
    ys = np.zeros(len(t))

    state = state0
    for i in range(t.size):
        xs[i], ys[i] = state[:2]
        state_new = step(state, dt)
        state = state_new

    plt.plot(xs, ys)
    plt.axis('equal')
    plt.show()
    pass

if __name__ == "__main__":
    main()