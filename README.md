# Exact and Hybrid Girth-Cycle Counting in Tanner Graphs

Reproducible source and results for the paper's **17 girth-only (T = g)** comparisons.

## Results

- [Final single-column LaTeX table](FINAL_TABLE.tex)
- [Full-precision runtimes, MARE, standard deviations and graph SHA-256 hashes](FINAL_TABLE.csv)
- [Readable table](FINAL_TABLE.md)

**Provenance:** The reported 100-run means for Exact and Hybrid were copied **without changing any measurements** from the prior verified 17-graph table. The original timing blocks ran additional methods, so these are historical timings, not post-migration remeasurements. A new benchmark with just Exact and Hybrid may yield different timings.

## Source code

- `exact_hybrid.cpp` contains the **original, unchanged** girth-counting `G`, `ExactState`, `exact`, `Sampler`, `Bvalue`, `HybridResult` and `hybrid` definitions extracted from the previous implementation. Only unrelated functions and command-line code were excluded.
- `benchmark_100.cpp` preserves the old 100-repetition randomized measurement harness, but runs **only Exact and Hybrid**.
- `generate_graphs.py` is copied unchanged from the previous repository.
- `run_100.py` regenerates and verifies the input graphs, compiles the benchmark, and can perform new 100-run measurements.

The hybrid uses 100 required closures and the original quantum of 8192. The two algorithms share the same exact-counting kernel. No code for longer cycle lengths is included.

## Inputs and reproducibility

13 of the 17 input graphs are created deterministically by `generate_graphs.py`. The R1200, R2400, P1200 and P1600 input edge lists are read from a **separate graph-data corpus** at https://github.com/aarashahadiacademic-1/tanner-cycle-counting . Set `REFERENCE_GRAPH_DIR` to its `graphs/` folder (default: `/tmp/reference-tanner-graphs/graphs`).

```sh
python3 run_100.py --verify-only
python3 run_100.py
```

Compilation: `g++ -std=c++17 -O3 -DNDEBUG`. The runner pins itself and child processes to one logical CPU on supported Linux hosts. Each method is measured 100 times with randomized order; each Exact count is checked against the recorded value, and Hybrid MARE includes exact returns. Input construction is excluded from timings.
