# Cahier de charge du projet
## Focntionnalité
- Gestion travaux au moyen d'ordre de travail
- Planification/ préparation intervention
- Gestion criticité equipement
- Mise en place procédure prédiction durée de vie equipements
- Exploitation historique equipements et analyse des pannes;
- Analyse performance et pilotage maintenance grace à un tableau de bord


les elements du gmao
- L'ordre de travail
- Base de donné des équipements et du matériel
- Gestion des articles
- Les achats
- La sous traitance
- La programmation des travaux (planification, preventif)
- Ressources humaines

### 1- Ordre de travail
- L'ordre de travail porte un numéro unique.
- Description de la demande.
- L'equipement concerné.
- Date de demande et d'execution.

#### Attribut:
- Ot_id
- Listes des équipements
- gammes
- Planification
- Responsable
- Listes des opérations
- Listes des sous opérations

#### Fonction de l'ordre
L'ordre a pour fonction de:
- Décrire les opérations à réaliser:
- - par saisie directe ou changements d'un texte descriptif
- - par utilisation de gammes d'opérations
- Définir les techniciens pour l'intervention.
- Définir le materiel, les equipements à installer.
- Définir les composants à changer.
- Controler la disponibilité des composants souhaités.
- Identifier, préparer, reserver les composants utiliser.
- Définir la sequence des opérations à effectuer et les positionner dans le temps.
- Enregistrer les couts et dépenses engendrés.
- Supporter les statistiques internes.

#### Avancement de l'ordre
`Ouvert`, `Approuvé`, `Approuvé`, `En attente de pièce`, `En attente de permis`, `planifié`, `En cours d'execution`, `Travaux achevés`, `En attente de controle`, `a valider`, `Cloturé`

#### Préparation des travaux dans l'ordre de travail
L'objectif de la phase de préparation est de:
- definir quel type de travail réaliser (réparation, intervention, maintenance programmée, installation).
- qui effectue l'Ordre (ressources humaines, poste de travail, machine, atelier)
- quoi faire, description globale du service à effectuer.
- comment, avec quels moyens, l'ordre regroupe une succession d'opérations et de sous opérations, chauque operation à exécuter est décrite de manière detaillé avec indication du temp prévu.
- ou et quand le faire
- a quel cout


### 2- Equipements
La desscription des equipements se fait au moyen:
- des fiches equipements;
- De l'arborescence topologique ou fonctionnelle.
- De l'arborescence des centres de couts;
- De la liste des pièces de rechanges associées à chaque equipement

#### Satut equipement
`Actif`, `Abandonné`, `Marche`, `degradé`, `Standby`, `Arret maintenance`, `Reglage`, `Demarrage`, `En test`.

### Calendrier d'utilisation

### Compteurs

### 3- Gestion article pour la maintenance  
Gère:
- les stocks de pièces de rechanges (composant detachable)
- Les stocks des pièces réparé ou cassées.
- Les pièces d'usures
- Les stocks de consommables et de matières premières pour l'atelier de réparation.
- Les outillages collectifs

#### Fiche article
- Désignation/ référence
- consommation prévisionnelle
- durée de vie previsionnelle
- approvisionnement(facilité de s'approvisionner)
- stock souhaité
- nombres de machines
- probabilité de defaillance, prévisible ou non dans une période donné.
- criticité de la défaillance d'un composant

#### Nomenclature
On est amené à gérer trois type de nomenclature:
- la liste de toutes les pièces constitutive de l'équipement.
- La liste des pièces d'usure et de sécurité.
- La nomenclature des pièces stockés en magasin.

#### 4- Gestion de stock
Doit:
- supporter la démarche interne de mise en gestion d’une pièce ou d’un consommable (fiche
article, caractéristiques, criticité, décision de stocker…) ;
- gérer les emplacements, les affectations d’articles aux emplacements et les quantités à stocker;
- gérer les mouvements de pièces de rechange et consommables ;
- calculer les quantités économiques et les points de commandes, ou au moins pouvoir stocker
ces valeurs dans des paramètres de gestion de stock, ces valeurs ayant pu être calculées dans
d’autres applications (typiquement Excel) ;
- analyser les stocks et les consommations (classement ABC, taux de rotation des stocks,...) et
réaliser des statistiques 

#### Methode ABC   
Le coût, le
taux de rotation ou importance des consommations
Dans un magasin pour la maintenance ou le SAV, on stocke essentiellement des pièces d’usure :
souvent des articles industriels standardisés, par exemple des roulements ou des pièces spécifiques
à certains constructeurs ou certaines machines (classe B). À noter qu’il existe pour ces pièces
disponibles facilement dans le commerce des procédures d’assurance livraison, négociables avec
les fournisseurs.
On stocke aussi des articles de consommation courante, à coût plus faible, à délai d’approvisionnement très réduit : le tout-venant, ainsi que les produits chimiques non en vrac (classe C). On
y stocke enfin des pièces de sécurité ou pièces stratégiques (forte criticité, forte gravité), dont
le coût est en général plus élevé, à long délai d’approvisionnement (classe A : 20 % des pièces,
représentant 80 % de la valeur du stock). Leur rôle est de pallier une déficience en production,
dont l’arrêt serait trop coûteux pour être tolérable. La pièce est immédiatement remplacée et la
production redémarre, limitant ainsi les pertes de production. La pièce endommagée sera réparée
ou rebutée, le stock de la pièce de sécurité sera complété par une commande immédiate.
On peut souhaiter que les classes fassent partie de la codification de la pièce.