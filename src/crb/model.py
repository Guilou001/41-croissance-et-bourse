"""Croissance composée, panel aligné et prévisions réellement décalées."""

import numpy as np
import pandas as pd


def real_return(nominal, inflation):
    return (1 + np.asarray(nominal)) / (1 + np.asarray(inflation)) - 1


def geometric(values, axis=0):
    values = np.asarray(values, dtype=float)
    if not np.isfinite(values).all() or (values <= -1).any():
        raise ValueError("Le taux composé nécessite des observations finies supérieures à −100 %")
    return np.expm1(np.log1p(values).mean(axis=axis))


def paired_correlations(x, y):
    """Une corrélation par ligne, sans gonfler le nombre de pays."""
    x = np.asarray(x) - np.asarray(x).mean(axis=-1, keepdims=True)
    y = np.asarray(y) - np.asarray(y).mean(axis=-1, keepdims=True)
    return (x * y).sum(axis=-1) / np.sqrt((x * x).sum(axis=-1) * (y * y).sum(axis=-1))


def forecasts(panel, start=1985, lag=2, window=5, minimum=20):
    """Prévoit r[t] avec le PIB connu conventionnellement jusqu'à t-lag.

    La base est révisée. Le décalage protège les dates du calcul, pas contre
    l'utilisation des révisions historiques qui sont absentes de ce millésime.
    """
    rows = []
    for iso, g in panel.groupby("iso"):
        g = g.sort_values("year").set_index("year").reindex(range(int(g.year.min()), int(g.year.max()) + 1))
        x = np.expm1(np.log1p(g.growth).rolling(window, min_periods=window).mean()).shift(lag)
        y = g.real_equity
        for year in g.index[g.index >= start]:
            train = pd.DataFrame({"x": x, "y": y}).loc[: year - 1].dropna()
            if len(train) < minimum or not np.isfinite(x.loc[year]) or not np.isfinite(y.loc[year]):
                continue
            design = np.column_stack([np.ones(len(train)), train.x])
            coef = np.linalg.lstsq(design, train.y, rcond=None)[0]
            rows.append(
                {
                    "iso": iso,
                    "year": year,
                    "actual": y.loc[year],
                    "prediction": coef[0] + coef[1] * x.loc[year],
                    "benchmark": train.y.mean(),
                    "predictor": x.loc[year],
                    "latest_predictor_year": year - lag,
                    "training_last_year": int(train.index.max()),
                    "training_n": len(train),
                }
            )
    return pd.DataFrame(rows)
