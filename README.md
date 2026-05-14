# BCRP ANALYTICS

This repository contains analytics and research projects built using BCRP public data, focused on:
- payment systems,
- inflation and macroeconomic indicators,
- financial system analysis,
- and reusable Python utilities for retrieving and processing BCRP datasets.

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
│   └── utils.py
│
├── requirements.txt
├── setup.py
├── .gitignore
└── README.md
```

---

# Main Components

| Folder | Description |
|---|---|
| `metadata/` | BCRP metadata catalog used to search and organize series codes |
| `payment-system/` | Payment system analysis notebooks and market research |
| `bcrp_analytics/` | Reusable Python utilities for retrieving and processing BCRP data |
| `reports/` | Generated reports and visualizations |
| `data/` | Local temporary datasets (excluded from GitHub) |

---

# Current Features

- Download and clean BCRP time series data
- Build custom datasets from multiple BCRP series
- Payment-system market analysis
- MCC-based merchant segment analysis
- Exploratory analysis of wallets, immediate payments and acquiring markets

---

# TODO

1. Add documentation and examples for `bcrp_analytics` utilities and tests
2. Create specialized modules for inflation, exchange rates and payment systems
3. Add caching and validation logic to avoid unnecessary API requests