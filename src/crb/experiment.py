"""Comparaisons internationales descriptives et concours de prévision distinct."""

import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr

from .model import forecasts, geometric, paired_correlations, real_return
from .support import block_indices, config, save_table


def load_panel():
    d = pd.read_stata("data/raw/jst.dta", convert_categoricals=False).sort_values(["iso", "year"])
    d["growth"] = d.groupby("iso").rgdpmad.pct_change(fill_method=None)
    d["inflation"] = d.groupby("iso").cpi.pct_change(fill_method=None)
    d["real_equity"] = real_return(d.eq_tr, d.inflation)
    return d


def balanced(d, start, end):
    d = d[d.year.between(start, end)]
    growth = d.pivot(index="year", columns="iso", values="growth").reindex(range(start, end + 1))
    returns = d.pivot(index="year", columns="iso", values="real_equity").reindex(range(start, end + 1))
    keep = growth.notna().all() & returns.notna().all() & growth.gt(-1).all() & returns.gt(-1).all()
    names = list(keep[keep].index)
    return growth[names], returns[names]


def run():
    c = config()
    d = load_panel()
    country_names = d.drop_duplicates("iso").set_index("iso").country.to_dict()
    coverage = (
        d.groupby(["iso", "country"])
        .agg(
            growth_years=("growth", "count"),
            return_years=("real_equity", "count"),
            first_year=("year", "min"),
            last_year=("year", "max"),
        )
        .reset_index()
    )
    save_table(coverage, "coverage")
    periods = [(c["primary_start"], c["primary_end"]), (1900, 2011), *map(tuple, c["subperiods"])]
    countries, correlations = [], []
    for a, b in periods:
        g, r = balanced(d, a, b)
        if len(g.columns) < 3:
            raise ValueError("Moins de trois pays sur une fenêtre annoncée")
        x, y = geometric(g), geometric(r)
        for k, iso in enumerate(g.columns):
            countries.append(
                {
                    "start_year": a,
                    "end_year": b,
                    "iso": iso,
                    "country": country_names[iso],
                    "years": len(g),
                    "growth_geometric": x[k],
                    "return_geometric": y[k],
                    "growth_arithmetic": g[iso].mean(),
                    "return_arithmetic": r[iso].mean(),
                }
            )
        correlations.append(
            {
                "start_year": a,
                "end_year": b,
                "countries": len(x),
                "years": len(g),
                "pearson_geometric": pearsonr(x, y).statistic,
                "spearman_geometric": spearmanr(x, y).statistic,
                "pearson_arithmetic": pearsonr(g.mean(), r.mean()).statistic,
            }
        )
    save_table(pd.DataFrame(countries), "country_growth_returns")
    save_table(pd.DataFrame(correlations), "period_correlations")
    g, r = balanced(d, c["primary_start"], c["primary_end"])
    x, y = geometric(g), geometric(r)
    save_table(
        pd.DataFrame(
            [
                {
                    "omitted_country": country_names[iso],
                    "pearson": pearsonr(np.delete(x, k), np.delete(y, k)).statistic,
                }
                for k, iso in enumerate(g.columns)
            ]
        ),
        "leave_one_country_out",
    )
    rng = np.random.default_rng(c["seed"])
    intervals = []
    for block in c["block_years"]:
        idx = block_indices(len(g), c["bootstrap_draws"], len(g), block, rng)
        xb = geometric(g.to_numpy()[idx], axis=1)
        yb = geometric(r.to_numpy()[idx], axis=1)
        corr = paired_correlations(xb, yb)
        intervals.append(
            {
                "block_years": block,
                "draws": len(corr),
                "estimate": pearsonr(x, y).statistic,
                "lower": np.quantile(corr, 0.025),
                "median": np.median(corr),
                "upper": np.quantile(corr, 0.975),
                "positive_share": np.mean(corr > 0),
            }
        )
    save_table(pd.DataFrame(intervals), "bootstrap_intervals")
    # Fixed primary country set, post-war learning sample and revised GDP.
    pred = forecasts(
        d[d.iso.isin(g.columns) & d.year.ge(c["primary_start"])],
        start=c["prediction_start"],
        lag=c["predictor_release_lag_years"],
        window=c["lagged_growth_years"],
    )
    save_table(pred, "forecasts")
    scores = []
    for iso, p in [("ALL", pred), *list(pred.groupby("iso"))]:
        err = (p.actual - p.prediction) ** 2
        bench = (p.actual - p.benchmark) ** 2
        scores.append(
            {
                "iso": iso,
                "country": country_names.get(iso, "Ensemble des pays"),
                "observations": len(p),
                "oos_r2": 1 - err.sum() / bench.sum(),
                "rmse_model": np.sqrt(err.mean()),
                "rmse_benchmark": np.sqrt(bench.mean()),
            }
        )
    save_table(pd.DataFrame(scores), "forecast_scores")
    yearly = (
        pred.assign(
            loss_model=(pred.actual - pred.prediction) ** 2,
            loss_benchmark=(pred.actual - pred.benchmark) ** 2,
        )
        .groupby("year")[["loss_model", "loss_benchmark"]]
        .sum()
    )
    score_intervals = []
    for block in c["block_years"]:
        idx = block_indices(len(yearly), c["bootstrap_draws"], len(yearly), block, rng)
        sums = yearly.to_numpy()[idx].sum(axis=1)
        r2 = 1 - sums[:, 0] / sums[:, 1]
        score_intervals.append(
            {"block_years": block, "lower": np.quantile(r2, 0.025), "upper": np.quantile(r2, 0.975)}
        )
    save_table(pd.DataFrame(score_intervals), "forecast_uncertainty")
    d[["iso", "country", "year", "growth", "real_equity"]].to_parquet(
        "data/processed/panel.parquet", index=False
    )
