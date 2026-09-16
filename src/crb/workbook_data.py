"""Prépare une sélection pédagogique de résultats pour le classeur."""

import json
from pathlib import Path

import pandas as pd

from .labels import NAMES

RULE = {
    "fixed": "Montant constant",
    "percentage": "Pourcentage du solde",
    "dynamic": "Ajustement limité",
    "floor": "Avec budget minimal",
}
PORT = {
    "reit": "Immobilier coté",
    "clone": "Remplacement estimé",
    "static_clone": "Mélange fixe 66 / 34",
    "base": "60 % actions et 40 % obligations",
    "with_reit": "Avec 10 % d’immobilier",
    "with_clone": "Avec 10 % de remplacement",
}


def table(name, subtitle, frame, columns):
    """Prépare le tableau de lecture en conservant les colonnes et leur ordre."""
    d = frame[[c[0] for c in columns]].copy()
    for col in d:
        if col == "country":
            d[col] = d[col].map(lambda name: NAMES.get(name, name))
        if col == "rule":
            d[col] = d[col].map(RULE)
        if col == "portfolio":
            d[col] = d[col].map(PORT)
    return {
        "name": name,
        "subtitle": subtitle,
        "headers": [c[1] for c in columns],
        "formats": [c[2] for c in columns],
        "rows": json.loads(d.to_json(orient="values")),
    }


def example(title, note, cells, checks):
    """Décrit les entrées et formules de l’exemple arithmétique Excel."""
    return {"name": "Exemple", "title": title, "subtitle": note, "cells": cells, "checks": checks}


def val(row, label, value, fmt="0.00"):
    """Décrit une cellule d’entrée numérique et son format d’affichage."""
    return {"row": row, "label": label, "value": value, "format": fmt}


def formula(row, label, expression, fmt="0.00"):
    """Décrit une cellule calculée et sa formule Excel explicite."""
    return {"row": row, "label": label, "formula": expression, "format": fmt}


def build():
    """Prépare la sélection Excel depuis les tables calculées et l’exemple connu."""
    root = Path.cwd()
    p = json.loads(Path("config/project.json").read_text())

    def read(name):
        return pd.read_csv(root / "results/tables" / f"{name}.csv")

    a = table(
        "Résultats",
        "Moyennes nationales, mêmes années pour chaque pays d’une fenêtre",
        read("period_correlations"),
        [
            ("start_year", "Première année", "0"),
            ("end_year", "Dernière année", "0"),
            ("countries", "Pays", "0"),
            ("pearson_geometric", "Corrélation des taux composés", "0.00"),
            ("spearman_geometric", "Corrélation des rangs", "0.00"),
        ],
    )
    b = table(
        "Prévisions",
        "Prévisions annuelles de 1985 à 2020, PIB révisé et décalé",
        read("forecast_scores"),
        [
            ("country", "Pays", "@"),
            ("observations", "Prévisions", "0"),
            ("oos_r2", "Réduction de l’erreur", "0.00%"),
            ("rmse_model", "Erreur du modèle", "0.00%"),
            ("rmse_benchmark", "Erreur du repère", "0.00%"),
        ],
    )
    e = example(
        "Croissance composée et correction de l’inflation",
        "Les entrées bleues peuvent être modifiées. Les cellules noires recalculent.",
        [
            val(7, "Rendement de la première année", -0.2, "0.0%"),
            val(8, "Rendement de la deuxième année", 0.25, "0.0%"),
            formula(10, "Moyenne arithmétique", "=(B7+B8)/2", "0.00%"),
            formula(11, "Moyenne composée", "=SQRT((1+B7)*(1+B8))-1", "0.00%"),
            val(14, "Rendement nominal", 0.20, "0.0%"),
            val(15, "Inflation", 0.10, "0.0%"),
            formula(17, "Rendement réel exact", "=(1+B14)/(1+B15)-1", "0.00%"),
        ],
        {"B10": 0.025, "B11": 0, "B17": 1 / 11},
    )
    e["mutation"] = {"input": "B7", "value": -0.1, "output": "B11", "expected": 0.06066017177982119}
    source_urls = [m["url"] for m in json.loads((root / "config/data_manifest.json").read_text()).values()]
    payload = {
        "title": p["title"],
        "repository": "https://github.com/Guilou001/" + p["repo"],
        "tables": [a, b],
        "example": e,
        "sources": source_urls,
    }
    (root / "results/workbook_data.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
