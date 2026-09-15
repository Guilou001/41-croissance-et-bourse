# Vérifications effectuées

Contrôle local du 15 septembre 2026.

## Contrôles mathématiques et de données

La croissance composée nationale est recalculée directement depuis les niveaux du PIB aux deux extrémités. Le rendement réel des actions est recalculé depuis le produit des rendements nominaux et le rapport des IPC. La corrélation et le score de prévision agrégé sont ensuite confrontés aux tables publiées.

Les tests modifient les rendements futurs et les PIB encore trop récents. Les prévisions qui ne doivent pas en dépendre restent identiques. Les corrélations vectorisées sont aussi comparées à SciPy. Une année manquante exclut correctement un pays du panel équilibré.

Le fichier [verification.json](../results/verification.json) conserve 34 comparaisons numériques réussies, leur référence et leur tolérance. Ce nombre compte des cellules confrontées, pas autant de méthodologies indépendantes. Le script `scripts/independent_audit.py` permet de refaire ces contre-calculs avec les données locales.

## Cohérence entre calcul et présentation

Les résultats du README et de l’article sont insérés depuis les tables CSV. Les empreintes lient le code, le verrou de dépendances, le protocole et les sorties du dernier calcul. Les figures et les deux formes de l’article disposent également d’un manifeste.

Les quatre figures ont été examinées visuellement, sur fond blanc. Les PDF ont été ouverts et rendus en images pour vérifier les tableaux, les légendes et les sauts de page. Les exemples Excel ont été confrontés à des valeurs calculées à la main. Les modifications d’une hypothèse doivent changer le résultat attendu, puis l’hypothèse initiale est rétablie.

Le notebook lit le paquet et les tables. Il ne contient pas une seconde implémentation des méthodes scientifiques.

## Corrections pendant la réalisation

Les dossiers intermédiaires sont créés par la commande run, ce qui permet une exécution depuis un dépôt neuf. Les tableaux PDF ont été maintenus ensemble pour éviter de séparer l’en-tête des premières observations. Les paramètres et substitutions scientifiques sont décrits dans le protocole, y compris les décisions prises après inspection de la couverture des sources.

## Ce que les vérifications ne prouvent pas

Des tests réussis ne suppriment ni le biais des données disponibles, ni les hypothèses du bootstrap, ni les limites des indices de substitution. La CI vérifie le style, les tests et les artefacts publiés. Elle ne télécharge pas les sources et ne refait pas l’étude complète.

Le dépôt est un document de recherche personnel. Il n’a pas fait l’objet d’une évaluation par les pairs. Les conclusions restent conditionnelles aux données, périodes et hypothèses publiées.

```bash
uv run pytest
uv run crb verify
uv run python scripts/independent_audit.py
```
