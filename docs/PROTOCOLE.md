# Protocole de l’étude

Document de travail du 15 septembre 2026, rédigé avant le premier calcul complet. Il ne s’agit pas d’un préenregistrement indépendant. Les données avaient déjà été inspectées pour leur couverture.

La comparaison principale porte sur 1950 à 2020 et retient uniquement les pays observés pour chaque année. Le PIB réel par habitant vient de rgdpmad. Le rendement total des actions inclut les dividendes. Il est déflaté par l'IPC local avec le quotient exact des facteurs de croissance.

Nous comparons les moyennes géométriques par pays. Pearson décrit une relation linéaire, Spearman compare les rangs. Les contrôles portent sur les moyennes arithmétiques, le retrait d'un pays à la fois et quatre sous-périodes définies dans le fichier de configuration. La fenêtre 1900 à 2011 permet une comparaison de période avec Ritter, avec des indices différents.

Le bootstrap rééchantillonne les mêmes années pour tous les pays par blocs de 3, 5 et 10 ans. Il préserve les chocs internationaux communs à l'intérieur des blocs. Ses intervalles sont conditionnels aux pays présents et au mécanisme de rééchantillonnage.

Le concours de prévision est distinct. À partir de 1985, une régression par pays utilise la croissance moyenne des cinq années terminées deux ans avant le rendement prévu. Elle est réestimée avec les seules cibles des années antérieures. Le repère est le rendement moyen de ces mêmes années d'apprentissage. L'échantillon d'apprentissage commence en 1950 et contient au moins vingt observations valides.

Le PIB est révisé. Ce décalage évite d'utiliser le rendement futur dans l'estimation mais ne reconstitue pas les publications disponibles en temps réel. Les résultats ne démontrent ni causalité ni stratégie accessible à un investisseur en chaque date.

Les paramètres machine sont conservés dans [protocol.json](../config/protocol.json). Les corrections éventuelles de programmation sont consignées dans le journal de vérification.
