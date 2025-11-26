import numpy as np
from scipy.integrate import solve_ivp
from constants import MU

def acceleration(r, MU):
    r_norm = np.linalg.norm(r)
    a = -MU * r / r_norm**3
    return a

def propagate(state, t_current, t_next):

    def state_eq(t, q):
        r = q[:3]
        v = q[3:]
        a = acceleration(r, MU)
        return np.concatenate([v, a])

    sol = solve_ivp(
        state_eq, 
        [t_current, t_next], 
        state, 
        method = 'DOP853', 
        t_eval = [t_next])

    return sol.y[:, -1]