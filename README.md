# Git_PDR_IMT

Indication :
Nous considérons que les camions partent de l'entrepôt central au début de la journée déjà chargé.
A chaque livraison de client, on retire la quantité de produit livré à la charge actuelle du camion

# 1. La classe Noeud représente un sommet du réseau.
Chaque nœud a notamment :

- id : identifiant unique
- nom : nom du lieu
- x, y : coordonnées
- time_window : plage horaire d’ouverture/fermeture
- requete_presente : indique s’il y a une demande active
- quantite : quantité demandée
- id_carg : identifiant de cargaison
- statut : "en_attente", "servi", "en_cours_livraison"
- heure_apparition : moment où la demande apparaît

# 2. La classe Arete relie :
- un nœud source
- un nœud cible
- un poids

# 3. Graphe : la carte routière
La classe Graphe stocke tout le réseau.
Elle contient :

- noeuds : dictionnaire des nœuds
- aretes : liste de toutes les arêtes
- adjacence : liste d’adjacence pour connaître les voisins
- demandes : liste de demandes construites depuis les nœuds actifs

Méthodes principales :
- ajouter_noeud(noeud) : Ajoute un nœud au graphe.
- ajouter_arete(source_id, cible_id, poids, **attributs) : Ajoute une route entre deux nœuds.
Si le graphe n’est pas orienté (oriente=False), il ajoute aussi la route inverse.
- voisins(noeud_id):Renvoie les voisins d’un nœud.
- poids_arete(source_id, cible_id) : Renvoie le poids d’une route directe entre deux nœuds.
- construire_demandes() : Construit une liste des demandes à partir des nœuds où requete_presente == True.
- dijkstra(depart_idx, arrivee_idx) : Implémente un calcul de plus court chemin.

# 4. Camion : le véhicule de livraison

La classe Camion représente un camion qui se déplace sur le graphe.
Attributs importants :

- id
- capacite
- disponible
- position
- destination
- route
- temps_restant_deplacement
- cible_actuelle
- charge_actuelle
- cargaison
- file_destinations  
- noeud_depot 

# 5. Gestion du chargement
- demander(...) : 
Ajoute une cargaison au dictionnaire cargaison, sans modifier réellement la charge.
Ça ressemble plus à un enregistrement de demande qu’à un vrai chargement.
- charger(...) : 
Ajoute une marchandise si la capacité le permet.
- decharger(...) :
Retire une marchandise du camion.

# 6. Calcul d’itinéraire
trouver_chemin_vers(destination, graphe) :
C’est un Dijkstra classique part de la position actuelle du camion
calcule la plus courte route jusqu’à destination
reconstruit le chemin
stocke le résultat dans self.route

# 7. Déplacement du camion

Il y a en réalité deux logiques de déplacement dans le code.

# A. Logique “temps continu”

Avec :
- assigner_demande
- _demarrer_deplacement
- mettre_a_jour
- _arriver_a_destination

Ici l’idée est :
on assigne une destination
on calcule une route
on enlève dt à un temps restant
quand le temps arrive à 0, le camion passe au sommet suivant

# B. Logique “tour par tour”
Avec :
- faire_un_tour
Ici le déplacement se fait à chaque tour de simulation :
- soit le camion est déjà en transit
- soit il part vers le prochain nœud
- soit il attend

# 8. distance_entre(...)

Fonction utilitaire qui calcule la distance la plus courte entre deux nœuds sans modifier les camions.
Elle sert dans le dispatch pour choisir le camion libre le plus proche d’une demande.

# 9. Ce que fait le main
Étape 1 : création du graphe
Étape 2 : création de deux camions
Étape 3 : création d’une ville en grille 4x4. On crée 16 nœuds, de A à P, avec ids de 0 à 15.
Étape 4 : ajout des routes
Étape 5 : demandes futures
Étape 6 : boucle de simulation
1. Apparition des nouvelles demandes
2. Dispatch intelligent
3. Avancer les camions

# 10. Le Dispatcher Intelligent & L'Heuristique d'Insertion

Plutôt que d'assigner la livraison au camion le plus proche géographiquement et de l'ajouter à la fin de son trajet (approche naïve), le dispatcher optimisé utilise une Cheapest Insertion Heuristic :

    Filtre de Stock Prévisionnel : Avant d'accepter une commande, le dispatcher calcule le "stock futur" du camion (charge actuelle - poids de toutes les commandes déjà présentes dans sa file d'attente). Un camion n'accepte une commande que s'il a une garantie de stock.

    Évaluation de l'Insertion : La méthode evaluer_meilleure_insertion simule l'insertion du nouveau client entre chaque arrêt déjà prévu dans la file_destinations.

    Calcul du Surcoût : Il calcule l'impact kilométrique de ce détour via la formule : Distance(A, Client) + Distance(Client, B) - Distance(A, B). La commande est assignée au camion (et à l'index précis) offrant le surcoût global le plus bas.

# 11. Logistique de Ravitaillement Automatique

Les camions gèrent désormais leurs propres allers-retours au dépôt. Si un camion termine sa tournée (ou est inactif) et que sa charge_actuelle tombe sous un seuil critique (ex: < 5 kg), le système appelle automatiquement la méthode assigner_demande_optimisee(g, depot) pour le renvoyer refaire le plein.

# 12. Tableau de Bord en Temps Réel (Live Dashboard)

Pour auditer le comportement de l'algorithme, un tableau de bord s'affiche dans la console à chaque tour de boucle. Il permet de monitorer en direct pour chaque camion :

    Sa position instantanée (ou sa direction en transit).

    Son objectif immédiat.

    Le contenu exact de sa file d'attente (multi-arrêts).

    Sa charge physique en temps réel.

# 13. Scalabilité et Graphes Complexes

Pour prouver l'efficacité de l'heuristique (Benchmark), le code inclut désormais une fonction graphe_complexe(). Elle génère un environnement de test massif (grille 6x6, 36 nœuds, 3 camions à haute capacité) permettant de lancer de véritables "avalanches de requêtes" et de tester les limites du Pathfinding et du Dispatcher.
