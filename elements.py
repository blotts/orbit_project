import numpy as np
from constants import MU


def coe(r_vec, v_vec):
    '''
    Convert position/velocity vectors to classical orbital elements.

    r_vec, v_vec: numpy arrays of shape (3,)
    returns: a, e, i, Omega, w, M (angles in radians)
    '''
    r_norm = np.linalg.norm(r_vec)
    v_norm = np.linalg.norm(v_vec)

    # specific angular momentum
    h_vec = np.cross(r_vec, v_vec)
    h_norm = np.linalg.norm(h_vec)

    # node vector (line of nodes)
    k = np.array([0., 0., 1.])
    n_vec = np.cross(k, h_vec)
    n_norm = np.linalg.norm(n_vec)

    # specific mechanical energy
    energy = v_norm**2 / 2. - MU / r_norm

    # semi-major axis
    if np.isclose(energy, 0., atol = 1e-12):
        a = np.inf  # parabolic case
    else:
        a = -MU / (2. * energy)

    # eccentricity vector and magnitude
    e_vec = (1. / MU) * ((v_norm**2 - MU / r_norm) * r_vec - np.dot(r_vec, v_vec) * v_vec)
    e = np.linalg.norm(e_vec)

    # inclination
    i = np.arccos(np.clip(h_vec[2] / h_norm, -1., 1.))  # stabilize small errors

    # tolerances
    tol_e = 1e-8   # near-circular
    tol_n = 1e-8   # near-equatorial

    # longitude of ascending node (Omega)
    if n_norm < tol_n:
        # equatorial orbit
        Omega = 0.
    else:
        Omega = np.arctan2(n_vec[1], n_vec[0])
    Omega = np.mod(Omega, 2. * np.pi)

    # argument of periapsis (w)
    if (e < tol_e) or (n_norm < tol_n):
        # circular or equatorial orbit
        w = 0.
    else:
        h_hat = h_vec / h_norm

        x = np.dot(n_vec, e_vec) / (n_norm * e)
        y = np.dot(np.cross(n_vec, e_vec), h_hat) / (n_norm * e)

        w = np.arctan2(y, x)
    w = np.mod(w, 2. * np.pi)

    # true anomaly / mean anomaly at epoch
    if (e < tol_e) and (n_norm >= tol_n):
        # circular but not equatorial, use argument of latitude u

        # in-plane basis: n_hat along line of nodes, w_hat 90 degrees ahead
        n_hat = n_vec / n_norm
        h_hat = h_vec / h_norm
        w_hat = np.cross(h_hat, n_hat)

        cos_u = np.dot(r_vec, n_hat) / r_norm
        sin_u = np.dot(r_vec, w_hat) / r_norm
        u = np.arctan2(sin_u, cos_u)

        # choose M = u for circular inclined orbit
        M = u
    elif (e < tol_e) and (n_norm < tol_n):
        # circular AND equatorial: fully degenerate
        M = 0.
    else:
        # radial velocity
        v_r = np.dot(r_vec, v_vec) / r_norm

        # true anomaly nu
        cos_nu = np.dot(e_vec, r_vec) / (e * r_norm)
        sin_nu = v_r * h_norm / (MU * e)
        nu = np.arctan2(sin_nu, cos_nu)

        # eccentric anomaly E from nu
        E = 2. * np.arctan2(
            np.sqrt(1. - e) * np.sin(nu / 2.),
            np.sqrt(1. + e) * np.cos(nu / 2.)
        )

        # mean anomaly M from E
        M = E - e * np.sin(E)

    return a, e, i, Omega, w, M


def compute_elements(states):
    '''
    Compute orbital elements over time from propagated Cartesian states.

    states: array (6, N) with [x, y, z, vx, vy, vz]
    returns: dict of arrays over time for each element
    '''
    N = states.shape[-1]

    a_arr = np.zeros(N)
    e_arr = np.zeros(N)
    i_arr = np.zeros(N)
    Omega_arr = np.zeros(N)
    w_arr = np.zeros(N)
    M_arr = np.zeros(N)

    for k in range(N):
        r_vec = states[:3, k]
        v_vec = states[3:, k]

        a_arr[k], e_arr[k], i_arr[k], Omega_arr[k], w_arr[k], M_arr[k] = coe(r_vec, v_vec)

    return {
        'a': a_arr,
        'e': e_arr,
        'i': i_arr,
        'Omega': Omega_arr,
        'w': w_arr,
        'M': M_arr
    }