from __future__ import annotations

import csv
import html
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


class DashboardError(ValueError):
    """Raised for invalid input or dashboard options."""


@dataclass(frozen=True)
class BuildResult:
    output: Path
    rows: int
    rendered_rows: int
    columns: tuple[str, ...]
    numeric_columns: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "output": str(self.output),
            "rows": self.rows,
            "rendered_rows": self.rendered_rows,
            "columns": list(self.columns),
            "numeric_columns": list(self.numeric_columns),
        }


def _display(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def load_records(path: Path) -> list[dict[str, Any]]:
    path = Path(path)
    if not path.is_file():
        raise DashboardError(f"input file not found: {path}")
    suffix = path.suffix.lower()
    try:
        if suffix == ".csv":
            with path.open("r", encoding="utf-8-sig", newline="") as handle:
                reader = csv.DictReader(handle)
                if not reader.fieldnames or any(not (name or "").strip() for name in reader.fieldnames):
                    raise DashboardError("CSV requires non-empty column headers")
                if len(set(reader.fieldnames)) != len(reader.fieldnames):
                    raise DashboardError("CSV column headers must be unique")
                return [dict(row) for row in reader]
        if suffix == ".json":
            data = json.loads(path.read_text(encoding="utf-8-sig"))
            if not isinstance(data, list) or any(not isinstance(item, dict) for item in data):
                raise DashboardError("JSON must be a top-level array of objects")
            return data
    except (UnicodeDecodeError, csv.Error, json.JSONDecodeError) as exc:
        raise DashboardError(f"cannot parse {path.name}: {exc}") from exc
    raise DashboardError("supported input formats are .csv and .json")


def _columns(records: Iterable[dict[str, Any]]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for record in records:
        for key in record:
            key = str(key)
            if key not in seen:
                seen.add(key)
                result.append(key)
    return result


def _numeric(values: Iterable[Any]) -> list[float]:
    result: list[float] = []
    for value in values:
        if value is None or isinstance(value, bool) or str(value).strip() == "":
            continue
        try:
            number = float(value)
        except (TypeError, ValueError):
            return []
        if not math.isfinite(number):
            return []
        result.append(number)
    return result


def _safe_json(value: Any) -> str:
    # Prevent a value containing </script> from ending the data script element.
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


def build_dashboard(
    records: list[dict[str, Any]],
    output: Path,
    *,
    title: str = "Data Dashboard",
    subtitle: str = "Generated locally",
    theme: str = "system",
    max_rows: int = 1000,
) -> BuildResult:
    if theme not in {"system", "light", "dark"}:
        raise DashboardError("theme must be system, light, or dark")
    if max_rows < 1:
        raise DashboardError("max_rows must be at least 1")
    if any(not isinstance(row, dict) for row in records):
        raise DashboardError("records must contain dictionaries")

    columns = _columns(records)
    numeric: dict[str, list[float]] = {}
    for column in columns:
        values = _numeric(row.get(column) for row in records)
        if values:
            numeric[column] = values

    normalized = [{column: _display(row.get(column)) for column in columns} for row in records[:max_rows]]
    cards = [f'<div class="card"><span>Rows</span><strong>{len(records):,}</strong></div>', f'<div class="card"><span>Columns</span><strong>{len(columns):,}</strong></div>']
    for column, values in list(numeric.items())[:4]:
        average = sum(values) / len(values)
        cards.append(f'<div class="card"><span>{html.escape(column)} · avg</span><strong>{average:,.2f}</strong><small>min {min(values):,.2f} · max {max(values):,.2f}</small></div>')

    theme_attr = html.escape(theme, quote=True)
    css = """
:root{color-scheme:light dark;--bg:#f6f7fb;--panel:#fff;--text:#172033;--muted:#687386;--line:#e5e8ef;--accent:#315efb}html[data-theme=dark]{--bg:#0e1420;--panel:#161e2d;--text:#eef3ff;--muted:#9aa8be;--line:#29354a;--accent:#86a4ff;color-scheme:dark}html[data-theme=light]{color-scheme:light}@media(prefers-color-scheme:dark){html[data-theme=system]{--bg:#0e1420;--panel:#161e2d;--text:#eef3ff;--muted:#9aa8be;--line:#29354a;--accent:#86a4ff}}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:14px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}.wrap{max-width:1200px;margin:auto;padding:32px 20px}h1{margin:0;font-size:30px}.sub{color:var(--muted);margin:5px 0 24px}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin-bottom:18px}.card,.panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;box-shadow:0 4px 18px #0000000a}.card{padding:16px}.card span,.card small{display:block;color:var(--muted)}.card strong{display:block;font-size:22px;margin:4px 0}.panel{overflow:hidden}.tools{padding:14px;border-bottom:1px solid var(--line);display:flex;gap:10px;align-items:center}.tools input{width:min(360px,100%);padding:9px 11px;border:1px solid var(--line);border-radius:9px;background:var(--bg);color:var(--text)}.count{margin-left:auto;color:var(--muted)}.table-wrap{overflow:auto;max-height:65vh}table{border-collapse:collapse;width:100%;white-space:nowrap}th,td{padding:10px 12px;border-bottom:1px solid var(--line);text-align:left}th{position:sticky;top:0;background:var(--panel);cursor:pointer;user-select:none}tbody tr:hover{background:color-mix(in srgb,var(--accent) 6%,transparent)}footer{color:var(--muted);margin-top:18px;font-size:12px}@media(max-width:600px){.wrap{padding:20px 12px}.tools{align-items:stretch;flex-direction:column}.count{margin-left:0}}
"""
    script = """
const rows=JSON.parse(document.getElementById('dataset').textContent);const cols=JSON.parse(document.getElementById('columns').textContent);const body=document.querySelector('tbody'),count=document.querySelector('.count'),q=document.querySelector('#search');let view=[...rows],sortCol='',asc=true;function draw(){body.textContent='';for(const row of view){const tr=document.createElement('tr');for(const c of cols){const td=document.createElement('td');td.textContent=row[c]??'';tr.appendChild(td)}body.appendChild(tr)}count.textContent=`${view.length} shown`}function filter(){const s=q.value.toLocaleLowerCase();view=rows.filter(r=>cols.some(c=>String(r[c]??'').toLocaleLowerCase().includes(s)));if(sortCol)sort();else draw()}function sort(){view.sort((a,b)=>{const x=a[sortCol]??'',y=b[sortCol]??'',nx=Number(x),ny=Number(y);const v=x!==''&&y!==''&&Number.isFinite(nx)&&Number.isFinite(ny)?nx-ny:String(x).localeCompare(String(y),undefined,{numeric:true});return asc?v:-v});draw()}q.addEventListener('input',filter);document.querySelectorAll('th').forEach(th=>th.addEventListener('click',()=>{const c=th.dataset.col;if(sortCol===c)asc=!asc;else{sortCol=c;asc=true}sort()}));draw();
"""
    headers = "".join(f'<th data-col="{html.escape(c, quote=True)}">{html.escape(c)}</th>' for c in columns)
    note = "" if len(records) <= max_rows else f"Showing the first {max_rows:,} of {len(records):,} rows."
    document = f'''<!doctype html><html lang="en" data-theme="{theme_attr}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><style>{css}</style></head><body><main class="wrap"><h1>{html.escape(title)}</h1><p class="sub">{html.escape(subtitle)}</p><section class="cards">{"".join(cards)}</section><section class="panel"><div class="tools"><input id="search" type="search" placeholder="Search rows…" aria-label="Search rows"><span class="count"></span></div><div class="table-wrap"><table><thead><tr>{headers}</tr></thead><tbody></tbody></table></div></section><footer>{html.escape(note)} Generated by Dashboard Generator · Radwan Abdulhadi Ahmed / @rad03i2</footer></main><script id="dataset" type="application/json">{_safe_json(normalized)}</script><script id="columns" type="application/json">{_safe_json(columns)}</script><script>{script}</script></body></html>'''
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(document, encoding="utf-8")
    return BuildResult(output.resolve(), len(records), len(normalized), tuple(columns), tuple(numeric))
