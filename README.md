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
