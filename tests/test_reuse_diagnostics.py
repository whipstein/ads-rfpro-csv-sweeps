from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, relative_path: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


DIAGNOSE = load_module(
    "diagnose_analysis_reuse",
    "rfpro_scripts/diagnose_analysis_reuse.py",
)
FINDER = load_module(
    "find_reusable_simulation_caches",
    "rfpro_scripts/find_reusable_simulation_caches.py",
)


class ReuseDiagnosticTests(unittest.TestCase):
    def temporary_root(self) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        return Path(directory.name)

    def test_cache_status_checks_one_exact_case_root(self) -> None:
        root = self.temporary_root() / "000001"
        (root / "emds_dsn" / "design").mkdir(parents=True)
        (root / "Run0001").mkdir()
        (root / ".reuse.hash").write_text("{}", encoding="utf-8")
        (root / "emds_dsn/design/.reusable").touch()
        (root / "emds_dsn/design/options.xml").touch()
        (root / "emds_dsn/design/design.sat").touch()
        (root / "Run0001/project.input").touch()
        (root / "Run0001/geometry.input").touch()

        self.assertTrue(all(DIAGNOSE.cache_status(root).values()))

    def test_log_evidence_returns_only_matching_tail(self) -> None:
        root = self.temporary_root()
        log = root / "project.log"
        log.write_text(
            "ordinary line\nExisting FEM mesh could not be reused\n"
            "Mesh and refinement is skipped, reusing existing mesh\n",
            encoding="utf-8",
        )

        evidence = DIAGNOSE.reuse_log_evidence(root, limit=1)

        self.assertEqual(len(evidence), 1)
        self.assertEqual(
            evidence[0][1],
            ["Mesh and refinement is skipped, reusing existing mesh"],
        )

    def test_cache_finder_reports_unique_roots(self) -> None:
        scan_root = self.temporary_root()
        first = scan_root / "group-a" / "000001"
        second = scan_root / "group-b" / "000002"
        (first / "emds_dsn/design").mkdir(parents=True)
        (second / "emds_dsn/design").mkdir(parents=True)
        (first / ".reuse.hash").touch()
        (first / "emds_dsn/design/.reusable").touch()
        (second / "emds_dsn/design/.reusable").touch()

        roots = FINDER.find_cache_roots(scan_root)

        self.assertEqual(
            {FINDER.normalized_path(path) for path in roots},
            {FINDER.normalized_path(first), FINDER.normalized_path(second)},
        )

    def test_scan_root_can_walk_above_group(self) -> None:
        root = self.temporary_root()
        group = root / "rfpro" / "000001"

        scan_root = FINDER.derive_scan_root("", str(group), [], 2)

        self.assertEqual(scan_root, root)


if __name__ == "__main__":
    unittest.main()
