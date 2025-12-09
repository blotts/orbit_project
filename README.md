# Orbit Project

This project implements a complete orbital mechanics workflow in Python, including numerical propagation of a two-body orbit, orbital element computation, and interactive 2D/3D visualizations.

The simulation loads initial conditions from a JSON file, propagates the spacecraft state using a high-order integrator, converts Cartesian state vectors into classical orbital elements, and generates a collection of plots that describe the orbit’s geometry and time evolution.

All quantities use kilometers, km/s, and seconds. All vectors are expressed in the Earth-Centered Inertial (ECI) frame.

---

## Features

• Two-body gravitational dynamics
• High-accuracy DOP853 propagation from SciPy
• Conversion from position/velocity to classical orbital elements
• 3D orbit visualization with Earth rendered as a sphere
• Automatic generation of diagnostic plots, including:
– Semi-major axis
– Eccentricity
– Inclination
– RAAN (Ω)
– Argument of periapsis (ω)
– Mean anomaly (M)

---

## Project Structure

The repository is organized into focused modules:

Orbit_Project
• constants.py – Physical constants
• dynamics.py – Gravitational model and numerical state propagation
• elements.py – Conversion from Cartesian state to orbital elements
• plotting.py – Interactive 2D and 3D visualization utilities
• run_orbit.py – Main entry point for running simulations
• input.json – User-defined initial conditions and integrator settings

---

## Input Configuration

The simulation is driven entirely by an input JSON file containing initial conditions and integration settings.

Example fields:

• r0 – Initial ECI position vector in kilometers
• v0 – Initial ECI velocity vector in km/s
• t_span – Start and end times for the simulation
• dt – Output time step

Keeping inputs external allows you to change missions or test cases without touching the source code.

---

## Installation

Required packages:

• Python 3.9 or later
• NumPy
• SciPy
• Plotly

Install packages with:

pip install numpy scipy plotly

---

## Usage

Run the JSON configuration:

python run_orbit.py

After running, the script displays:

• A 3D orbit visualization
• Semi-major axis vs. time
• Eccentricity vs. time
• Inclination vs. time
• RAAN vs. time
• Argument of periapsis vs. time
• Mean anomaly vs. time

---

## Extending the Project

The modular structure makes the project easy to expand. Possible extensions:

• J2 or higher-order gravitational models
• Atmospheric drag or solar radiation pressure
• Ground track generation
• Impulsive or finite-burn maneuvers
• Monte Carlo analysis for sensitivity studies
• Relative motion modeling