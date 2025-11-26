import numpy as np
import matplotlib.pyplot as plt

def acceleration(r, mu):
    r_norm = np.linalg.norm(r)
    a = -mu * r / r_norm**3

    return a

def step(state, dt, mu):
    r = np.array(state[:3])
    v = np.array(state[3:])
    a = acceleration(r, mu)

    r_new = r + v * dt
    v_new = v + a * dt

    state_new = np.concatenate([r_new, v_new])
    
    return state_new

def main():
    MU = 3.986004418e14
    R_EARTH = 6378137.
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
        state_new = step(state, dt, MU)
        state = state_new

    plt.plot(xs, ys)
    plt.axis('equal')
    plt.show()
    pass

if __name__ == "__main__":
    main()