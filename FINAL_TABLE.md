# Exact versus Hybrid: girth-cycle counting

Original measured arithmetic means of 100 executions per method and graph, shown to two decimals (milliseconds).

| Graph | (dv,dc) | g | n | Ng | Exact | Hybrid | MARE (%) |
|---|---|---:|---:|---:|---:|---:|---:|
| A16c | (3,6) | 6 | 672 | 2560 | **0.10** | 0.78 | 4.30 |
| A128c | (3,6) | 6 | 5376 | 20480 | **0.96** | 1.08 | 8.63 |
| A256c | (3,6) | 6 | 10752 | 40960 | 2.64 | **1.68** | 8.63 |
| A128r | (3,6) | 6 | 5376 | 176 | **1.24** | 9.06 | 0 |
| B128c | (3,4) | 6 | 2560 | 4608 | **0.31** | 0.42 | 8.33 |
| C128c | (4,8) | 6 | 11264 | 204928 | 5.50 | **2.96** | 7.70 |
| C256c | (4,8) | 6 | 22528 | 409856 | 15.91 | **4.82** | 7.70 |
| C512c | (4,8) | 6 | 45056 | 819712 | 47.61 | **6.74** | 7.70 |
| C128r | (4,8) | 6 | 11264 | 1590 | **6.19** | 60.67 | 0 |
| R1200 | (4,8) | 6 | 1200 | 1564 | **0.92** | 4.36 | 0 |
| R2400 | (3,6) | 6 | 2400 | 155 | **0.83** | 4.13 | 0 |
| D16c | (3,6) | 8 | 4992 | 57680 | **3.75** | 3.77 | 7.58 |
| D32c | (3,6) | 8 | 9984 | 115360 | 8.60 | **4.85** | 7.58 |
| P1200 | (3,6) | 8 | 1200 | 65 | **0.99** | 6.80 | 0 |
| P1600 | (3,4) | 10 | 1600 | 11 | **2.11** | 11.38 | 0 |
| Q410 | (3,4) | 10 | 40448 | 40448 | **29.19** | 80.06 | 7.14 |
| Q412 | (3,4) | 12 | 36352 | 308992 | 70.35 | **57.64** | 10.13 |

## Standard deviations over 100 runs (ms)

| Graph | Exact SD | Hybrid SD |
|---|---:|---:|
| A16c | 0.01 | 0.05 |
| A128c | 0.04 | 0.11 |
| A256c | 0.16 | 0.16 |
| A128r | 0.07 | 0.12 |
| B128c | 0.03 | 0.05 |
| C128c | 0.16 | 0.30 |
| C256c | 0.56 | 0.46 |
| C512c | 0.51 | 0.70 |
| C128r | 0.21 | 0.90 |
| R1200 | 0.03 | 0.12 |
| R2400 | 0.02 | 0.07 |
| D16c | 0.09 | 0.36 |
| D32c | 0.15 | 0.46 |
| P1200 | 0.07 | 0.19 |
| P1600 | 0.04 | 0.12 |
| Q410 | 0.47 | 8.14 |
| Q412 | 0.79 | 5.90 |

`FINAL_TABLE.csv` preserves unrounded means and graph SHA-256 hashes. The recorded times originate from the prior randomized four-method measurement blocks, filtered without changing Exact or Hybrid values. Re-running the cleaned two-method benchmark will produce new measurements.
