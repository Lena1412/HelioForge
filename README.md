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

##  Step-by-step design
Each file has a short explanation of the workflow, but here is a summary of it.

This project was done in a step-by-step manner. The first step was research. I looked through the examples given in the project's description and many other sources like tutorials, blogs for beginner programmers and git projects. It is a very basic project so I found a lot of different variations of it. One commonality I found was that the projects where mostly very short and basic (some of them even contained in one file). So even though I mostly knew what has to be done, I had to do it in a different more complex way with multiple files, testing, documentation and so on. After looking through all the different ways it could be done, I decided to use pygame for visualisation, since I have dabbled in it before (I had a class on Python where we each had to present a PYTHON library and I chose pygame). I have only used it for making small games, but figured that just visualisation should be simple.

However, before visualising anything I had to create the basis. And so the helioforge core was created first: the classes for the celestial bodies and the whole system for "storing" them, the math behind it (python version of kepler), and the preset (solar system) to have something to test on. At first a fantasy theme was used for naming. To do that I used chatGPT to come up with a list of fantasy-sounding short words connected to cosmos and then by myself joined them into the names (helio-forge, cosmo-view). However, after a consultation with a senior developer, decided to change most of them into simpler and more readable names commonly used in the iterations of this project. Only the modules' names remain fantasy-themed, but you can find the old names  in the proper files. Not all files have the old names, since the initial plan assumed a different, simpler file structure, which became more complex along the way. Next I focused on the C++ part (helioforge_native) using pybind and after that I moved onto the visualisation part (cosmoview): reading in the data from helioforge, the simple visualisation of the system, the movements of the bodies and then the UI and so on (play/pause, zoom-in/out, speed-up, the ).

And then came the time to think what else I could add and how to make this into a proper project. I added the usage from command line (this was something I'd been wanting to try for a while in my day-to-day work, but could not due to time constraints), the generation of a random system, and the option to export and import systems using .json files. Finally, I created the tests, the documentation (using mkdocs), finished up the readme, and prepared the examples and the demo notebook. The old repository's history was convoluted (at first I used branches, then I decided not to; it was overall messy) and so I decided to create a new one with a clean and descriptive history. 

Important note: this project was done with a help of a senior developer (my sister). Since it was my first standalone project, I had her "supervising" my progress. She read through all of the code and gave points on how to improve it or make it more readable and professional (for example the confusing naming convention, keeping the constants in a separate file instead of defining them multiple times across different files, or creating the example files to show how the code can actually be used).

Additional comments with explanation and sometimes the old names were added to the src files.
The additional comments were not added to the following files .gitignore, CMakeLists.txt, demo.ipynb, LICENSE, pyproject.toml, and the docs, example and test files.
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
