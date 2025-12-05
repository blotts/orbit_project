import numpy as np
from scipy.integrate import solve_ivp
from constants import MU

def acceleration(r, MU):
    r_norm = np.linalg.norm(r)
    a = -MU * r / r_norm**3
    return a

def state_eq(t, q):
    r = q[:3]
    v = q[3:]
    a = acceleration(r, MU)
    return np.concatenate([v, a])

def propagate(state0, t_span, dt):

    cols = int((t_span[1] - t_span[0]) / dt + 1)
    states = np.zeros([6, cols])
    states[:, 0] = state0

    t_current = t_span[0]
    t_next = t_current + dt

    t = np.zeros(cols)
    t[0] = t_current

    for i in range(1, cols):

        sol = solve_ivp(
            state_eq, 
            [t_current, t_next], 
            states[:, i - 1], 
            method = 'DOP853', 
            t_eval = [t_next])

        t[i] = t_next
        t_current = t_next
        t_next = t_current + dt

        states[:, i] = sol.y[:, -1]

    return states, t