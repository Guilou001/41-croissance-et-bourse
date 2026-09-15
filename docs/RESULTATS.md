# Lire les résultats

Les CSV utilisent un point décimal pour les logiciels. Les rendements, fréquences et bornes de rendement sont enregistrés en fractions. Une valeur de 0,10 signifie 10 %. Les corrélations et les ratios de Sharpe restent des nombres sans unité. Les périodes et dénominateurs doivent être comparés avant les résultats.

## country_growth_returns.csv

Une ligne par pays et période. growth_geometric est la croissance composée réelle par habitant. return_geometric est le rendement composé réel des actions, dividendes compris.

## period_correlations.csv

Pearson compare les valeurs, Spearman leurs rangs. Les colonnes arithmétiques constituent une convention alternative. countries et years donnent la couverture exacte.

## leave_one_country_out.csv

Corrélation principale après retrait d’un pays. Le pays retiré est identifié. Cette sensibilité ne crée pas de nouvelles observations indépendantes.

## bootstrap_intervals.csv

Bornes à 95 % de la corrélation sous rééchantillonnage commun des années. positive_share est la part des tirages au-dessus de zéro, pas une valeur p classique.

## forecasts.csv

Une ligne par pays et année prévue. Les dernières années du prédicteur et de l’apprentissage sont conservées pour contrôler la chronologie.

## forecast_scores.csv

Gain de précision face à la moyenne passée. oos_r2 négatif signifie une augmentation de l’erreur quadratique. Les erreurs rmse sont des fractions de rendement annuel.

## forecast_uncertainty.csv

Intervalles sur le gain de précision agrégé. Les pertes réalisées sont rééchantillonnées ensemble par année, sans refaire chaque estimation du modèle.

## coverage.csv

Disponibilité macroéconomique et boursière par pays. Une couverture du PIB n’implique pas une couverture des rendements.

Les figures et les tableaux de l’article proviennent de ces sorties. [Revenir à l’article](../ARTICLE.md).
