# 🚀 Orbit Project








A minimalist two-body orbital dynamics simulator written in Python.
The project propagates spacecraft motion using a high-order DOP853 integrator,
computes classical orbital elements, and generates clean 2D/3D visualizations.

Designed to be readable, modular, and extensible — suitable for aerospace,
mission design, and scientific computing portfolios.

---

## ✨ Features
• Two-body gravitational dynamics
• High-accuracy DOP853 propagation
• Orbital element generation (a, e, i, Ω, ω, M)
• Interactive 3D orbit visualization
• Fully JSON-driven input configuration
• Lightweight and easy to extend

---

## 📁 Project Structure
constants.py — physical constants
dynamics.py — propagation + gravitational model
elements.py — Cartesian → orbital elements
plotting.py — 2D/3D visualization utilities
run_orbit.py — main simulation driver
input.json — user-defined initial conditions

---

## ▶️ Usage

Install dependencies:
pip install numpy scipy plotly

Run a simulation:
python run_orbit.py

Input JSON file can be copied and modified to simulate custom orbits

---

## 🔧 Extend the Project
Easy to expand with:
• J2 or higher-order gravity
• Drag, SRP, or custom forces
• Maneuver modeling
• Ground tracks, radius plots, or Monte-Carlo runs

---

## 📄 License
For educational and personal use.