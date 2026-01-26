#include <pybind11/pybind11.h>
#include <cmath>
#include <stdexcept>

namespace py = pybind11;

class KeplerSolver {
public:
    explicit KeplerSolver(double central_mass_kg)
        : central_mass_kg_(central_mass_kg)
    {
        if (central_mass_kg_ <= 0.0) {
            throw std::invalid_argument("central_mass_kg must be > 0");
        }
        mu_ = G * central_mass_kg_;
    }

    double central_mass_kg() const { return central_mass_kg_; }
    double mu() const { return mu_; }

    // T = 2π * sqrt(a^3 / μ)
    double period_from_distance(double semi_major_axis_m) const {
        if (semi_major_axis_m <= 0.0) {
            throw std::invalid_argument("semi_major_axis_m must be > 0");
        }
        return 2.0 * M_PI * std::sqrt((semi_major_axis_m * semi_major_axis_m * semi_major_axis_m) / mu_);
    }

    // v = sqrt(μ / r) for circular orbit
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
