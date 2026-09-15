"""Contre-calcul séparé de résultats choisis, sans import du moteur scientifique."""

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

root = Path.cwd()
checks = []


def record(name, actual, reference, tolerance=1e-8):
    error = float(abs(actual - reference))
    assert error <= tolerance, (name, actual, reference, error)
    checks.append(
        {
            "check": name,
            "calculated": float(actual),
            "independent_reference": float(reference),
            "absolute_difference": error,
            "tolerance": tolerance,
        }
    )


raw = pd.read_stata(root / "data/raw/jst.dta")
published = pd.read_csv(root / "results/tables/country_growth_returns.csv").query(
    "start_year == 1950 and end_year == 2020"
)
xs, ys = [], []
for row in published.itertuples():
    g = raw[raw.iso.eq(row.iso)].set_index("year")
    base = g.loc[1949]
    last = g.loc[2020]
    growth = (last.rgdpmad / base.rgdpmad) ** (1 / 71) - 1
    ret = (math.prod(1 + g.loc[1950:2020].eq_tr) * base.cpi / last.cpi) ** (1 / 71) - 1
    record(row.iso + "_growth", row.growth_geometric, growth)
    record(row.iso + "_return", row.return_geometric, ret)
    xs.append(growth)
    ys.append(ret)
actual = pd.read_csv(root / "results/tables/period_correlations.csv").iloc[0].pearson_geometric
record("correlation", actual, np.corrcoef(xs, ys)[0, 1])
predictions = pd.read_csv(root / "results/tables/forecasts.csv")
error = sum((r.actual - r.prediction) ** 2 for r in predictions.itertuples())
baseline = sum((r.actual - r.benchmark) ** 2 for r in predictions.itertuples())
record(
    "pooled_prediction_score",
    pd.read_csv(root / "results/tables/forecast_scores.csv").iloc[0].oos_r2,
    1 - error / baseline,
)

output = {
    "date": "2026-09-15",
    "method": "Contre-calcul séparé, sans import des fonctions scientifiques du projet",
    "checks": checks,
    "passed": len(checks),
}
(root / "results/verification.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
print(len(checks), "comparaisons numériques réussies")
