# Inflation Analytics

This project explores inflation dynamics in Peru using BCRP data, focusing on the Consumer Price Index (IPC), inflation rates, and macroeconomic analysis.

---

# Definitions

## IPC (Índice de Precios al Consumidor)

The IPC measures the price level of a representative basket of consumer goods and services relative to a base period.

Example:
- IPC Dec.2021 = 100
- IPC Apr.2026 = 120

This means that prices increased approximately 20% since Dec.2021.

---

## Inflation

Inflation is the percentage change of the IPC over time.

Monthly inflation:

```python
inflation = ipc.pct_change()
```

Interannual inflation:

```python
inflation_12m = ipc.pct_change(12)
```

---

# Sources

- Olivier Blanchard — *Macroeconomics*
- David Romer — *Advanced Macroeconomics*

---

# Findings

TODO

---

# TODOs

- Replicate official BCRP inflation series
- Compare monthly vs interannual inflation
- Analyze core inflation vs headline inflation
- Try to simulate how the BCRP deseasonalizes CPI series
- Explore ARIMA and Prophet for inflation forecasting
- Analyze inflation-adjusted payment system growth