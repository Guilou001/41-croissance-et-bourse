"""Présentation pédagogique des résultats calculés."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .labels import NAMES
from .rendering import BLUE, GREY, ORANGE, compile_article, number, polish, save, style, table, templates


def read(name):
    """Lit une table de résultats CSV depuis le dépôt courant."""
    return pd.read_csv(f"results/tables/{name}.csv")


def publish():
    """Produit les quatre figures et insère les résultats dans les textes relus."""
    style()
    countries = read("country_growth_returns")
    primary = countries[countries.start_year.eq(1950) & countries.end_year.eq(2020)]
    correlations = read("period_correlations")
    corr = correlations.iloc[0].pearson_geometric
    fig, ax = plt.subplots(figsize=(9, 5.5), layout="constrained")
    x, y = primary.growth_geometric * 100, primary.return_geometric * 100
    ax.scatter(x, y, color=BLUE, s=48)
    # Small deterministic label offsets avoid calling labels evidence.
    offsets = {
        "FRA": (7, -14),
        "DEU": (7, -13),
        "JPN": (7, 7),
        "ITA": (7, -14),
        "CHE": (7, -13),
        "PRT": (7, -13),
        "AUS": (7, -13),
        "USA": (-40, 2),
    }
    for row in primary.itertuples():
        ax.annotate(
            NAMES[row.country],
            (row.growth_geometric * 100, row.return_geometric * 100),
            xytext=offsets.get(row.iso, (7, 7)),
            textcoords="offset points",
            fontsize=8,
        )
    coef = np.polyfit(x, y, 1)
    grid = np.array([x.min() - 0.1, x.max() + 0.25])
    ax.plot(grid, np.polyval(coef, grid), color=GREY, ls="--", lw=1, label="Relation linéaire descriptive")
    ax.set(
        xlabel="Croissance annuelle composée du PIB réel par habitant (%)",
        ylabel="Rendement annuel composé réel des actions (%)",
        title=f"Une croissance plus forte n'a pas garanti un meilleur rendement\n{len(primary)} pays, 1950 à 2020, corrélation {number(corr, 2)}",
    )
    ax.margins(x=0.16, y=0.16)
    ax.legend(fontsize=8)
    polish(ax)
    save(fig, "croissance_et_rendement")
    fig, ax = plt.subplots(figsize=(9, 4.8), layout="constrained")
    labels = [f"{int(r.start_year)} à {int(r.end_year)}" for r in correlations.itertuples()]
    ax.barh(
        labels,
        correlations.pearson_geometric,
        color=[BLUE if v < 0 else ORANGE for v in correlations.pearson_geometric],
    )
    ax.axvline(0, color=GREY, lw=1)
    ax.invert_yaxis()
    ax.set(
        xlabel="Corrélation entre pays",
        xlim=(-1, 1),
        title="Le signe de la relation change avec la période retenue",
    )
    for i, v in enumerate(correlations.pearson_geometric):
        ax.text(
            v + (0.03 if v >= 0 else -0.03), i, number(v, 2), ha="left" if v >= 0 else "right", va="center"
        )
    save(fig, "periodes")
    f = read("forecast_scores")
    subset = f[f.iso.ne("ALL")].sort_values("oos_r2")
    fig, ax = plt.subplots(figsize=(9, 6.1), layout="constrained")
    ax.barh(
        [NAMES[n] for n in subset.country],
        subset.oos_r2 * 100,
        color=[BLUE if x > 0 else ORANGE for x in subset.oos_r2],
    )
    ax.axvline(0, color=GREY, lw=1)
    ax.set(
        xlabel="Réduction de l'erreur quadratique par rapport à la moyenne passée (%)",
        title="Prévoir l'année suivante est une autre question\nPrévisions annuelles de 1985 à 2020, PIB révisé et décalé de deux ans",
    )
    polish(ax)
    save(fig, "prevision")
    ci = read("bootstrap_intervals")
    fig, ax = plt.subplots(figsize=(9, 4.4), layout="constrained")
    for i, row in ci.iterrows():
        ax.plot([row.lower, row.upper], [i, i], color=BLUE, lw=5, solid_capstyle="round")
        ax.scatter([row.estimate], [i], s=65, color=ORANGE, zorder=3)
    ax.axvline(0, color=GREY, ls="--", lw=1)
    ax.set(
        yticks=range(3),
        yticklabels=[f"Blocs de {int(b)} ans" for b in ci.block_years],
        xlabel="Corrélation entre les moyennes nationales",
        xlim=(-1, 1),
        title="Une estimation négative, mais une incertitude large\nIntervalles par rééchantillonnage conjoint des années, niveau de 95 %",
    )
    save(fig, "incertitude")
    score = f[f.iso.eq("ALL")].iloc[0]
    q = ci[ci.block_years.eq(5)].iloc[0]
    leave = read("leave_one_country_out")
    values = {
        "correlation": number(corr, 2),
        "countries": len(primary),
        "forecast_r2": number(score.oos_r2, 2, True),
        "ci_low": number(q.lower, 2),
        "ci_high": number(q.upper, 2),
        "leave_low": number(leave.pearson.min(), 2),
        "leave_high": number(leave.pearson.max(), 2),
        "forecast_n": int(score.observations),
        "period_table": table(
            ["Période", "Pays", "Corrélation entre croissance et rendement", "Corrélation des rangs"],
            [
                [
                    f"{int(r.start_year)} à {int(r.end_year)}",
                    int(r.countries),
                    number(r.pearson_geometric, 2),
                    number(r.spearman_geometric, 2),
                ]
                for r in correlations.itertuples()
            ],
        ),
        "country_table": table(
            ["Pays", "PIB réel par habitant par an", "Actions en pouvoir d'achat par an"],
            [
                [
                    NAMES[r.country],
                    number(r.growth_geometric, 2, True) + " %",
                    number(r.return_geometric, 2, True) + " %",
                ]
                for r in primary.sort_values("growth_geometric").itertuples()
            ],
        ),
        "forecast_ci_table": table(
            ["Longueur des blocs", "Borne basse", "Borne haute"],
            [
                [
                    str(int(r.block_years)) + " ans",
                    number(r.lower, 2, True) + " %",
                    number(r.upper, 2, True) + " %",
                ]
                for r in read("forecast_uncertainty").itertuples()
            ],
        ),
    }
    templates(values)
    compile_article("41-croissance-et-bourse")
