"""Find unique RFPro FEM reuse caches and compare them with registered paths.

Run this read-only script inside RFPro. Unlike an exploratory recursive search,
each cache root is printed exactly once. Registered analysis paths and orphaned
or historical caches are identified separately.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any, Sequence


# Edit these when RFPro's Run Script command cannot pass arguments.
DEFAULT_ANALYSIS_NAME = ""
DEFAULT_SCAN_ROOT = ""
DEFAULT_SCAN_PARENT_LEVELS = 2


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


def normalized_path(path: Path) -> str:
    return os.path.normcase(os.path.abspath(str(path)))


def derive_scan_root(
    configured_root: str,
    simulation_group_path: str,
    registered_paths: Sequence[Path],
    parent_levels: int,
) -> Path:
    """Choose an explicit root or walk upward from the analysis result group."""

    if configured_root:
        return Path(configured_root).expanduser()
    group_text = str(simulation_group_path or "").strip()
    if group_text:
        root = Path(group_text)
    elif registered_paths:
        common = os.path.commonpath([str(path) for path in registered_paths])
        root = Path(common)
    else:
        raise RuntimeError(
            "RFPro exposes no result path. Set DEFAULT_SCAN_ROOT or pass --root."
        )
    for _ in range(parent_levels):
        parent = root.parent
        if parent == root:
            break
        root = parent
    return root


def find_cache_roots(scan_root: Path) -> list[Path]:
    """Return unique directories containing a reuse hash or reusable marker."""

    roots: dict[str, Path] = {}
    for hash_file in scan_root.rglob(".reuse.hash"):
        root = hash_file.parent
        roots[normalized_path(root)] = root
    for marker in scan_root.rglob(".reusable"):
        try:
            root = marker.parents[2]
        except IndexError:
            continue
        if marker.parent.name != "design" or marker.parent.parent.name != "emds_dsn":
            continue
        roots[normalized_path(root)] = root
    return sorted(roots.values(), key=lambda path: normalized_path(path))


def print_cache_inventory(
    analysis: Any, registered_paths: Sequence[Path], scan_root: Path
) -> None:
    if not scan_root.is_dir():
        raise FileNotFoundError(f"Reuse-cache scan root does not exist: {scan_root}")
    registered = {normalized_path(path) for path in registered_paths}
    cache_roots = find_cache_roots(scan_root)

    print("RFPro reusable-cache inventory (read-only)")
    print(f"Analysis: {analysis.name}")
    print(f"Simulation group ID: {analysis.simulationGroup!r}")
    print(f"Simulation group path: {analysis.simulationGroupPath}")
    print(f"Scan root: {scan_root}")
    print(f"Registered result paths: {len(registered_paths)}")
    print(f"Unique cache roots found: {len(cache_roots)}")

    if registered_paths:
        print("\nRegistered result paths")
        for path in registered_paths:
            print(
                f"  {path} | hash={(path / '.reuse.hash').is_file()} "
                f"| reusable={(path / 'emds_dsn/design/.reusable').is_file()}"
            )

    print("\nUnique cache roots")
    registered_cache_count = 0
    orphaned_cache_count = 0
    for root in cache_roots:
        is_registered = normalized_path(root) in registered
        registered_cache_count += int(is_registered)
        orphaned_cache_count += int(not is_registered)
        print(
            f"  {root} | registered={is_registered} "
            f"| hash={(root / '.reuse.hash').is_file()} "
            f"| reusable={(root / 'emds_dsn/design/.reusable').is_file()}"
        )

    print("\nSummary")
    print(f"  Registered paths that are cache roots: {registered_cache_count}")
    print(f"  Unregistered/historical cache roots: {orphaned_cache_count}")
    if not cache_roots:
        print("  No reuse metadata was found under the selected scan root.")


def _parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Find unique RFPro FEM caches and compare registered paths."
    )
    parser.add_argument("--analysis", default=DEFAULT_ANALYSIS_NAME)
    parser.add_argument("--root", default=DEFAULT_SCAN_ROOT)
    parser.add_argument(
        "--parent-levels", type=int, default=DEFAULT_SCAN_PARENT_LEVELS
    )
    arguments, unknown = parser.parse_known_args(argv)
    if unknown:
        print("Ignoring RFPro/launcher arguments: " + " ".join(unknown))
    if arguments.parent_levels < 0:
        raise ValueError("--parent-levels cannot be negative.")
    return arguments


def main(argv: Sequence[str] | None = None) -> None:
    arguments = _parse_arguments(argv)
    import empro

    analysis = find_analysis(empro.activeProject, arguments.analysis)
    output = empro.output.AnalysisOutput(analysis)
    registered_paths = [
        Path(str(path)) for path in (output.getAvailableSimulationPaths() or [])
    ]
    scan_root = derive_scan_root(
        arguments.root,
        str(analysis.simulationGroupPath or ""),
        registered_paths,
        arguments.parent_levels,
    )
    print_cache_inventory(analysis, registered_paths, scan_root)


if __name__ == "__main__":
    main()
