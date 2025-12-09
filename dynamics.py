import numpy as np
from scipy.integrate import solve_ivp
from constants import MU

def acceleration(r):
    '''
    Gravitational acceleration for a point mass in a two-body model.

    r: position vector [km], shape (3,)
    MU: gravitational parameter [km^3/s^2]
    returns: acceleration vector [km/s^2], shape (3,)
    '''
    r_norm = np.linalg.norm(r)
    a = -MU * r / r_norm**3
    return a


def state_eq(t, q):
    '''
    State derivative for [r, v] with central gravity only.

    q: state vector [x, y, z, vx, vy, vz], shape (6,)
    t: time [s], not used (autonomous system)
    returns: time derivative [vx, vy, vz, ax, ay, az]
    '''
    r = q[:3]
    v = q[3:]
    a = acceleration(r)
    return np.concatenate([v, a])

def propagate(state0, t_span, dt):
    '''
    Propagate an initial state forward in time using solve_ivp.

    state0: initial state vector [x, y, z, vx, vy, vz], shape (6,)
    t_span: [t0, tf] in seconds
    dt: output time step in seconds

    returns:
        states: array (6, N) of propagated states
        t: time array (N,)
    '''
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
            t_eval = [t_next]
        )

        # store time and update step window
        t[i] = t_next
        t_current = t_next
        t_next = t_current + dt

        # store state at t_next
        states[:, i] = sol.y[:, -1]

    return states, t