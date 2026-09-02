"""Regenerate the two self-contained RFPro launcher bundles.

The standalone operation scripts remain the readable, tested source of truth.
This builder compresses their exact UTF-8 source into the corresponding direct
RFPro entry file, allowing either launcher to be copied and run by itself.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import textwrap
import zlib
from pathlib import Path
from typing import Sequence


ROOT = Path(__file__).resolve().parents[1]
RFPRO_SCRIPTS = ROOT / "rfpro_scripts"
START_MARKER = "# BEGIN GENERATED EMBEDDED TOOLS"
END_MARKER = "# END GENERATED EMBEDDED TOOLS"
PAYLOAD_WIDTH = 88

BUNDLES = {
    "rfpro_workflow.py": (
        ("import_csv", "import_csv_parameter_sweeps.py"),
        ("run_analysis", "run_analysis_reuse_existing.py"),
        ("duplicate_analysis", "duplicate_analysis_with_results.py"),
        ("export_mdif", "export_analysis_mdif.py"),
        ("geometry_inspector", "preview_sweep_geometries.py"),
    ),
    "rfpro_diagnostics.py": (
        ("duplicate_conditions", "diagnose_duplicate_sweep_conditions.py"),
        ("analysis_reuse", "diagnose_analysis_reuse.py"),
        ("cache_inventory", "find_reusable_simulation_caches.py"),
        ("geometry_inspector", "preview_sweep_geometries.py"),
    ),
}


def encode_source(path: Path) -> tuple[str, str]:
    source = path.read_bytes()
    digest = hashlib.sha256(source).hexdigest()
    payload = base64.b85encode(zlib.compress(source, level=9)).decode("ascii")
    return digest, payload


def rendered_payload(entries: Sequence[tuple[str, str]]) -> str:
    lines = ["_EMBEDDED_TOOLS: dict[str, tuple[str, str, str]] = {"]
    for operation_key, filename in entries:
        source_path = RFPRO_SCRIPTS / filename
        if not source_path.is_file():
            raise FileNotFoundError(f"Bundle source does not exist: {source_path}")
        digest, payload = encode_source(source_path)
        lines.extend(
            [
                f"    {operation_key!r}: (",
                f"        {filename!r},",
                f"        {digest!r},",
                "        (",
            ]
        )
        for chunk in textwrap.wrap(payload, PAYLOAD_WIDTH):
            lines.append(f"            {chunk!r}")
        lines.extend(["        ),", "    ),"])
    lines.append("}")
    return "\n".join(lines)


def regenerated_text(
    launcher_text: str,
    entries: Sequence[tuple[str, str]],
) -> str:
    if launcher_text.count(START_MARKER) != 1 or launcher_text.count(END_MARKER) != 1:
        raise ValueError("Launcher must contain exactly one generated bundle region.")
    start = launcher_text.index(START_MARKER)
    end = launcher_text.index(END_MARKER, start) + len(END_MARKER)
    replacement = (
        START_MARKER + "\n" + rendered_payload(entries) + "\n" + END_MARKER
    )
    return launcher_text[:start] + replacement + launcher_text[end:]


def build(check_only: bool = False) -> list[Path]:
    changed: list[Path] = []
    for launcher_name, entries in BUNDLES.items():
        launcher_path = RFPRO_SCRIPTS / launcher_name
        current = launcher_path.read_text(encoding="utf-8")
        regenerated = regenerated_text(current, entries)
        if regenerated == current:
            continue
        changed.append(launcher_path)
        if not check_only:
            launcher_path.write_text(regenerated, encoding="utf-8", newline="\n")
    return changed


def _parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail when either committed launcher has stale embedded sources",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    arguments = _parse_arguments(argv)
    changed = build(check_only=arguments.check)
    if arguments.check and changed:
        names = ", ".join(path.name for path in changed)
        raise SystemExit(
            f"RFPro launcher bundles are stale: {names}. "
            "Run scripts/build_rfpro_bundles.py."
        )
    if changed:
        print("Regenerated: " + ", ".join(path.name for path in changed))
    else:
        print("RFPro launcher bundles are current.")


if __name__ == "__main__":
    main()
