import json
import numpy as np
from dynamics import propagate
from constants import MU, R_EARTH
from elements import compute_elements
from plotting import (
    plot_semi_major_axis,
    plot_eccentricity,
    plot_inclination,
    plot_Omega,
    plot_argument_of_periapsis,
    plot_mean_anomaly,
    plot_3d_orbit
)


def main(input_file = 'input.json'):
    '''Load config, propagate orbit, and generate plots.'''
    with open(input_file, 'r') as f:
        cfg = json.load(f)

    # initial state [km, km/s]
    r0 = np.array(cfg['initial_state']['r0'], dtype = float)
    v0 = np.array(cfg['initial_state']['v0'], dtype = float)

    # integration settings
    t_span = np.array(cfg['integration']['t_span'], dtype = float)
    dt = float(cfg['integration']['dt'])

    state0 = np.concatenate([r0, v0])
    states, t = propagate(state0, t_span, dt)

    # convert to orbital elements over time
    elmts = compute_elements(states)
    a = elmts['a']
    e = elmts['e']
    i = elmts['i']
    Omega = elmts['Omega']
    w = elmts['w']
    M = elmts['M']

    # build figures
    fig_orbit = plot_3d_orbit(states)
    fig_a = plot_semi_major_axis(t, a)
    fig_e = plot_eccentricity(t, e)
    fig_i = plot_inclination(t, i)
    fig_Omega = plot_Omega(t, Omega)
    fig_w = plot_argument_of_periapsis(t, w)
    fig_M = plot_mean_anomaly(t, M)

    # show figures
    fig_orbit.show()
    fig_a.show()
    fig_e.show()
    fig_i.show()
    fig_Omega.show()
    fig_w.show()
    fig_M.show()


if __name__ == '__main__':
    main()