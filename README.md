# psae-factor

Factor analysis & IC tear sheets for **PSAE** — analogous to Quantopian's **Alphalens**.

## Quick start

```python
import psae_factor as pf

factor_data = pf.get_factor_and_returns(signals, pricing, periods=[1,4,24,120])
ic = pf.compute_ic(factor_data)
print(ic)

fig = pf.create_full_tear_sheet(factor_data)
```

## Key metrics
- Mean IC / IC t-stat / IC p-value per holding period
- IC decay curve (signal half-life)
- Q5-Q1 long-short spread
- Sector-conditional returns
- Regime-conditional IC (VIX buckets)

## License
Apache 2.0
