# Master IG Feature Notes

- Target: `IG target from OAS BAMLC0A0CM (percent → ×100 = bps).`
- Term spreads (`TERM_*`): business-cycle / monetary stance proxies; impact credit spreads.
- `VIXCLS`, `d_VIXCLS`: market uncertainty and changes in risk aversion.
- Treasury yields (`DGS*`/`GS*`) and their deltas: level/curve shape effects on spreads.
- `UNRATE`, `CPIAUCSL`, `PCEPI`, `INDPRO` (+ deltas): labor/inflation/production fundamentals tied to default risk.
- Inflation expectations (`T10YIE`, `T5YIE`, `T5YIFR`): pricing of real vs nominal risk.
- Liquidity (`mkt_par_lb`, `mkt_n_trades`, `mkt_share_rpt`, `mkt_px_std_daily`) + deltas: liquidity premia.
- AR/MA-like: `IG_spread_lag*`, `dIG_spread_lag*`, and rolling mean/std of `IG_spread`.

Columns: 126 | Rows: 311