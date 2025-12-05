import numpy as np
from constants import MU

def coe(r_vec, v_vec):
    '''
    convert position/velocity vectors to classical orbital elements
    r_vec, v_vec: numpy arrays of shape (3,)
    returns: a, e, i (angles in radians)
    '''
    r_norm = np.linalg.norm(r_vec)
    v_norm = np.linalg.norm(v_vec)

    # specific angular momentum
    h_vec = np.cross(r_vec, v_vec)
    h_norm = np.linalg.norm(h_vec)

    # eccentricity vector
    e_vec = (1. / MU) * ((v_norm**2 - MU / r_norm) * r_vec - np.dot(r_vec, v_vec) * v_vec)
    e = np.linalg.norm(e_vec)

    # specific mechanical energy
    energy = v_norm**2 / 2. - MU / r_norm

    # semi major axis
    if np.isclose(energy, 0., atol = 1e-12):
        a = np.inf # parabolic case
    else:
        a = -MU / (2. * energy)
    
    # inclination
    i = np.arccos(np.clip(h_vec[2] / h_norm, -1., 1.)) # stabilize small errors

    return e, a, i

def compute_elements(states):
    '''
    states: array (6, N) with [x, y, z, vx, vy, vz]
    Returns dict of arrays over time
    '''
    N = states.shape[-1]

    a_arr = np.zeros(N)
    e_arr = np.zeros(N)
    i_arr = np.zeros(N)

    for i in range(N):
        r_vec = states[:3, i]
        v_vec = states[3:, i]

        e_arr[i], a_arr[i], i_arr[i] = coe(r_vec, v_vec)

    return {
        'e': e_arr,
        'a': a_arr,
        'i': i_arr
    }