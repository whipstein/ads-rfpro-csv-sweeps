"""Open the combined RFPro diagnostics dropdown."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence


def main(argv: Sequence[str] | None = None) -> None:
    from empro.toolkit import scripting

    launcher = Path(__file__).resolve().parent / "rfpro_tool_launcher.py"
    scripting.run(
        str(launcher),
        ["--category", "diagnostics", *(list(argv) if argv is not None else [])],
    )


if __name__ == "__main__":
    main()
