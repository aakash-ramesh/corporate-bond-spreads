# Master HY Feature Notes

- Target: `HY target from OAS BAMLH0A0HYM2 (percent → ×100 = bps).`
- Term spreads (`TERM_*`): business-cycle / monetary stance proxies; HY typically more cyclical.
- `VIXCLS`, `d_VIXCLS`: uncertainty tends to affect HY more strongly.
- Treasury yields + deltas: rate level and curve effects.
- `UNRATE`, `CPIAUCSL`, `PCEPI`, `INDPRO` (+ deltas): fundamentals relevant to default risk.
- Liquidity (`mkt_par_lb`, `mkt_n_trades`, `mkt_share_rpt`, `mkt_px_std_daily`) + deltas: HY spreads are sensitive to liquidity conditions.
- AR/MA-like: `HY_spread_lag*`, `dHY_spread_lag*`, and rolling mean/std of `HY_spread`.

Columns: 126 | Rows: 311