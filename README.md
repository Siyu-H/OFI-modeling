# Order Flow Imbalance (OFI) Feature Engineering

This project implements a set of functions for extracting and analyzing various forms of Order Flow Imbalance (OFI) from high-frequency limit order book data. It is based on the research paper **"Cross-Impact of Order Flow Imbalance in Equity Markets"** and fulfills **Task 1** of the modeling assessment by operationalizing the proposed features and their variations.

## Project Structure


```
OFI-modeling/
├── data/
│   ├── first_25000_rows.csv                # Input data (symbol, ts_event, order book levels)
│   ├── best_level_ofi.csv                  # Output: Best-level OFI
│   ├── multi_level_ofi.csv                 # Output: Multi-level OFI
│   ├── integrated_ofi.csv                  # Output: Integrated OFI
│   └── cross_asset_ofi_<symbol>.csv        # Output: Cross-asset OFI per target
├── src/
│   ├── ofi_best_level.py                   # Computes best-level OFI
│   ├── ofi_multi_level.py                  # Computes multi-level OFI
│   ├── ofi_integrated.py                   # Computes integrated (rolling) OFI
│   └── ofi_cross_asset.py                  # Computes cross-asset OFI features
├── tests/
│   └── test_ofi_functions.py               # Unit tests for all OFI modules
├── main.py                                 # Driver script to compute and save OFI features
├── requirements.txt                        # Required Python packages
├── test-report.log                         # Log output of unit tests
├── pyproject.toml                          # Modern build configuration file
└── README.md                               # Project overview and usage instructions
```

## Requirements

```text
pandas>=1.5
numpy>=1.20
pytest>=7.0
```

Install with:

```bash
pip install -r requirements.txt
```

## OFI Feature Definitions

### 1. Best-Level OFI

**Location:** `src/ofi_best_level.py`

**Logic:**

```python
OFI_t = (bid_sz_00[t] - bid_sz_00[t-1]) - (ask_sz_00[t] - ask_sz_00[t-1])
```

This captures the net change in liquidity at the best bid and ask levels (Level 0).

### 2. Multi-Level OFI

**Location:** `src/ofi_multi_level.py`

**Logic:**

```python
OFI_t = Σ_i (1 / (i + 1)) * [(bid_sz_i[t] - bid_sz_i[t-1]) - (ask_sz_i[t] - ask_sz_i[t-1])]
```

The OFI across multiple levels, where each level's impact is discounted by its depth. Shallower levels are given more weight (1 / (i + 1)).

### 3. Integrated OFI

**Location:** `src/ofi_integrated.py`

**Logic:**

```python
Integrated_OFI_t = RollingAggregate(OFI, window=W)
```

Where `RollingAggregate` can be either:

* `sum` (default): cumulative pressure over past window
* `mean`: smoothed average order flow pressure

The use of `min_periods = window` ensures that only complete windows contribute to the signal, aligning with the methodology of the reference paper.

### 4. Cross-Asset OFI

**Location:** `src/ofi_cross_asset.py`

**Logic:**

```python
Cross_OFI_target_t = OFI_base_t'  where t' ≤ t and (t - t') ≤ 1s
```

This aligns the OFI of a base symbol (e.g., SPY) to a target symbol (e.g., AAPL) based on nearest past timestamps within a one-second tolerance. It captures potential cross-asset influence.

## How to Run

1. Place your input file `first_25000_rows.csv` in the `data/` directory.
2. Run the main script:

```bash
python main.py
```

The script will generate the following output files:

* `data/best_level_ofi.csv`
* `data/multi_level_ofi.csv`
* `data/integrated_ofi.csv`
* `data/cross_asset_ofi_<symbol>.csv`

## Unit Testing

All computation modules are validated using unit tests based on synthetic inputs. These tests ensure numerical correctness, shape compatibility, and appropriate error handling.

To run tests and log the output:

```bash
PYTHONPATH=. pytest tests/ | tee test-report.log
```

## Academic Background

This implementation is developed in response to **Task 1** of an assessment on order book modeling. It is grounded in the academic literature on microstructure, particularly:

> Cont, Rama, and Adrien de Larrard. *"Price dynamics in a Markovian limit order market."* SIAM Journal on Financial Mathematics 4.1 (2013): 1–25.

This project extends the original formulation by introducing:

* Weighted multi-level aggregation of order flow
* Rolling-window integration of OFI
* Cross-asset alignment of OFI as a feature

Each module is modular, well-documented, and suitable for downstream modeling or feature engineering in predictive pipelines.

