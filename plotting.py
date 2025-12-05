import numpy as np
import plotly.graph_objects as go
from constants import R_EARTH

DEG = 180.0 / np.pi

def plot_semi_major_axis(t, a):
    """Line plot of semi-major axis vs time."""
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=t,
            y=a,
            mode="lines",
            name="a",
        )
    )

    fig.update_layout(
        title="Semi-major Axis vs Time",
        xaxis_title="Time [s]",
        yaxis_title="a [km]",
        yaxis=dict(range=[0.5 * np.min(a), 1.5 * np.max(a)]),
        template="plotly_dark",
    )

    return fig

def plot_eccentricity(t, e):
    """line plot of eccentricity vs time (zoomed to [0, 1])."""
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=t,
            y=e,
            mode="lines",
            name="e",
        )
    )

    fig.update_layout(
        title="Eccentricity vs Time",
        xaxis_title="Time [s]",
        yaxis_title="e [-]",
        yaxis=dict(range=[0, max(1.0, 1.1 * np.max(e))]),
        template="plotly_dark",
    )

    return fig

def plot_inclination(t, i_rad):
    """
    plot inclination vs time
    Angles in radians, converted to degrees for plotting
    """

    i_deg = i_rad * (180. / np.pi)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=t,
            y=i_deg,
            mode="lines",
            name="Inclination i",
        )
    )

    fig.update_layout(
        title="Inclination vs Time",
        xaxis_title="Time [s]",
        yaxis_title="Angle [deg]",
        yaxis=dict(range=[0.5 * np.min(i_deg), 1.5 * np.max(i_deg)]),
        template="plotly_dark",
    )

    return fig

def plot_3d_orbit(states):
    """
    3D orbit plot with Earth as a sphere.
    states: array (N, 6) -> [x, y, z, vx, vy, vz]
    R_EARTH: Earth radius [km]
    """
    x = states[0, :]
    y = states[1, :]
    z = states[2, :]

    # Earth sphere parameterization
    u = np.linspace(0, 2 * np.pi, 40)
    v = np.linspace(0, np.pi, 20)
    uu, vv = np.meshgrid(u, v)

    xe = R_EARTH * np.cos(uu) * np.sin(vv)
    ye = R_EARTH * np.sin(uu) * np.sin(vv)
    ze = R_EARTH * np.cos(vv)

    fig = go.Figure()

    # Earth
    fig.add_trace(
        go.Surface(
            x=xe,
            y=ye,
            z=ze,
            opacity=0.6,
            colorscale="Blues",
            showscale=False,
            name="Earth",
        )
    )

    # Orbit trajectory
    fig.add_trace(
        go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode="lines",
            name="Orbit",
            line=dict(width=3),
        )
    )

    # Start / end markers
    fig.add_trace(
        go.Scatter3d(
            x=[x[0]],
            y=[y[0]],
            z=[z[0]],
            mode="markers+text",
            name='Start',
            marker=dict(size=6, symbol="circle"),
        )
    )

    fig.add_trace(
        go.Scatter3d(
            x=[x[-1]],
            y=[y[-1]],
            z=[z[-1]],
            mode="markers+text",
            name='Stop',
            marker=dict(size=5, symbol="circle"),
        )
    )

    # Layout: axis labels, aspect ratio, title
    fig.update_layout(
        title='3D Orbit Propagation',
        scene=dict(
            xaxis_title='x [km]',
            yaxis_title='y [km]',
            zaxis_title='z [km]',
            aspectmode='data'  # equal scaling in all directions
        ),
        legend=dict(
            x=0.02, y=0.98
        )
    )
    
    return fig