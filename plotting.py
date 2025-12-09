import numpy as np
import plotly.graph_objects as go
from constants import R_EARTH

DEG = 180. / np.pi

def plot_semi_major_axis(t, a):
    '''Line plot of semi-major axis vs time.'''
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x = t,
            y = a,
            mode = 'lines',
            name = 'a'
        )
    )

    fig.update_layout(
        title = 'Semi-major Axis vs Time',
        xaxis_title = 'Time [s]',
        yaxis_title = 'a [km]',
        yaxis = dict(range = [0.5 * np.min(a), 1.5 * np.max(a)]),
        template = 'plotly_dark'
    )

    return fig


def plot_eccentricity(t, e):
    '''Line plot of eccentricity vs time.'''
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x = t,
            y = e,
            mode = 'lines',
            name = 'e'
        )
    )

    fig.update_layout(
        title = 'Eccentricity vs Time',
        xaxis_title = 'Time [s]',
        yaxis_title = 'e [-]',
        yaxis = dict(range = [0., max(1., 1.1 * np.max(e))]),
        template = 'plotly_dark'
    )

    return fig


def plot_inclination(t, i_rad):
    '''
    Plot inclination vs time.

    Angles in radians, converted to degrees for plotting.
    '''
    i_deg = i_rad * DEG
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x = t,
            y = i_deg,
            mode = 'lines',
            name = 'Inclination i'
        )
    )

    fig.update_layout(
        title = 'Inclination vs Time',
        xaxis_title = 'Time [s]',
        yaxis_title = 'Angle [deg]',
        yaxis = dict(range = [0., 2. * np.pi * DEG]),
        template = 'plotly_dark'
    )

    return fig


def plot_Omega(t, Omega_rad):
    '''Plot longitude of ascending node vs time.'''
    Omega_deg = Omega_rad * DEG
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x = t,
            y = Omega_deg,
            mode = 'lines',
            name = 'Ω'
        )
    )

    fig.update_layout(
        title = 'Longitude of Ascending Node (Ω) vs Time',
        xaxis_title = 'Time [s]',
        yaxis_title = 'Ω [deg]',
        yaxis = dict(range = [0., 2. * np.pi * DEG]),
        template = 'plotly_dark'
    )

    return fig


def plot_argument_of_periapsis(t, w_rad):
    '''Plot argument of periapsis vs time.'''
    w_deg = w_rad * DEG
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x = t,
            y = w_deg,
            mode = 'lines',
            name = 'ω'
        )
    )

    fig.update_layout(
        title = 'Argument of Periapsis (ω) vs Time',
        xaxis_title = 'Time [s]',
        yaxis_title = 'ω [deg]',
        yaxis = dict(range = [0., 2. * np.pi * DEG]),
        template = 'plotly_dark'
    )

    return fig


def plot_mean_anomaly(t, M_rad):
    '''Plot mean anomaly vs time, unwrapped for continuity.'''
    M_deg = np.unwrap(M_rad) * DEG
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x = t,
            y = M_deg,
            mode = 'lines',
            name = 'M'
        )
    )

    fig.update_layout(
        title = 'Mean Anomaly (M) vs Time',
        xaxis_title = 'Time [s]',
        yaxis_title = 'M [deg]',
        template = 'plotly_dark'
    )

    return fig


def plot_3d_orbit(states):
    '''
    3D orbit plot with Earth as a sphere.

    states: array (6, N) with [x, y, z, vx, vy, vz]
    R_EARTH: Earth radius [km]
    '''
    x = states[0, :]
    y = states[1, :]
    z = states[2, :]

    # Earth sphere parameterization
    u = np.linspace(0., 2. * np.pi, 40)
    v = np.linspace(0., np.pi, 20)
    uu, vv = np.meshgrid(u, v)

    xe = R_EARTH * np.cos(uu) * np.sin(vv)
    ye = R_EARTH * np.sin(uu) * np.sin(vv)
    ze = R_EARTH * np.cos(vv)

    fig = go.Figure()

    # Earth
    fig.add_trace(
        go.Surface(
            x = xe,
            y = ye,
            z = ze,
            opacity = 0.6,
            colorscale = 'Blues',
            showscale = False,
            name = 'Earth'
        )
    )

    # Orbit trajectory
    fig.add_trace(
        go.Scatter3d(
            x = x,
            y = y,
            z = z,
            mode = 'lines',
            name = 'Orbit',
            line = dict(width = 3)
        )
    )

    # Start marker
    fig.add_trace(
        go.Scatter3d(
            x = [x[0]],
            y = [y[0]],
            z = [z[0]],
            mode = 'markers',
            name = 'Start',
            marker = dict(size = 6, symbol = 'circle')
        )
    )

    # End marker
    fig.add_trace(
        go.Scatter3d(
            x = [x[-1]],
            y = [y[-1]],
            z = [z[-1]],
            mode = 'markers',
            name = 'Stop',
            marker = dict(size = 5, symbol = 'circle')
        )
    )

    # Layout: axis labels, aspect ratio, title
    fig.update_layout(
        title = '3D Orbit Propagation',
        scene = dict(
            xaxis_title = 'x [km]',
            yaxis_title = 'y [km]',
            zaxis_title = 'z [km]',
            aspectmode = 'data'  # equal scaling in all directions
        ),
        legend = dict(
            x = 0.02,
            y = 0.98
        )
    )

    return fig
