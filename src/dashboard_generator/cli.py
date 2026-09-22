from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .core import DashboardError, build_dashboard, load_records


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="dashboard-generator", description="Generate a self-contained HTML dashboard from CSV or JSON.")
    p.add_argument("input", type=Path, help="UTF-8 CSV or JSON input")
    p.add_argument("-o", "--output", type=Path, default=Path("dashboard.html"))
    p.add_argument("--title", default="Data Dashboard")
    p.add_argument("--subtitle", default="Generated locally")
    p.add_argument("--theme", choices=("system", "light", "dark"), default="system")
    p.add_argument("--max-rows", type=int, default=1000)
    p.add_argument("--json", action="store_true", dest="json_output", help="Print build metadata as JSON")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__} — Radwan Abdulhadi Ahmed / @rad03i2")
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        records = load_records(args.input)
        result = build_dashboard(records, args.output, title=args.title, subtitle=args.subtitle, theme=args.theme, max_rows=args.max_rows)
    except (DashboardError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.json_output:
        print(json.dumps(result.as_dict(), ensure_ascii=False, indent=2))
    else:
        print(f"Wrote {result.output} ({result.rendered_rows}/{result.rows} rows, {len(result.columns)} columns)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
