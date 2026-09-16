# Un pays qui s'enrichit enrichit-il ses actionnaires ?

Une économie peut produire davantage sans que les actions déjà cotées rapportent davantage. Une partie de la croissance profite aux salariés, aux nouvelles entreprises ou aux consommateurs. Le prix payé pour acheter une action compte aussi.

**Sur {{countries}} pays entre 1950 et 2020, la corrélation entre croissance réelle par habitant et rendement réel des actions vaut {{correlation}}. Son signe change selon la période.** Utiliser la croissance passée pour prévoir les rendements suivants n'améliore pas non plus la prévision moyenne sur l'ensemble des pays.

[Lire l’article](ARTICLE.md) · [Télécharger le PDF](rapport/rapport.pdf) · [Lire l’audit](docs/AUDIT_2026-09-15.md)

![Croissance et rendement par pays](results/figures/croissance_et_rendement.png)

Chaque point représente un pays, pas une année. Aller vers la droite signifie que le niveau de vie mesuré par le PIB par habitant a davantage augmenté. Monter signifie qu'un investissement en actions a davantage rapporté après inflation et dividendes.

## Un exemple simple

Une entreprise réalise 100 dollars de bénéfice avec 100 actions. Chaque action correspond à un dollar de bénéfice. Elle lève ensuite de l'argent et émet 20 actions supplémentaires. Si le bénéfice monte à 110 dollars, l'entreprise a grandi de 10 %. Le bénéfice par action est pourtant descendu à environ 0,92 dollar.

Ce mécanisme ne suffit pas à expliquer tous les résultats. Il montre pourquoi la croissance d'une économie et l'enrichissement des actionnaires existants sont deux objets différents.

## La question du papier

Jay Ritter examine cette distinction dans [Is Economic Growth Good for Investors?](https://doi.org/10.1111/j.1745-6622.2012.00385.x), publié en 2012. Il prolonge son article de 2005 sur la croissance et les rendements boursiers.

Notre étude reprend sa question avec des données publiques JST. Elle sépare deux exercices. Le premier décrit les pays qui ont grandi et rapporté davantage. Le second tente de prévoir le rendement de l'année suivante avec la croissance déjà observée. **Une relation descriptive n'est pas automatiquement une prévision exploitable.**

## Des résultats sensibles à la période

{{period_table}}

Les rendements sont composés et incluent les dividendes. Chaque fenêtre retient seulement les pays entièrement observés. Une corrélation de 1 signifie que les moyennes nationales s’alignent parfaitement sur une droite croissante. Le chiffre ne décrit pas leurs mouvements année par année. Une corrélation proche de zéro indique une relation linéaire faible.

![Relation selon la période](results/figures/periodes.png)

La relation n'est donc pas toujours négative. Le dépôt ne reprend pas l'estimation historique de Ritter comme si elle constituait une loi permanente.

## Et pour prévoir ?

Une régression est réestimée chaque année et pour chaque pays, sans utiliser les rendements futurs. Elle emploie la croissance moyenne des cinq années terminées deux ans plus tôt. Le repère est la moyenne des rendements d'apprentissage.

Sur {{forecast_n}} prévisions de 1985 à 2020, la réduction d'erreur vaut **{{forecast_r2}} %**. Un nombre négatif signifie que le modèle fait légèrement moins bien que le repère. Le PIB reste révisé, ce qui empêche de présenter cet exercice comme une simulation en temps réel.

## Explorer le projet

- [Article complet](ARTICLE.md) et [PDF avec résumé anglais](rapport/rapport.pdf)
- [Protocole](docs/PROTOCOLE.md) et [explications des concepts](docs/COMPRENDRE.md)
- [Données et limites](docs/DONNEES.md), [vérifications](docs/VERIFICATION.md)
- [Résultats Excel](results/resultats.xlsx) et [notebook pédagogique](notebooks/01_comprendre.ipynb)

```bash
uv sync --locked
uv run crb fetch
uv run crb run
uv run crb publish
uv run pytest
```

Le [guide de reproduction](docs/REPRODUIRE.md) présente les fichiers, les empreintes de données et l'entrepôt SQL. Aucune base payante n'est nécessaire.

## Ce qui reste hors de portée

L'échantillon contient des économies avancées dont les marchés ont survécu. Il n'inclut pas toutes les occasions d'investissement mondiales. Le Canada est présent dans les variables économiques JST mais n'a pas la série de rendements requise ici. L'étude ne mesure ni une causalité de la croissance sur les actions, ni une règle de choix des pays pour investir.

[![Tests automatiques](https://github.com/Guilou001/41-croissance-et-bourse/actions/workflows/ci.yml/badge.svg)](https://github.com/Guilou001/41-croissance-et-bourse/actions/workflows/ci.yml)

## English summary

Across-country economic growth and shareholder returns are distinct quantities. Using public JST data, this study compares long-run real GDP per capita growth with dividend-inclusive real equity returns. It then evaluates lagged-growth forecasts separately. The association changes across periods, while the forecasting exercise fails to improve the pooled historical-mean benchmark. Revised GDP and surviving-market coverage limit interpretation.
