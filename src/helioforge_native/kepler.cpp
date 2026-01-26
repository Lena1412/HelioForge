// src/helioforge_native/kepler.cpp
//
// Native Kepler solver for helioforge.
//
// This file defines a small C++ helper class and exposes it to Python via
// pybind11. The Python package uses this module opportunistically (if present)
// to speed up repeated Kepler-law calculations in realtime simulations.
//
// IMPORTANT:
// - The gravitational constant value MUST match `helioforge.constants.G`.
// - The formulas assume a two-body system where the orbiting mass is negligible.
//
// Build output module name: `helioforge_native`

#include <pybind11/pybind11.h>
#include <cmath>
#include <stdexcept>

namespace py = pybind11;

/**
 * @brief Minimal Kepler-law helper for circular orbits.
 *
 * This class provides:
 * - period from semi-major axis
 * - circular-orbit speed from radius
 *
 * It precomputes the standard gravitational parameter μ = G*M for the
 * configured central mass.
 */
class KeplerSolver {
public:
    /**
     * @brief Construct the solver for a given central mass.
     *
     * @param central_mass_kg Mass of the central body in kilograms.
     * @throws std::invalid_argument if central_mass_kg <= 0.
     */
    explicit KeplerSolver(double central_mass_kg)
        : central_mass_kg_(central_mass_kg)
    {
        if (central_mass_kg_ <= 0.0) {
            throw std::invalid_argument("central_mass_kg must be > 0");
        }
        mu_ = G * central_mass_kg_;
    }

    /// Central body mass in kg.
    double central_mass_kg() const { return central_mass_kg_; }

    /// Standard gravitational parameter μ = G*M.
    double mu() const { return mu_; }

    // T = 2π * sqrt(a^3 / μ)
    /**
     * @brief Compute orbital period from semi-major axis (two-body approximation).
     *
     * @param semi_major_axis_m Semi-major axis in meters (radius for circular orbit).
     * @return Orbital period in seconds.
     * @throws std::invalid_argument if semi_major_axis_m <= 0.
     */
    double period_from_distance(double semi_major_axis_m) const {
        if (semi_major_axis_m <= 0.0) {
            throw std::invalid_argument("semi_major_axis_m must be > 0");
        }
        return 2.0 * M_PI * std::sqrt((semi_major_axis_m * semi_major_axis_m * semi_major_axis_m) / mu_);
    }

    // v = sqrt(μ / r) for circular orbit
    /**
     * @brief Compute circular-orbit speed at a given radius.
     *
     * @param distance_m Orbital radius in meters.
     * @return Orbital speed in meters per second.
     * @throws std::invalid_argument if distance_m <= 0.
     */
    double circular_speed_from_distance(double distance_m) const {
        if (distance_m <= 0.0) {
            throw std::invalid_argument("distance_m must be > 0");
        }
        return std::sqrt(mu_ / distance_m);
    }

private:
    // Must match helioforge.constants.G
    static constexpr double G = 6.67430e-11;

    double central_mass_kg_;
    double mu_;
};

PYBIND11_MODULE(helioforge_native, m) {
    m.doc() = "Native Kepler solver for helioforge (pybind11).";

    py::class_<KeplerSolver>(m, "KeplerSolver")
        .def(py::init<double>(), py::arg("central_mass_kg"))
        .def_property_readonly("central_mass_kg", &KeplerSolver::central_mass_kg)
        .def_property_readonly("mu", &KeplerSolver::mu)
        .def("period_from_distance", &KeplerSolver::period_from_distance, py::arg("semi_major_axis_m"))
        .def("circular_speed_from_distance", &KeplerSolver::circular_speed_from_distance, py::arg("distance_m"));
}
