# BCRP ANALYTICS

This repository contains analytics and research projects built using BCRP public data, focused on:

- payment systems
- inflation and macroeconomic indicators
- financial system analysis
- reusable Python utilities for retrieving and processing BCRP datasets

---

# Project Structure

```text
BCRP-ANALYTICS/
│
├── metadata/
│   └── BCRPData-metadata.csv
│
├── payment-system/
│   ├── README.md
│   ├── notebooks/
│   ├── reports/
│   └── data/
│
├── bcrp_analytics/
│   ├── __init__.py
│   ├── utils.py
│   └── bcrp_analyzer.py
│
├── pyproject.toml
├── poetry.lock
├── .gitignore
└── README.md
```

---

# Installation

This project uses Poetry for dependency management and packaging.


## Install dependencies

```bash
poetry install
```
---

# Example Usage

```python
from bcrp_analytics.utils import (
    build_bcrp_dataset,
    get_bcrp_clean_series,
)
```

---

# Current Features

- Download and clean BCRP time series data
- Build custom datasets from multiple BCRP series
- Inflation and IPC analysis utilities
- Deflation and real-growth utilities
- Payment-system market analysis
- Exploratory analysis of wallets, immediate payments and acquiring markets
- Shared caching system for reusable macroeconomic datasets

---

# TODO

1. Add documentation and examples for `bcrp_analytics` utilities and tests
2. Create specialized modules for inflation, exchange rates and payment systems
3. Improve dataframe validation and merge safety for time-series operations
4. Add visualization utilities for macroeconomic analysis
5. Add forecasting and deseasonalization experiments
