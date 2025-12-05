import json
import numpy as np
from dynamics import propagate
from constants import MU, R_EARTH
from elements import compute_elements
from plotting import (
    plot_semi_major_axis,
    plot_eccentricity,
    plot_inclination,
    plot_3d_orbit,
)

def main(input_file = 'input.json'):

    with open(input_file, 'r') as f:
        cfg = json.load(f)

    r0 = np.array(cfg["r0"], dtype = float)
    v0 = np.array(cfg["v0"], dtype = float)
    t_span = np.array(cfg["t_span"], dtype = float)
    dt = float(cfg["dt"])

    state0 = np.concatenate([r0, v0])
    states, t = propagate(state0, t_span, dt)

    elmts = compute_elements(states)
    a = elmts['a']
    e = elmts['e']
    i = elmts['i']

    fig_orbit = plot_3d_orbit(states)
    fig_a = plot_semi_major_axis(t, a)
    fig_e = plot_eccentricity(t, e)
    fig_i = plot_inclination(t, i)

    fig_orbit.show()
    fig_a.show()
    fig_e.show()
    fig_i.show()

if __name__ == "__main__":
    main()