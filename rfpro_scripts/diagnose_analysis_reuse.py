"""Report RFPro analysis-to-result mappings and per-condition reuse evidence.

Run this read-only script inside RFPro. It does not save the project, change
the analysis, create simulations, or touch result files. The public result
paths are reported separately from private flow diagnostics so path and cache
problems are not conflated.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any, Sequence


# Edit this when RFPro's Run Script command cannot pass arguments.
DEFAULT_ANALYSIS_NAME = ""
DEFAULT_LOG_MATCH_LIMIT = 20

_REUSE_LOG_PATTERN = re.compile(
    r"reus|simulating from scratch|existing FEM|"
    r"did not succeed|invalid status|abort|kill|interrupt|traceback",
    re.IGNORECASE,
)
_REQUIRED_CACHE_PATHS = (
    ("reuse hash", Path(".reuse.hash")),
    ("reusable marker", Path("emds_dsn/design/.reusable")),
    ("FEM options", Path("emds_dsn/design/options.xml")),
    ("FEM geometry", Path("emds_dsn/design/design.sat")),
    ("project input", Path("Run0001/project.input")),
    ("geometry input", Path("Run0001/geometry.input")),
)
_LOG_PATHS = (
    Path("project.log"),
    Path("emds_dsn/design/design.log"),
    Path("emds_dsn/design/design.filtered_log"),
    Path("emds_dsn/design/messages.xml"),
    Path("emds_dsn/design/.messages.xml"),
    Path("emds_dsn/design/python_traceback.txt"),
    Path("emds_dsn/design/design_traceback.txt"),
)


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


def cache_status(root: Path) -> dict[str, bool]:
    """Return the reuse prerequisites present directly under one case root."""

    return {label: (root / relative).is_file() for label, relative in _REQUIRED_CACHE_PATHS}


def reuse_log_evidence(root: Path, limit: int) -> list[tuple[Path, list[str]]]:
    """Return the last reuse/failure lines from known logs without modifying them."""

    evidence: list[tuple[Path, list[str]]] = []
    candidates = [root / relative for relative in _LOG_PATHS]
    status_directory = root / "Run0001" / "status"
    if status_directory.is_dir():
        candidates.extend(sorted(status_directory.glob("runstatus.*")))
    for path in candidates:
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as error:
            evidence.append((path, [f"<could not read: {error}>"]))
            continue
        matches = [
            line.strip()
            for line in text.splitlines()
            if _REUSE_LOG_PATTERN.search(line)
        ]
        if matches:
            evidence.append((path, matches[-limit:]))
    return evidence


def _call_private_bool(value: Any) -> str:
    try:
        return str(bool(value())) if callable(value) else "unavailable"
    except Exception as error:
        return f"unavailable ({error})"


def _path_text(value: Any) -> str:
    return str(value or "")


def print_analysis_reuse_report(empro_module: Any, analysis: Any, log_limit: int) -> None:
    output = empro_module.output.AnalysisOutput(analysis)
    settings = analysis.simulationSettings
    simulation_ids = list(output.getAvailableSimulationIds() or [])
    simulation_paths = [
        Path(str(path)) for path in (output.getAvailableSimulationPaths() or [])
    ]
    sequence_mappings = list(output.getAvailableSequenceAndSimulationIds() or [])

    print("RFPro analysis reuse diagnostic (read-only)")
    print(f"Analysis: {analysis.name}")
    print(f"Analysis type: {analysis.analysisType}")
    print(f"Simulation group ID: {analysis.simulationGroup!r}")
    print(f"Simulation group path: {_path_text(analysis.simulationGroupPath)}")
    print(f"Analysis simulation path: {_path_text(analysis.simulationPath)}")
    print(f"Parameter sweep enabled: {bool(settings.parameterSweepEnabled)}")
    print(f"Configured parameter instances: {int(settings.numberOfParameterInstances)}")
    print(f"Configured parameter sequences: {len(settings.parameterSequences)}")
    print(
        "Stored reuseExistingResults: "
        + str(getattr(settings, "reuseExistingResults", "unavailable"))
    )
    print(
        "Simulation-flow V2: "
        + _call_private_bool(getattr(analysis, "_useSimulationFlowV2", None))
    )
    print(
        "Duplicate simulation group: "
        + _call_private_bool(getattr(analysis, "_hasDuplicateGroupId", None))
    )
    print(
        "Analysis-flow version: "
        + str(getattr(output, "_analysisFlowVersion", "unavailable"))
    )
    print(f"Available simulation IDs ({len(simulation_ids)}): {simulation_ids}")
    print(f"Sequence/simulation mappings: {sequence_mappings}")
    print(f"Registered simulation paths: {len(simulation_paths)}")

    reusable_count = 0
    hash_count = 0
    for index, root in enumerate(simulation_paths):
        simulation_id = simulation_ids[index] if index < len(simulation_ids) else "?"
        status = cache_status(root)
        hash_count += int(status["reuse hash"])
        reusable_count += int(status["reusable marker"])
        print(f"\nCondition {index}: simulation ID {simulation_id}")
        print(f"  Registered path: {root}")
        print(f"  Directory exists: {root.is_dir()}")
        for label, present in status.items():
            print(f"  {label}: {present}")
        for log_path, lines in reuse_log_evidence(root, log_limit):
            print(f"  Evidence: {log_path}")
            for line in lines:
                print(f"    {line}")

    print("\nSummary")
    print(f"  Result IDs: {len(simulation_ids)}")
    print(f"  Registered paths: {len(simulation_paths)}")
    print(f"  Paths with .reuse.hash: {hash_count}")
    print(f"  Paths with .reusable: {reusable_count}")
    if len(simulation_ids) != len(simulation_paths):
        print("  WARNING: result-ID and registered-path counts differ.")
    if simulation_paths and reusable_count < len(simulation_paths):
        print(
            "  WARNING: some registered result paths do not contain reusable FEM caches."
        )


def _parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspect RFPro analysis result mappings and reuse evidence."
    )
    parser.add_argument("--analysis", default=DEFAULT_ANALYSIS_NAME)
    parser.add_argument("--log-limit", type=int, default=DEFAULT_LOG_MATCH_LIMIT)
    arguments, unknown = parser.parse_known_args(argv)
    if unknown:
        print("Ignoring RFPro/launcher arguments: " + " ".join(unknown))
    if arguments.log_limit < 1:
        raise ValueError("--log-limit must be positive.")
    return arguments


def main(argv: Sequence[str] | None = None) -> None:
    arguments = _parse_arguments(argv)
    import empro

    analysis = find_analysis(empro.activeProject, arguments.analysis)
    print_analysis_reuse_report(empro, analysis, arguments.log_limit)


if __name__ == "__main__":
    main()
