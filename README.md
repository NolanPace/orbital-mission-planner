# Orbital Mission Planner

A tested, dependency-free astrodynamics utility for **two-body circular-orbit Hohmann transfer calculations** and **2D Keplerian orbit propagation**. Includes a self-contained HTML trajectory visualization.

## Try it
Python 3.10+ required.
```bash
python main.py --from-km 400 --to-km 35786 --json --plot
python -m unittest discover -s tests -v
```
The `--plot` option creates `transfer.html` which you can open in a browser.

## Features
- Analytical Hohmann transfer first and second impulses, total delta-v, and transfer time
- Orbital circular velocity and period
- Kepler's equation solved with Newton iteration, and planar elliptical propagation
- No dependency on orbital mechanics packages

## Assumptions
Two-body point-mass gravity, impulsive maneuver, coplanar circular starting and target orbits. No perturbations, thrust limits, plane changes, launch windows, or collision constraints. Calculated trajectories are *illustrative*, not flight-certified.

MIT licensed.