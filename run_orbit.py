import numpy as np
import plotly.graph_objects as go
from dynamics import acceleration, propagate
from constants import MU, R_EARTH

def main():
    alt = 800.0e3

    r0 = np.array([R_EARTH + alt, 0, 0])
    v_circ = np.sqrt(MU / np.linalg.norm(r0))
    v0 = np.array([0, v_circ, 0])

    state0 = np.concatenate([r0, v0])

    # Orbital period (for a 2-body Kepler problem)
    T = 2 * np.pi * np.sqrt(np.linalg.norm(r0)**3 / MU)
    t = np.linspace(0, 0.5*T, 90)   # more points for smoother curve
    dt = t[1] - t[0]

    xs = np.zeros(len(t))
    ys = np.zeros(len(t))
    zs = np.zeros(len(t))

    state = state0
    t_current = t[0]

    for i in range(t.size):
        t_next = t_current + dt
        xs[i], ys[i], zs[i] = state[:3]   # store 3D position

        state = propagate(state, t_current, t_next)
        t_current = t_next                # <-- advance time

    # --- Earth sphere mesh (centered at origin) ---
    # θ: polar angle [0, π], φ: azimuth [0, 2π]
    phi = np.linspace(0, 2 * np.pi, 60)
    theta = np.linspace(0, np.pi, 30)
    phi, theta = np.meshgrid(phi, theta)

    x_earth = R_EARTH * np.sin(theta) * np.cos(phi)
    y_earth = R_EARTH * np.sin(theta) * np.sin(phi)
    z_earth = R_EARTH * np.cos(theta)

    # --- Build Plotly figure ---
    fig = go.Figure()

    # Orbit trajectory
    fig.add_trace(go.Scatter3d(
        x=xs, y=ys, z=zs,
        mode='lines',
        name='Orbit',
        line=dict(width=3)
    ))

    # Start marker
    fig.add_trace(go.Scatter3d(
        x=[xs[0]], y=[ys[0]], z=[zs[0]],
        mode='markers+text',
        name='Start',
        marker=dict(size=6),
        text=['Start'],
        textposition='top center'
    ))

    # Stop marker (final point)
    fig.add_trace(go.Scatter3d(
        x=[xs[-1]], y=[ys[-1]], z=[zs[-1]],
        mode='markers+text',
        name='Stop',
        marker=dict(size=6),
        text=['Stop'],
        textposition='top center'
    ))

    # Earth surface
    fig.add_trace(go.Surface(
        x=x_earth,
        y=y_earth,
        z=z_earth,
        colorscale='Blues',
        opacity=0.6,
        showscale=False,
        name='Earth'
    ))

    # Layout: axis labels, aspect ratio, title
    fig.update_layout(
        title='3D Orbit Propagation',
        scene=dict(
            xaxis_title='x [m]',
            yaxis_title='y [m]',
            zaxis_title='z [m]',
            aspectmode='data'  # equal scaling in all directions
        ),
        legend=dict(
            x=0.02, y=0.98
        )
    )

    fig.show()

if __name__ == "__main__":
    main()
