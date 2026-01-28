# HelioForge & CosmoView

HelioForge is a small Python library for building and simulating simple heliocentric
planetary systems using circular Keplerian orbits.
CosmoView is a lightweight pygame-based viewer for visualizing those simulations
interactively.

The project is intentionally minimal and educational:
- no N-body gravity,
- no orbital perturbations,
- no external physics engines.

It focuses on clarity, determinism, and smooth visualization.

---

## Project structure

```
HelioForge/
├── src/
│   ├── helioforge/          # Core simulation & data model
│   ├── cosmoview/           # Pygame-based visualization
│   └── helioforge_native/   # (optional) C++ Kepler solver
├── docs/                    # MkDocs documentation
├── tests/                   # Pytest test suite
├── examples/                # Usage examples
└── pyproject.toml
```

---

## HelioForge

HelioForge provides a small set of building blocks for heliocentric simulations.

### Core concepts

- **CentralBody**  
  Represents the central mass (e.g. a star).

- **Planet**  
  A planet on a 2D circular orbit defined by:
  - orbital radius,
  - phase angle,
  - orbital period and speed.

- **SolarSystem**  
  Container holding a central body and a list of planets.

- **Simulation**  
  Advances a `SolarSystem` forward in time using fixed time steps.

---

### Orbital mechanics

- Uses Kepler’s third law to compute:
  - orbital period from distance,
  - circular orbit speed.
- Implemented in pure Python.
- Optional native acceleration via `helioforge_native` (C++ / pybind11).
  - Automatically used if available.
  - Falls back to Python if not present.

---

### Procedural generation

The `generation` module can create deterministic, visually plausible systems:

- Log-spaced orbital distances
- Simple planet type classification:
  - rocky
  - gas giant
  - ice giant
  - dwarf
- Rough mass and radius heuristics per type

This is intended for demos and visualization, not scientific accuracy.

---

### Presets

A built-in approximate **Solar System** preset is provided:

- Sun + eight major planets
- Roughly correct ordering and periods
- Suitable for demos and sanity checks

---

### Export

A `SolarSystem` can be serialized to JSON using:

- `to_json(system)`
- `save_json(system, path)`

---

## CosmoView

CosmoView is a standalone pygame viewer for HelioForge simulations.

### Features

- Real-time visualization of circular orbits
- Logarithmic distance scaling
- Smooth rendering via supersampling
- Interactive controls:
  - play / pause
  - speed up / slow down
  - zoom in / out
  - toggle labels
  - toggle statistics overlay
- Keyboard and mouse shortcuts
- Deterministic demo modes

---

### Running the viewer

```bash
cosmoview --mode solar
```

or:

```bash
cosmoview --mode random
```

Available options:

```bash
cosmoview --help
```

---

## Installation

### Basic installation (library only)

```bash
pip install -e .
```

### With viewer support

```bash
pip install -e ".[view]"
```

### With documentation tools

```bash
pip install -e ".[docs]"
```

### Optional native acceleration

If you want the C++ Kepler solver:

```bash
pip install pybind11
# then build helioforge_native using your build system
```

This step is optional; HelioForge works fully without it.

---

## Documentation

API documentation is generated from docstrings using MkDocs:

```bash
mkdocs serve
```

Then open:

http://127.0.0.1:8000/

---

## Testing

Run the test suite with:

```bash
pytest
```

Tests cover:
- Kepler formulas (Python and native)
- Model behavior
- Procedural generation
- System stepping
- Presets

---

## Intended use

HelioForge and CosmoView are suitable for:

- educational demos,
- teaching orbital mechanics basics,
- visualization experiments,
- lightweight simulations where clarity matters more than realism.

They are **not** intended for high-precision astrophysical modeling.
