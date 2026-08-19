"""Find RFPro sweep points that evaluate to the same parameter condition.

Run this read-only script inside RFPro. It expands every native
``ParameterSequence`` into individual parameter combinations, compares the
documented evaluated ``SingleParameterSweep.parameterValues`` in RFPro
reference units, and reports duplicate groups alongside registered-result
counts. It does not modify parameters, geometry, analyses, or result files.
"""

from __future__ import annotations

import argparse
import itertools
import math
from typing import Any, Mapping, Sequence


# Edit these defaults when RFPro's Run Script command cannot pass arguments.
DEFAULT_ANALYSIS_NAME = ""
DEFAULT_MATCH_REL_TOLERANCE = 1.0e-9
DEFAULT_MATCH_ABS_TOLERANCE = 1.0e-15


def analysis_names(project: Any) -> list[str]:
    return [str(name) for name in project.analyses.names()]


def find_analysis(project: Any, name: str) -> Any:
    names = analysis_names(project)
    if not names:
        raise RuntimeError("The active RFPro project contains no analyses.")
    if name:
        if name not in names:
            raise ValueError(
                f"Analysis {name!r} does not exist. Available analyses: "
                + ", ".join(names)
            )
        return project.analyses[project.analyses.index(name)]
    if len(names) == 1:
        return project.analyses[0]
    raise ValueError(
        "Set DEFAULT_ANALYSIS_NAME or pass --analysis. Available analyses: "
        + ", ".join(names)
    )


def validated_tolerance(value: Any, label: str) -> float:
    try:
        tolerance = float(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{label} must be a finite nonnegative number.") from error
    if not math.isfinite(tolerance) or tolerance < 0.0:
        raise ValueError(f"{label} must be a finite nonnegative number.")
    return tolerance


def _evaluated_sweep_values(sweep: Any) -> tuple[list[float], list[str]]:
    raw_values = getattr(sweep, "parameterValues")
    raw_values = raw_values() if callable(raw_values) else raw_values
    numeric = [float(value) for value in raw_values]
    if not numeric or not all(math.isfinite(value) for value in numeric):
        raise ValueError(
            f"Sweep {str(sweep.parameterName)!r} has no finite evaluated values."
        )

    display: list[str] = []
    getter = getattr(sweep, "getParameterValues", None)
    if callable(getter):
        for arguments in (("ValueAndFrontendUnit",), ()):
            try:
                candidate = [str(value) for value in getter(*arguments)]
            except Exception:
                continue
            if len(candidate) == len(numeric):
                display = candidate
                break
    if not display:
        display = [f"{value:.16g} [reference units]" for value in numeric]
    return numeric, display


def expand_configured_points(settings: Any) -> list[dict[str, Any]]:
    """Expand independent native sequences into individual RFPro conditions."""

    points: list[dict[str, Any]] = []
    for sequence_index, sequence in enumerate(settings.parameterSequences, start=1):
        names: list[str] = []
        numeric_lists: list[list[float]] = []
        display_lists: list[list[str]] = []
        for sweep in sequence:
            name = str(getattr(sweep, "parameterName", "") or "")
            if not name:
                raise ValueError(
                    f"Sequence {sequence_index} contains an unnamed parameter sweep."
                )
            if name in names:
                raise ValueError(
                    f"Sequence {sequence_index} repeats parameter {name!r}."
                )
            numeric, display = _evaluated_sweep_values(sweep)
            names.append(name)
            numeric_lists.append(numeric)
            display_lists.append(display)
        if not names:
            continue

        index_lists = [range(len(values)) for values in numeric_lists]
        for combination_index, value_indices in enumerate(
            itertools.product(*index_lists), start=1
        ):
            numeric_mapping = {
                name: numeric_lists[index][value_index]
                for index, (name, value_index) in enumerate(zip(names, value_indices))
            }
            display_mapping = {
                name: display_lists[index][value_index]
                for index, (name, value_index) in enumerate(zip(names, value_indices))
            }
            points.append(
                {
                    "sequence_index": sequence_index,
                    "combination_index": combination_index,
                    "numeric": numeric_mapping,
                    "display": display_mapping,
                }
            )
    return points


def point_values_match(
    left: Mapping[str, float],
    right: Mapping[str, float],
    relative_tolerance: float,
    absolute_tolerance: float,
) -> bool:
    if left.keys() != right.keys():
        return False
    return all(
        math.isclose(
            left[name],
            right[name],
            rel_tol=relative_tolerance,
            abs_tol=absolute_tolerance,
        )
        for name in left
    )


def duplicate_point_groups(
    points: Sequence[Mapping[str, Any]],
    relative_tolerance: float,
    absolute_tolerance: float,
) -> list[list[int]]:
    """Return zero-based groups of repeated evaluated parameter conditions."""

    relative_tolerance = validated_tolerance(
        relative_tolerance, "Duplicate-match relative tolerance"
    )
    absolute_tolerance = validated_tolerance(
        absolute_tolerance, "Duplicate-match absolute tolerance"
    )
    assigned: set[int] = set()
    groups: list[list[int]] = []
    for first_index, first in enumerate(points):
        if first_index in assigned:
            continue
        matches = [
            candidate_index
            for candidate_index in range(first_index + 1, len(points))
            if candidate_index not in assigned
            and point_values_match(
                first["numeric"],
                points[candidate_index]["numeric"],
                relative_tolerance,
                absolute_tolerance,
            )
        ]
        if matches:
            group = [first_index, *matches]
            groups.append(group)
            assigned.update(group)
    return groups


def _point_label(point: Mapping[str, Any]) -> str:
    return (
        f"sequence {point['sequence_index']}, "
        f"combination {point['combination_index']}"
    )


def _display_mapping(mapping: Mapping[str, str]) -> str:
    return ", ".join(f"{name}={value}" for name, value in mapping.items())


def print_duplicate_sweep_report(
    empro_module: Any,
    analysis: Any,
    relative_tolerance: float,
    absolute_tolerance: float,
) -> None:
    relative_tolerance = validated_tolerance(
        relative_tolerance, "Duplicate-match relative tolerance"
    )
    absolute_tolerance = validated_tolerance(
        absolute_tolerance, "Duplicate-match absolute tolerance"
    )
    settings = analysis.simulationSettings
    points = expand_configured_points(settings)
    groups = duplicate_point_groups(
        points, relative_tolerance, absolute_tolerance
    )
    redundant_count = sum(len(group) - 1 for group in groups)

    output = empro_module.output.AnalysisOutput(analysis)
    simulation_ids = list(output.getAvailableSimulationIds() or [])
    simulation_paths = list(output.getAvailableSimulationPaths() or [])
    sequence_mappings = list(output.getAvailableSequenceAndSimulationIds() or [])

    print("RFPro duplicate sweep-condition diagnostic (read-only)")
    print(f"Analysis: {analysis.name}")
    print(f"Configured parameter sequences: {len(settings.parameterSequences)}")
    print(f"RFPro configured parameter instances: {settings.numberOfParameterInstances}")
    print(f"Python-expanded parameter instances: {len(points)}")
    print(f"Registered simulation IDs: {len(simulation_ids)}")
    print(f"Registered simulation paths: {len(simulation_paths)}")
    print(f"Sequence/simulation mappings: {sequence_mappings}")
    print(f"Relative comparison tolerance: {relative_tolerance:.16g}")
    print(f"Absolute comparison tolerance: {absolute_tolerance:.16g}")

    if groups:
        print("\nDuplicate evaluated condition groups")
        for group_number, group in enumerate(groups, start=1):
            print(
                f"Group {group_number}: "
                + ", ".join(_point_label(points[index]) for index in group)
            )
            for point_index in group:
                point = points[point_index]
                print(
                    f"  {_point_label(point)}: "
                    f"{_display_mapping(point['display'])}"
                )
                reference_values = ", ".join(
                    f"{name}={value:.16g}"
                    for name, value in point["numeric"].items()
                )
                print(f"    Reference units: {reference_values}")
    else:
        print("\nNo duplicate evaluated parameter conditions were found.")

    print("\nSummary")
    print(f"  Duplicate groups: {len(groups)}")
    print(f"  Redundant configured entries: {redundant_count}")
    print(f"  Unique evaluated conditions: {len(points) - redundant_count}")
    missing_result_count = max(len(points) - len(simulation_ids), 0)
    print(f"  Configured-minus-registered count: {missing_result_count}")
    if redundant_count and redundant_count == missing_result_count:
        print(
            "  NOTE: the duplicate count equals the registered-result shortfall. "
            "This is consistent with RFPro coalescing repeated conditions, but "
            "the count match alone does not prove the native selection decision."
        )
    elif missing_result_count:
        print(
            "  NOTE: evaluated duplicates do not fully explain the result "
            "shortfall. Check ignored CSV headings, invalid geometry, and the "
            "analysis reuse/cache diagnostics."
        )


def _parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Find duplicate evaluated RFPro sweep conditions."
    )
    parser.add_argument("--analysis", default=DEFAULT_ANALYSIS_NAME)
    parser.add_argument(
        "--match-rel-tol",
        type=float,
        default=DEFAULT_MATCH_REL_TOLERANCE,
    )
    parser.add_argument(
        "--match-abs-tol",
        type=float,
        default=DEFAULT_MATCH_ABS_TOLERANCE,
    )
    arguments, unknown = parser.parse_known_args(argv)
    if unknown:
        print("Ignoring RFPro/launcher arguments: " + " ".join(unknown))
    validated_tolerance(
        arguments.match_rel_tol, "Duplicate-match relative tolerance"
    )
    validated_tolerance(
        arguments.match_abs_tol, "Duplicate-match absolute tolerance"
    )
    return arguments


def main(argv: Sequence[str] | None = None) -> None:
    arguments = _parse_arguments(argv)
    import empro

    analysis = find_analysis(empro.activeProject, arguments.analysis)
    print_duplicate_sweep_report(
        empro,
        analysis,
        arguments.match_rel_tol,
        arguments.match_abs_tol,
    )


if __name__ == "__main__":
    main()
