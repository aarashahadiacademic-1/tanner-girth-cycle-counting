#!/usr/bin/env python3
"""Verify 17 girth-only graphs and optionally remeasure Exact and Hybrid."""
import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

P = Path(__file__).resolve().parent
REF = Path(os.environ.get("REFERENCE_GRAPH_DIR", "/tmp/reference-tanner-graphs/graphs"))
parser = argparse.ArgumentParser()
parser.add_argument("--verify-only", action="store_true",
                    help="Compile and check all graph hashes and exact girth counts; do not change recorded times")
args = parser.parse_args()
if hasattr(os, "sched_getaffinity"):
    cpu = min(os.sched_getaffinity(0))
    os.sched_setaffinity(0, {cpu})
    print("PINNED_CPU", cpu, flush=True)
subprocess.run([sys.executable, str(P / "generate_graphs.py")], check=True)
exe = P / "counter-100"
subprocess.run(["g++", "-std=c++17", "-O3", "-DNDEBUG",
                str(P / "benchmark_100.cpp"), "-o", str(exe)], check=True)
with (P / "FINAL_TABLE.csv").open(newline="") as stream:
    reader = csv.DictReader(stream)
    fields = reader.fieldnames
    rows = list(reader)
if len(rows) != 17:
    raise RuntimeError("Expected 17 girth-only graphs")
for row in rows:
    name = row["graph"]
    graph = (REF if name.startswith(("R", "P")) else P / "graphs") / (name + ".edges")
    if not graph.is_file():
        raise RuntimeError("Missing graph: " + str(graph))
    if hashlib.sha256(graph.read_bytes()).hexdigest() != row["sha256"]:
        raise RuntimeError("Graph SHA-256 mismatch: " + name)
    if args.verify_only:
        subprocess.run([str(exe), str(graph), row["g"], row["Ng"], "verify"],
                       text=True, capture_output=True, check=True, timeout=120)
        print("COUNT_VERIFIED", name, "Ng", row["Ng"], flush=True)
        continue
    process = subprocess.run([str(exe), str(graph), row["g"], row["Ng"], "100"],
                             text=True, capture_output=True, timeout=1200, check=True)
    result = json.loads(process.stdout)
    if result["n"] != int(row["n"]) or result["Ng"] != int(row["Ng"]):
        raise RuntimeError("Count/size mismatch: " + name)
    for key in ("Exact_ms", "Hybrid_ms", "Exact_std_ms",
                "Hybrid_std_ms", "MARE_percent"):
        row[key] = result[key]
    print("VERIFIED_100", name, "Exact", result["Exact_ms"],
          "Hybrid", result["Hybrid_ms"], flush=True)
if args.verify_only:
    print("ALL_17_HASHES_AND_COUNTS_VERIFIED", flush=True)
    sys.exit(0)
import io
out = io.StringIO()
writer = csv.DictWriter(out, fieldnames=fields)
writer.writeheader()
writer.writerows(rows)
(P / "FINAL_TABLE.csv").write_text(out.getvalue())
print("COMPLETE", len(rows), "100-run graphs; updated FINAL_TABLE.csv", flush=True)


def display(x):
    return "0" if float(x) == 0 else f"{float(x):.2f}"
def highlight(x, winner):
    return "\\textbf{" + display(x) + "}" if winner else display(x)
tex = [
    r"\begin{table}[t]", r"\centering",
    r"\caption{Exact and Hybrid girth-cycle counting. Mean runtimes are in milliseconds over 100 runs; MARE is in percent.}",
    r"\label{tab:combined-exp}", r"\scriptsize",
    r"\setlength{\tabcolsep}{2pt}", r"\begin{tabular}{lccrrrrr}\hline",
    r"Graph & $(d_v,d_c)$ & $g$ & $n$ & $N_g$ &",
    r"Exact & Hybrid & MARE\\\hline"
]
md = [
    "# Exact versus Hybrid: girth-cycle counting", "",
    "Arithmetic means of 100 executions per method and graph (milliseconds).", "",
    "| Graph | (dv,dc) | g | n | Ng | Exact | Hybrid | MARE (%) |",
    "|---|---|---:|---:|---:|---:|---:|---:|"
]
for x in rows:
    exact_ms = float(x["Exact_ms"])
    hybrid_ms = float(x["Hybrid_ms"])
    exwin = exact_ms <= hybrid_ms
    ex = highlight(exact_ms, exwin)
    hy = highlight(hybrid_ms, not exwin)
    mare = display(x["MARE_percent"])
    tex.append(f"{x['graph']} & $({x['dv']},{x['dc']})$ & {x['g']} & {x['n']} & {x['Ng']} & {ex} & {hy} & {mare} " + r"\\")
    md_ex = "**" + display(exact_ms) + "**" if exwin else display(exact_ms)
    md_hy = "**" + display(hybrid_ms) + "**" if not exwin else display(hybrid_ms)
    md.append(f"| {x['graph']} | ({x['dv']},{x['dc']}) | {x['g']} | {x['n']} | {x['Ng']} | {md_ex} | {md_hy} | {mare} |")
tex.extend([r"\hline", r"\end{tabular}", r"\end{table}", ""])
md.extend(["", "## Sample standard deviations across 100 runs (ms)", "",
           "| Graph | Exact SD | Hybrid SD |", "|---|---:|---:|"])
for x in rows:
    md.append(f"| {x['graph']} | {display(x['Exact_std_ms'])} | {display(x['Hybrid_std_ms'])} |")
md.extend(["", "Full-precision means and graph hashes are in FINAL_TABLE.csv.", ""])
(P / "FINAL_TABLE.tex").write_text("\n".join(tex))
(P / "FINAL_TABLE.md").write_text("\n".join(md))
print("UPDATED_CSV_TEX_MD", flush=True)
