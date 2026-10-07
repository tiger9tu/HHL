"""Paper D1 FLOP model -> HPCG-based solver-core time and energy.

Real FP64 rate-transfer assumption; no solver or HPCG execution.
"""
import argparse
import json
import math
from pathlib import Path

MODEL_VERSION = "classical-d1-hpcg-v1"


def _positive_integer(value, name):
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(name + " must be a positive integer")


def _finite_positive(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(name + " must be a finite positive number")
    try:
        valid = math.isfinite(value) and value > 0
    except OverflowError:
        valid = False
    if not valid:
        raise ValueError(name + " must be a finite positive number")


def logical_resources(N, kappa, s, epsilon, rounding="ceil"):
    """Return the literal D1 count and the selected iteration-rounding model."""
    _positive_integer(N, "N")
    _positive_integer(s, "s")
    _finite_positive(kappa, "kappa")
    _finite_positive(epsilon, "epsilon")
    if s > N or kappa < 1 or epsilon >= 1:
        raise ValueError("Require s <= N, kappa >= 1 and 0 < epsilon < 1")
    if rounding not in ("ceil", "paper"):
        raise ValueError("rounding must be 'ceil' or 'paper'")
    iterations = 0.5 * kappa * (math.log(2) - math.log(epsilon))
    _finite_positive(iterations, "iteration estimate")
    per_iteration = N * (4 * s + 14)
    try:
        paper_flops = iterations * per_iteration
    except OverflowError:
        raise ValueError("FLOP estimate exceeds floating-point range")
    _finite_positive(paper_flops, "FLOP estimate")
    chosen_iterations = math.ceil(iterations) if rounding == "ceil" else iterations
    return {
        "model_version": MODEL_VERSION,
        "algorithm": "paper D1 normal-equation CG (CGNE-labeled; CGLS/CGNR recurrence)",
        "N": N, "kappa_original": kappa, "s": s,
        "epsilon_relative_solution": epsilon,
        "iterations_paper": iterations,
        "iterations_selected": chosen_iterations,
        "rounding": rounding,
        "flops_per_iteration": per_iteration,
        "nflops_paper": paper_flops,
        "nflops": chosen_iterations * per_iteration,
        "status": "analytical arithmetic model, not measured instructions",
    }


def physical_resources(nflops, hardware):
    """Project using a single hardware.json profile; PFLOP/s and kW inputs."""
    _finite_positive(nflops, "nflops")
    _finite_positive(hardware["hpcg_pflop_s"], "HPCG PFLOP/s")
    _finite_positive(hardware["power_kW"], "power kW")
    rate = hardware["hpcg_pflop_s"] * 1e15
    power = hardware["power_kW"] * 1e3
    _finite_positive(rate, "FLOP/s")
    _finite_positive(power, "power W")
    time_s = nflops / rate
    energy_J = time_s * power
    _finite_positive(time_s, "projected time")
    _finite_positive(energy_J, "projected energy")
    return {
        "system": hardware["id"],
        "hpcg_pflop_s": hardware["hpcg_pflop_s"],
        "power_kW": hardware["power_kW"],
        "core_time_s": time_s,
        "core_energy_J": energy_J,
        "core_energy_kWh": energy_J / 3.6e6,
        "status": "HPCG-rate projection with unpaired system-power proxy",
        "scope": "solver core only; end-to-end costs and capacity unresolved",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--N", type=int, required=True)
    parser.add_argument("--kappa", type=float, required=True)
    parser.add_argument("--s", type=int, required=True)
    parser.add_argument("--epsilon", type=float, required=True)
    parser.add_argument("--rounding", choices=("ceil", "paper"), default="ceil")
    parser.add_argument("--system", default="all", help="Profile ID, or all (default)")
    parser.add_argument("--hardware", type=Path,
                        default=Path(__file__).with_name("hardware.json"))
    args = parser.parse_args()
    try:
        config = json.loads(args.hardware.read_text())
        profiles = [p for p in config["profiles"]
                    if args.system == "all" or p["id"] == args.system]
        if not profiles:
            raise ValueError("No matching hardware profile: " + args.system)
        logical = logical_resources(args.N, args.kappa, args.s,
                                    args.epsilon, args.rounding)
        result = {"logical": logical, "hardware_version": config["version"],
                  "physical": [physical_resources(logical["nflops"], p)
                               for p in profiles]}
        print(json.dumps(result, indent=2, allow_nan=False))
    except (ValueError, KeyError, TypeError, OSError, OverflowError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
