import numpy as np
from constants import MU

def acceleration(r, mu=MU):
    r_norm = np.linalg.norm(r)
    a = -mu * r / r_norm**3

    return a

def step(state, dt, mu=MU):
    r = np.array(state[:3])
    v = np.array(state[3:])
    a = acceleration(r, mu)

    r_new = r + v * dt
    v_new = v + a * dt

    state_new = np.concatenate([r_new, v_new])
    
    return state_new