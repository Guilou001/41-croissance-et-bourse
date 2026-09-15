#set figure.caption(separator: [. ])
#set document(title: "Un pays qui s'enrichit enrichit-il ses actionnaires ?", author: "Guillaume Vaudescal")
#set page(
  paper: "a4",
  margin: (x: 2.2cm, y: 2.4cm),
  numbering: "1 / 1",
  footer: context [
    #set text(size: 8pt, fill: luma(90))
    #grid(columns: (1fr, auto), align: (left, right),
      [Document de recherche · Version 1.0], [#counter(page).display("1 / 1", both: true)])
  ],
)
#set text(font: ("Libertinus Serif", "Times New Roman", "DejaVu Serif"), size: 10.5pt, lang: "fr")
#set par(justify: true, leading: 0.68em, spacing: 1.1em)
#set heading(numbering: none)
#show heading.where(level: 2): it => block(sticky: true, above: 1.6em, below: 0.8em, text(size: 13pt, it))
#show heading.where(level: 3): it => block(above: 1.2em, below: 0.6em, text(size: 11pt, it))
#show raw.where(block: true): it => block(
  fill: luma(246), inset: 8pt, radius: 3pt, width: 100%, text(size: 8.5pt, it))
#show raw.where(block: false): it => text(size: 9pt, fill: rgb("#1a3f66"), it)
#show quote.where(block: true): it => block(
  inset: (left: 10pt), stroke: (left: 1.5pt + luma(180)),
  text(style: "italic", fill: luma(45), it.body))
// la table NE DOIT PAS être enfermée dans un par() : Typst 0.15 la supprime alors
// entièrement, sans erreur. Le réglage se pose donc dans la portée du bloc.
#show table: it => block(breakable: false, above: 1.1em, below: 1.1em,
  [#set par(justify: false); #text(size: 8.8pt, it)])
#show figure: it => block(above: 1.4em, below: 1.4em, it)
#show figure.caption: it => text(size: 8.5pt, fill: luma(70), it)
#show link: it => text(fill: rgb("#0072B2"), it)

#align(center)[
  #block(width: 100%)[
    #text(hyphenate: false, size: 18pt, weight: "bold")[Un pays qui s'enrichit enrichit-il ses actionnaires ?]
    #v(0.6em)
    #text(size: 10pt, fill: luma(70))[Guillaume Vaudescal · 15 septembre 2026 · #link("https://github.com/Guilou001/41-croissance-et-bourse")[Guilou001/41-croissance-et-bourse]]
  ]
]
#v(1.2em)
#line(length: 100%, stroke: 0.6pt + luma(190))
#v(0.8em)

Document de recherche, 15 septembre 2026. Adaptation publique des travaux de Jay Ritter.

== Résumé

Cette étude distingue la croissance économique, le rendement des actions existantes et la prévision des rendements futurs. Les données publiques JST permettent une comparaison homogène de 16 économies avancées entre 1950 et 2020. La corrélation entre croissance réelle par habitant et rendement composé réel des actions vaut -0,21. Elle change de signe lorsque la période change.

Un rééchantillonnage conjoint des années donne un intervalle de 95 % allant de -0,55 à 0,58 avec des blocs de cinq ans. L'estimation ne permet donc pas d'affirmer une relation négative stable. Un modèle utilisant la croissance passée obtient une réduction d'erreur de -0,51 % par rapport à la moyenne historique sur 576 prévisions. Les données de PIB sont révisées. Il s'agit d'un exercice chronologique sur ce millésime, sans reconstitution des publications en temps réel.

== 1. Pourquoi croissance et rendement ne sont pas synonymes

Le PIB mesure la production d'une économie. Une action représente une part d'une entreprise, achetée à un prix donné. Entre les deux se trouvent plusieurs mécanismes. De nouvelles entreprises peuvent créer de la richesse sans appartenir aux indices existants. Une entreprise cotée peut émettre des actions et partager son bénéfice entre davantage de propriétaires. Une amélioration de la productivité peut aussi profiter aux consommateurs sous forme de prix plus faibles.

Le prix initial de l'action constitue un autre lien. Une économie dont la croissance future est largement anticipée peut déjà se négocier à un prix élevé. Réaliser cette croissance ne suffit alors pas à donner un rendement exceptionnel à l'acheteur.

Ces mécanismes sont des explications possibles. Notre base ne contient pas tous les éléments nécessaires pour quantifier leur contribution respective. La corrélation descriptive ne les identifie pas séparément.

== 2. Place dans la littérature

Ritter (2005) étudie la relation entre croissance économique et rendement des actions sur une longue histoire internationale. Son texte de 2012, Is Economic Growth Good for Investors?, actualise la discussion. Il rapporte notamment une relation négative dans son échantillon de marchés développés jusqu'en 2011.

Hsu, Ritter, Wool et Zhao (2022) déplacent une partie de la question vers les marchés émergents et le bénéfice par action. Ce prolongement rappelle que la croissance d'un pays et celle du bénéfice attribuable à une action ne se confondent pas.

Notre apport n'est pas de découvrir cette distinction. Nous rendons la comparaison reproductible avec une autre base publique, testons sa stabilité selon les périodes et séparons explicitement la description de la prévision. Une estimation différente de celle de Ritter ne constitue pas à elle seule une réfutation. Les pays, indices et millésimes diffèrent.

== 3. Données et choix de mesure

La base JST R6 couvre 1870 à 2020 pour un ensemble d'économies avancées. Nous utilisons le PIB réel par habitant de la série rgdpmad, les rendements totaux des actions eq\_tr et l'IPC local cpi. La documentation de cette version signale des révisions des séries macroéconomiques et des mises à jour des sources de rendements.

La fenêtre principale de 1950 à 2020 retient 16 pays dont chaque année est complète. Nous n'interpolons ni les rendements ni le PIB. Le Canada et l'Irlande n'ont pas les rendements d'actions nécessaires. Les tableaux de couverture les montrent au lieu de laisser supposer qu'ils ont été analysés.

Pour chaque année, le rendement réel des actions est calculé par le rapport entre le facteur de rendement nominal et le facteur d'inflation.

#raw("Rendement réel = (1 + rendement nominal total) / (1 + inflation) − 1\nCroissance annuelle composée = exp(moyenne(log(1 + croissance annuelle))) − 1", block: true, lang: "text")

Une hausse nominale de 10 % avec une inflation de 10 % donne un rendement réel nul. Une hausse de 20 % avec la même inflation donne environ 9,09 %, et non 10 %.

La moyenne géométrique répond à la question du capital effectivement composé. Perdre 20 % puis gagner 25 % ramène au point de départ. La moyenne arithmétique des deux taux vaut pourtant 2,5 %. Nous publions les deux conventions comme contrôle, sans les mélanger.

== 4. Comparaison entre pays

Chaque observation du graphique principal est une paire de moyennes nationales calculées sur les mêmes années. Le nombre de points est donc 16. Il serait incorrect de traiter les milliers de lignes annuelles de la base comme autant d'observations indépendantes pour cette corrélation de long terme.

#figure(image("../results/figures/croissance_et_rendement.svg", width: 100%), caption: [Croissance et rendement])

#table(
  columns: 3,
  stroke: (x, y) => if y == 0 { (bottom: 0.6pt) } else { none },
  align: left + top,
  inset: 5pt,
    [*Pays*],
    [*PIB réel par habitant par an*],
    [*Actions en pouvoir d'achat par an*],
    [Suisse],
    [1,55 %],
    [6,33 %],
    [Royaume-Uni],
    [1,74 %],
    [6,46 %],
    [Australie],
    [1,88 %],
    [5,65 %],
    [États-Unis],
    [1,88 %],
    [7,57 %],
    [Danemark],
    [1,96 %],
    [7,91 %],
    [Suède],
    [2,05 %],
    [8,90 %],
    [Pays-Bas],
    [2,08 %],
    [7,19 %],
    [France],
    [2,09 %],
    [3,44 %],
    [Belgique],
    [2,16 %],
    [5,28 %],
    [Norvège],
    [2,45 %],
    [4,47 %],
    [Italie],
    [2,50 %],
    [3,03 %],
    [Finlande],
    [2,50 %],
    [8,47 %],
    [Allemagne],
    [2,73 %],
    [8,39 %],
    [Portugal],
    [2,77 %],
    [-0,49 %],
    [Espagne],
    [2,90 %],
    [4,75 %],
    [Japon],
    [3,65 %],
    [6,79 %],
)

La corrélation de Pearson mesure l'alignement linéaire des points. Spearman remplace les valeurs par les rangs. Un pays peut ainsi contribuer à une relation de rang sans imposer une distance numérique particulière aux autres pays.

La corrélation principale vaut -0,21. Lorsque l'on retire un pays à la fois, elle varie de -0,37 à -0,06. Ce contrôle indique la dépendance du résultat à un pays influent. Il ne remplace pas un modèle de l'incertitude.

== 5. Une relation qui dépend de la période

#table(
  columns: 4,
  stroke: (x, y) => if y == 0 { (bottom: 0.6pt) } else { none },
  align: left + top,
  inset: 5pt,
    [*Période*],
    [*Pays*],
    [*Corrélation des rendements composés*],
    [*Corrélation des rangs*],
    [1950 à 2020],
    [16],
    [-0,21],
    [-0,21],
    [1900 à 2011],
    [15],
    [-0,17],
    [-0,15],
    [1900 à 1949],
    [15],
    [0,38],
    [0,40],
    [1950 à 1984],
    [16],
    [0,03],
    [-0,05],
    [1985 à 2020],
    [16],
    [0,23],
    [0,11],
    [2000 à 2020],
    [16],
    [0,54],
    [0,52],
)

#figure(image("../results/figures/periodes.svg", width: 100%), caption: [Sous-périodes])

La fenêtre 1900 à 2011 s'approche de celle du papier de 2012, mais les indices et la couverture restent différents. Les sous-périodes de l'après-guerre produisent des relations positives alors que la moyenne sur 1950 à 2020 est négative. Ces coefficients répondent à des comparaisons différentes entre pays et ne doivent pas être présentés comme des contradictions arithmétiques.

La composition du panel est équilibrée à l'intérieur de chaque fenêtre. Elle peut changer entre fenêtres, lorsque des valeurs anciennes manquent. Les nombres de pays sont affichés pour rendre cette différence visible.

== 6. Mesurer l'incertitude sans casser les chocs mondiaux

Les pays subissent des guerres, des récessions et des changements de régime monétaire communs. Tirer leurs années séparément détruirait une partie de cette dépendance. Nous tirons donc les mêmes blocs d'années pour tous les pays.

Un bloc de cinq ans pourrait contenir cinq années consécutives avec tous les pays observés pendant ces années. Les blocs sont assemblés jusqu'à reconstituer soixante et onze années. Les indices sont circulaires, ce qui autorise un raccord entre la dernière et la première année. Ce raccord est un artifice du rééchantillonnage, pas une période historique réelle.

Les moyennes composées et leur corrélation sont recalculées pour chaque tirage. Cinq mille tirages sont réalisés pour chacune des longueurs de trois, cinq et dix ans. Les bornes sont les quantiles de 2,5 % et 97,5 % des corrélations obtenues.

#figure(image("../results/figures/incertitude.svg", width: 100%), caption: [Incertitude de la corrélation])

L'intervalle principal va de -0,55 à 0,58. Il couvre zéro ainsi que des relations positives et négatives. Il est conditionnel aux pays retenus et à l'histoire rééchantillonnée. Il ne couvre pas l'incertitude liée aux marchés absents ou aux révisions possibles de la base.

== 7. Prévoir demande une expérience séparée

La corrélation précédente utilise ce qui s'est effectivement produit pendant toute la période. Un investisseur placé au début d'une année ne connaît pas la croissance des années suivantes. Nous construisons donc un concours distinct.

Pour prévoir le rendement de l'année t, le modèle utilise la croissance moyenne des cinq années terminées en t moins deux. Par exemple, une prévision pour 2000 utilise les croissances de 1994 à 1998. La régression est propre à chaque pays. Elle est estimée sur les années antérieures à 2000, jamais sur son rendement ou celui des années suivantes.

L'apprentissage commence en 1950 et exige au moins vingt observations valides. Les prévisions publiées vont de 1985 à 2020. Le repère est la moyenne des rendements disponibles dans les mêmes lignes d'apprentissage. Cette égalité d'échantillon évite de favoriser un modèle en lui donnant davantage d'histoire.

#raw("Réduction de l'erreur = 1 − somme des erreurs du modèle au carré\n                           / somme des erreurs du repère au carré", block: true, lang: "text")

Une valeur de 5 % signifie que le modèle réduit de 5 % l'erreur quadratique. Une valeur de −5 % signifie qu'il l'augmente de 5 %. Ce résultat n'est pas un rendement de portefeuille.

#figure(image("../results/figures/prevision.svg", width: 100%), caption: [Prévision par pays])

Sur l'ensemble des 576 prévisions, la réduction d'erreur vaut -0,51 %. Quelques pays bénéficient de la variable. D'autres se dégradent. Le résultat agrégé ne soutient pas une amélioration générale par cette spécification simple.

#table(
  columns: 3,
  stroke: (x, y) => if y == 0 { (bottom: 0.6pt) } else { none },
  align: left + top,
  inset: 5pt,
    [*Longueur des blocs*],
    [*Borne basse*],
    [*Borne haute*],
    [3 ans],
    [-13,54 %],
    [9,81 %],
    [5 ans],
    [-16,10 %],
    [9,55 %],
    [10 ans],
    [-17,11 %],
    [9,86 %],
)

Ces intervalles rééchantillonnent les pertes de prévision par blocs d'années communs aux pays. Ils gardent les prévisions déjà produites. Ils mesurent l'incertitude de leur comparaison sur cette séquence et ne réestiment pas tout l'apprentissage dans chaque tirage.

== 8. Ce que le test chronologique ne résout pas

Les dates d'apprentissage sont contrôlées, mais les PIB sont révisés. La valeur de la croissance de 1998 présente dans JST R6 n'est pas nécessairement celle qu'un investisseur connaissait en 2000. Le décalage de deux années est une convention prudente de calendrier, pas une reconstruction des millésimes de publication.

L'échantillon est aussi sélectionné par la disponibilité et la survie des marchés. Les pays dont les marchés ont disparu ou sont devenus inaccessibles ne sont pas représentés de manière exhaustive. Enfin, les rendements locaux ne donnent pas directement le rendement d'un investisseur canadien exposé au change et aux retenues fiscales.

Il serait donc excessif d'écrire que la croissance n'a jamais d'information ou que les économies lentes sont toujours de meilleurs investissements. Le constat porte sur ces mesures, ces pays, ces périodes et ce modèle.

== 9. Vérification et prolongements

Les tests vérifient le calcul réel exact, la différence entre moyenne arithmétique et composée, le traitement des années manquantes et les corrélations par une implémentation indépendante de SciPy. Deux tests modifient les rendements futurs ou les PIB trop récents. Les prévisions qui doivent rester identiques sont confrontées avant et après ces modifications.

Un prolongement utile serait de travailler sur les prévisions de croissance disponibles en chaque date, puis sur les surprises entre croissance attendue et réalisée. Un autre demanderait le bénéfice par action et les émissions nettes d'actions pour distinguer directement croissance de l'entreprise et dilution. Ces données supplémentaires ne sont pas supposées présentes ici.

Le #link("docs/PROTOCOLE.md")[protocole], le #link("docs/DONNEES.md")[dictionnaire des données] et le #link("docs/VERIFICATION.md")[journal des contrôles] permettent de distinguer ce qui a été calculé de ces travaux possibles.

== English extended summary

Economic growth, returns to existing shareholders and return predictability are different research questions. This study uses public JST R6 data to compare real GDP per capita growth and dividend-inclusive real equity returns across 16 advanced economies from 1950 through 2020.

The long-run cross-country correlation is -0,21. Its sign changes across subperiods. Synchronous moving-block resampling preserves common annual international shocks within each block and produces wide uncertainty intervals. These intervals are conditional on the observed surviving countries and do not account for missing markets.

A separate expanding-window forecast exercise predicts annual equity returns using five-year GDP growth ending two years before the target year. Each country is estimated separately, with a matched historical-mean benchmark. Pooled out-of-sample error reduction is -0,51%. Future-target mutation tests check the chronology. GDP is nevertheless revised, so the design is not a vintage-correct real-time investment experiment.

The contribution is a transparent public-data robustness study, not a claim of exact replication or a new causal identification strategy.

== Références

Ritter, J. R. (2005). #link("https://site.warrington.ufl.edu/ritter/files/2015/04/Economic-growth-and-equity-returns-2005.pdf")[Economic Growth and Equity Returns]. Pacific-Basin Finance Journal, 13, 489–503.

Ritter, J. R. (2012). #link("https://doi.org/10.1111/j.1745-6622.2012.00385.x")[Is Economic Growth Good for Investors?]. Journal of Applied Corporate Finance, 24(3), 8–18.

Hsu, J., Ritter, J. R., Wool, P. et Zhao, Y. (2022). #link("https://site.warrington.ufl.edu/ritter/files/Emerging-Markets-Returns.pdf")[What Matters More for Emerging Market Investors, Economic Growth or EPS Growth?]. Journal of Portfolio Management, 48(8), 11–19.

Jordà, Ò., Knoll, K., Kuvshinov, D., Schularick, M. et Taylor, A. M. (2019). #link("https://doi.org/10.1093/qje/qjz012")[The Rate of Return on Everything, 1870–2015]. Quarterly Journal of Economics. #link("https://www.macrohistory.net/database/")[Base JST et documentation].
